from typing import Dict, List, Optional
import chromadb
from chromadb.config import Settings
import os
from dotenv import load_dotenv

load_dotenv()

class ResearchMemory:
    def __init__(self):
        self.persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma")
        self.client = chromadb.Client(Settings(
            persist_directory=self.persist_dir,
            is_persistent=True
        ))
        self.collection = self.client.get_or_create_collection(
            name="research_results",
            metadata={"hnsw:space": "cosine"}
        )
    
    def store_research_result(self, 
                            query: str, 
                            results: List[Dict], 
                            metadata: Optional[Dict] = None) -> str:
        """
        Store research results in the vector store
        """
        # Convert results to a string format for storage
        content = str(results)
        
        # Generate a unique ID for this research result
        doc_id = f"research_{hash(query + content)}"
        
        # Store in ChromaDB
        self.collection.add(
            documents=[content],
            ids=[doc_id],
            metadatas=[metadata or {}]
        )
        
        return doc_id
    
    def retrieve_similar_research(self, 
                                query: str, 
                                n_results: int = 3) -> List[Dict]:
        """
        Retrieve similar research results based on query
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return [
            {
                "content": doc,
                "metadata": meta,
                "id": id
            }
            for doc, meta, id in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["ids"][0]
            )
        ]
    
    def clear_memory(self):
        """
        Clear all stored research results
        """
        self.collection.delete(where={}) 