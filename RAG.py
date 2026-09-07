import os
from dotenv import load_dotenv

load_dotenv()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


def create_vector_store(text):

    if isinstance(text, list):
        text = "\n\n".join(
            str(item) for item in text
        )

    elif not isinstance(text, str):
        text = str(text)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = text_splitter.split_text(text)

    vector_store = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        collection_name="research_chunks"
    )

    return vector_store


def retrieve_relevant_chunks(vector_store, query: str):

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 10,
            "lambda_mult": 0.5
        }
    )

    docs = retriever.invoke(query)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return context