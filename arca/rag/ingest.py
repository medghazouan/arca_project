# loads, chunks, embeds documentsimport os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

POLICIES_DIR = "../data/policies"
VECTOR_DIR = "../vectorstore/index"

def load_documents():
    docs = []
    for file in os.listdir(POLICIES_DIR):
        if file.endswith(".md"):
            path = os.path.join(POLICIES_DIR, file)
            loader = TextLoader(path, encoding="utf-8")
            docs.extend(loader.load())
    return docs

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    return splitter.split_documents(docs)

def embed_and_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTOR_DIR)

    print("✅ Vectorstore created successfully using Sentence Transformers!")

if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    embed_and_store(chunks)
