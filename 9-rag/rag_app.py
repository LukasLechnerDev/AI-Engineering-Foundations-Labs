import os
from functools import lru_cache
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv

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

Context:
{context}
"""


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


def load_parent_documents(chunks: list[Document]) -> list[str]:
    """Load the whole document of every chunk (parent document retrieval)."""
    # dict.fromkeys removes duplicate paths but keeps the order
    sources = dict.fromkeys(chunk.metadata["source"] for chunk in chunks)
    # The paths are relative to the RAG directory, not to the current working directory
    return [(RAG_DIRECTORY / source).read_text() for source in sources]


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
            context = "\n\n".join(documents)
            system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)

            response = get_llm().invoke(
                [SystemMessage(content=system_prompt), HumanMessage(content=question)],
                config={
                    "callbacks": [langfuse_handler],
                    "run_name": "generate-answer",
                },
            )

        root_span.update(
            output=response.content,
            metadata={
                "retrieved_chunks": len(chunks),
                "retrieved_documents": len(documents),
            },
        )
        return response.content


def create_app() -> gr.ChatInterface:
    return gr.ChatInterface(
        fn=answer_question,
        title="AI Engineering Jobs RAG",
        description="Ask questions about the AI engineering job postings.",
    )


if __name__ == "__main__":
    create_app().launch()
