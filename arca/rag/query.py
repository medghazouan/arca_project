# rag/query.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_DIR = "../vectorstore/index"

def test_query():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # load the saved FAISS index (make sure VECTOR_DIR exists and contains the index)
    db = FAISS.load_local(
        VECTOR_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )

    query = "What is our data retention rule?"
    results = db.similarity_search(query, k=5)

    for r in results:
        print("-----")
        print(r.page_content[:1000])  # print a chunk (trim if too long)

if __name__ == "__main__":
    test_query()
