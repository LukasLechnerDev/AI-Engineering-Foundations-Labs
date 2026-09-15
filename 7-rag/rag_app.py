from functools import lru_cache
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

MODEL = "gpt-5.6-luna"
EMBEDDING_MODEL = "text-embedding-3-large"

RAG_DIRECTORY = Path(__file__).resolve().parent
VECTOR_DB_PATH = RAG_DIRECTORY / "vector_db"
PROJECT_ROOT = RAG_DIRECTORY.parent

load_dotenv(PROJECT_ROOT / ".env", override=True)

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
    return vectorstore.as_retriever()


@lru_cache
def get_llm():
    """Create the language model once and reuse it for later questions."""
    return ChatOpenAI(temperature=0, model=MODEL, reasoning_effort="none")


def answer_question(question: str, history=None) -> str:
    """Answer one question using the local vector database."""
    documents = get_retriever().invoke(question)
    context = "\n\n".join(document.page_content for document in documents)
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)

    response = get_llm().invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=question)]
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
