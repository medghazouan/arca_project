# agents/policy_researcher.py
"""
Agent 1: Policy Researcher (ARCA System)
- Pure retrieval agent using FAISS + HuggingFace embeddings
- Compliant with TSD requirements: Top 5 excerpts with IDs
- Input: query (str)
- Output: dict with query, items (list of dicts), concatenated_excerpts (str)
"""

import os
from pathlib import Path
from typing import List, Dict, Any
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# CONFIG - Fixed path resolution
# Get the directory where THIS file is located (agents/)
CURRENT_FILE_DIR = Path(__file__).parent
# Go up one level to get project root (arca/)
PROJECT_ROOT = CURRENT_FILE_DIR.parent
# Build absolute path to vectorstore
DEFAULT_VECTOR_DIR = str(PROJECT_ROOT / "vectorstore")

VECTOR_DIR = os.getenv("ARCA_VECTOR_DIR", DEFAULT_VECTOR_DIR)
EMBEDDING_MODEL = os.getenv("ARCA_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
TOP_K = 5


class PolicyResearcherAgent:
    def __init__(self, vector_dir: str = VECTOR_DIR, embedding_model: str = EMBEDDING_MODEL):
        """
        Initialize the Policy Researcher Agent.
        Loads FAISS vectorstore created by ingest.py
        """
        self.vector_dir = vector_dir
        self.embedding_model = embedding_model
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        
        # Load FAISS DB (must match ingest.py output)
        try:
            self.db = FAISS.load_local(
                self.vector_dir, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
            print(f"✅ Policy Researcher initialized with {self.db.index.ntotal} policy chunks")
        except Exception as e:
            raise RuntimeError(f"❌ Failed to load vectorstore from {self.vector_dir}: {e}")

    def vector_db_search(self, query: str, k: int = TOP_K) -> List[Dict[str, Any]]:
        """
        Core tool: vector_db_search
        Returns top-k most relevant policy excerpts with metadata
        
        TSD Specification:
        - Input: query (str)
        - Output: List of dicts with policy_id, excerpt, score, source
        """
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")

        # Retrieve top-k similar documents with scores
        results = self.db.similarity_search_with_score(query, k=k)

        formatted = []
        for i, (doc, score) in enumerate(results):
            metadata = doc.metadata or {}
            
            # Extract policy identifier (TSD requirement: policy_id)
            policy_id = metadata.get("source", f"policy_chunk_{i+1}")
            if policy_id.endswith(".md"):
                policy_id = policy_id[:-3]  # Remove .md extension
            
            formatted.append({
                "policy_id": policy_id,
                "excerpt": doc.page_content,
                "score": float(score),
                "source": metadata.get("source", "unknown"),
                "metadata": metadata
            })

        return formatted

    def run(self, query: str, k: int = TOP_K) -> Dict[str, Any]:
        """
        Main execution method for Agent 1.
        
        TSD Role: "Expert en recherche sémantique"
        TSD Objective: "Récupérer les Top 5 extraits les plus pertinents"
        
        Returns structured output for Agent 2 (Compliance Auditor)
        """
        if not query or not isinstance(query, str):
            raise ValueError("Query (str) is required")

        # Execute vector search
        items = self.vector_db_search(query, k=k)

        # Create concatenated excerpts for easy consumption
        concatenated_excerpts = "\n\n".join([
            f"[Policy ID: {it['policy_id']}]\n{it['excerpt']}" 
            for it in items
        ])

        return {
            "query": query,
            "items": items,
            "concatenated_excerpts": concatenated_excerpts,
            "total_results": len(items)
        }


def quick_test():
    """Test Agent 1 with sample query"""
    agent = PolicyResearcherAgent()
    query = "data retention period and client data deletion requirements"
    
    print("=" * 60)
    print("🔍 TESTING POLICY RESEARCHER AGENT")
    print("=" * 60)
    print(f"Query: {query}\n")
    
    result = agent.run(query, k=5)
    
    print(f"✅ Found {result['total_results']} relevant policies\n")
    
    for i, item in enumerate(result['items'], 1):
        print(f"[{i}] Policy ID: {item['policy_id']}")
        print(f"    Score: {item['score']:.4f}")
        print(f"    Excerpt: {item['excerpt'][:200]}...")
        print()


if __name__ == "__main__":
    quick_test()
