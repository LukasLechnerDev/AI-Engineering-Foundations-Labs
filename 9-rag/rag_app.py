import html
import os
from functools import lru_cache
from pathlib import Path

import gradio as gr
import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field

MODEL = "gpt-5.6-luna"
EMBEDDING_MODEL = "text-embedding-3-large"

RAG_DIRECTORY = Path(__file__).resolve().parent
VECTOR_DB_PATH = RAG_DIRECTORY / "vector_db"

load_dotenv(RAG_DIRECTORY / ".env", override=True)

# Empty keys should disable tracing instead of causing export retries.
if not os.getenv("LANGFUSE_PUBLIC_KEY") or not os.getenv("LANGFUSE_SECRET_KEY"):
    os.environ["LANGFUSE_TRACING_ENABLED"] = "false"

# Langfuse must be initialized before the OpenAI client is imported.
from langfuse import get_client, propagate_attributes  # noqa: E402
from langfuse.langchain import CallbackHandler  # noqa: E402
from langchain_chroma import Chroma  # noqa: E402
from langchain_core.documents import Document  # noqa: E402
from langchain_core.messages import HumanMessage, SystemMessage  # noqa: E402
from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # noqa: E402

langfuse = get_client()

SYSTEM_PROMPT_TEMPLATE = """
You are a friendly and knowledgeable assistant helping the user with our knowledge
base about AI engineering job postings. Our knowledge base includes jobs that have
either AI or engineering in the title, and we also looked for jobs that are about
building applications on top of LLMs.

If relevant, use the given context to answer any question.
If you don't know the answer, say so.

Each document in the context starts with its source path. If your answer mentions
specific job postings, add each of them to `jobs` with its source path. The app
shows these jobs as cards with title, company, location, your reason, and link.
So don't list the jobs one by one in your answer. Keep it to a short summary.

Context:
{context}
"""

JOB_CARD_CSS = """
.job-card {
    border: 1px solid var(--border-color-primary);
    border-left: 4px solid var(--color-accent);
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    background: var(--background-fill-secondary);
}
.job-card h3 { margin: 0 0 4px; }
.job-card p { margin: 0 0 8px; }
.job-meta { color: var(--body-text-color-subdued); }
"""


class JobPick(BaseModel):
    source: str = Field(description="Source path of the job posting")
    why_it_fits: str = Field(description="One sentence on why this job fits")


class JobAnswer(BaseModel):
    answer: str = Field(description="Answer to the question, in Markdown")
    jobs: list[JobPick] = Field(description="Job postings mentioned in the answer")


@lru_cache
def get_retriever():
    """Create the retriever once and reuse it for later questions."""
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = Chroma(
        persist_directory=str(VECTOR_DB_PATH),
        embedding_function=embeddings,
    )
    # Several chunks often come from the same document, so we fetch 10 instead of 4
    return vectorstore.as_retriever(search_kwargs={"k": 10})


@lru_cache
def get_llm():
    """Create the language model once and reuse it for later questions."""
    return ChatOpenAI(temperature=0, model=MODEL, reasoning_effort="none")


def load_parent_documents(chunks: list[Document]) -> dict[str, str]:
    """Load the whole document of every chunk (parent document retrieval)."""
    # dict.fromkeys removes duplicate paths but keeps the order
    sources = dict.fromkeys(chunk.metadata["source"] for chunk in chunks)
    # The paths are relative to the RAG directory, not to the current working directory
    return {source: (RAG_DIRECTORY / source).read_text() for source in sources}


def read_frontmatter(document: str) -> dict:
    """Read the YAML block between the first two '---' lines of a document."""
    _, frontmatter, _ = document.split("---", 2)
    return yaml.safe_load(frontmatter)


def render_job_cards(jobs: list[JobPick], documents: dict[str, str]) -> str:
    """Turn the jobs picked by the LLM into HTML cards.

    Title, company, and URL come from the document itself, not from the LLM,
    so the link is always there and always correct.
    """
    cards = []
    for job in jobs:
        # Skip sources the LLM made up
        if job.source not in documents:
            continue
        posting = read_frontmatter(documents[job.source])
        # Skip documents that are not job postings, like company profiles
        if "job_url" not in posting:
            continue
        url = html.escape(posting["job_url"])
        # No blank lines inside a card, otherwise Markdown breaks the HTML apart
        cards.append(
            f'''<div class="job-card">
<h3>{html.escape(posting["title"])}</h3>
<p class="job-meta">{html.escape(posting["company"])} · {html.escape(posting["location"])}</p>
<p>{html.escape(job.why_it_fits)}</p>
<a href="{url}" target="_blank">{url}</a>
</div>'''
        )
    return "\n\n".join(cards)


def answer_question(
    question: str,
    history=None,
    request: gr.Request | None = None,
) -> str:
    """Answer one question using the local vector database."""
    langfuse_handler = CallbackHandler()
    session_id = request.session_hash if request else None

    with langfuse.start_as_current_observation(
        as_type="span",
        name="answer-question",
        input=question,
    ) as root_span:
        with propagate_attributes(
            trace_name="answer-question",
            session_id=session_id,
            tags=["rag-chat"],
        ):
            chunks = get_retriever().invoke(
                question,
                config={
                    "callbacks": [langfuse_handler],
                    "run_name": "retrieve-context",
                    "metadata": {"index": "ai-engineering-jobs"},
                },
            )
            documents = load_parent_documents(chunks)
            context = "\n\n".join(
                f"Source: {source}\n{text}" for source, text in documents.items()
            )
            system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)

            # The LLM returns a JobAnswer object instead of plain text
            response = (
                get_llm()
                .with_structured_output(JobAnswer)
                .invoke(
                    [
                        SystemMessage(content=system_prompt),
                        HumanMessage(content=question),
                    ],
                    config={
                        "callbacks": [langfuse_handler],
                        "run_name": "generate-answer",
                    },
                )
            )

        reply = f"{response.answer}\n\n{render_job_cards(response.jobs, documents)}"
        root_span.update(
            output=reply,
            metadata={
                "retrieved_chunks": len(chunks),
                "retrieved_documents": len(documents),
            },
        )
        return reply


def create_app() -> gr.ChatInterface:
    return gr.ChatInterface(
        fn=answer_question,
        title="AI Engineering Jobs RAG",
        description="Ask questions about the AI engineering job postings.",
    )


if __name__ == "__main__":
    create_app().launch(css=JOB_CARD_CSS)
