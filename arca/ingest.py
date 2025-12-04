# ingest.py
"""
ARCA Phase 1: Data Ingestion Pipeline
Loads, chunks, and embeds internal policy documents

TSD Requirements:
- Chunk size: 400 tokens
- Overlap: 50 tokens
- Model: all-MiniLM-L6-v2
- Storage: FAISS vectorstore
"""

import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Configuration (TSD Section 1.2)
POLICIES_DIR = "./data/policies"
VECTOR_DIR = "./vectorstore"

def load_documents():
    """
    Load all .md policy documents from the data/policies directory
    """
    docs = []
    if not os.path.exists(POLICIES_DIR):
        raise FileNotFoundError(f"❌ Policies directory not found: {POLICIES_DIR}")
    
    files = [f for f in os.listdir(POLICIES_DIR) if f.endswith(".md")]
    
    if not files:
        raise ValueError(f"❌ No .md files found in {POLICIES_DIR}")
    
    print(f"📂 Loading {len(files)} policy documents...")
    
    for file in files:
        path = os.path.join(POLICIES_DIR, file)
        try:
            loader = TextLoader(path, encoding="utf-8")
            loaded = loader.load()
            # Add source metadata
            for doc in loaded:
                doc.metadata["source"] = file
            docs.extend(loaded)
            print(f"   ✅ Loaded: {file}")
        except Exception as e:
            print(f"   ⚠️  Failed to load {file}: {e}")
    
    return docs

def chunk_documents(docs):
    """
    Split documents into chunks according to TSD specifications
    
    TSD Section 1.2:
    - chunk_size: 400 tokens
    - chunk_overlap: 50 tokens
    - Method: RecursiveCharacterTextSplitter
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,      # TSD requirement
        chunk_overlap=50,    # TSD requirement
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = splitter.split_documents(docs)
    print(f"✂️  Created {len(chunks)} chunks (400 tokens, 50 overlap)")
    
    return chunks

def embed_and_store(chunks):
    """
    Generate embeddings and store in FAISS vectorstore
    
    TSD Section 1.2:
    - Model: all-MiniLM-L6-v2 (Sentence Transformers)
    - Storage: FAISS
    """
    print("🧠 Generating embeddings with all-MiniLM-L6-v2...")
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("💾 Creating FAISS vectorstore...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Create directory if it doesn't exist
    os.makedirs(VECTOR_DIR, exist_ok=True)
    
    vectorstore.save_local(VECTOR_DIR)
    
    print(f"✅ Vectorstore created successfully!")
    print(f"   Location: {VECTOR_DIR}")
    print(f"   Total vectors: {vectorstore.index.ntotal}")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 ARCA PHASE 1: DATA INGESTION")
    print("=" * 60)
    
    try:
        # Step 1: Load documents
        docs = load_documents()
        print(f"📄 Total documents loaded: {len(docs)}")
        
        # Step 2: Chunk documents
        chunks = chunk_documents(docs)
        
        # Step 3: Embed and store
        embed_and_store(chunks)
        
        print("\n" + "=" * 60)
        print("✅ INGESTION COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ INGESTION FAILED: {e}")
        raise