import chromadb
import uuid
from data_models import MemoryNode

class MemoryStore:
    def __init__(self, path: str = "./chroma_data"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name="mistakes",
            metadata={"hnsw:space": "cosine"}
        )

    def add(self, node: MemoryNode, code_pair_id: str = None):
        """Store a memory node."""
        doc = node.model_dump()
        
        # ChromaDB hates empty lists
        if not doc.get("tags"):
            doc["tags"] = ["general"]
        
        # Use a proper UUID string to avoid negative hash collisions
        if code_pair_id is None:
            code_pair_id = str(uuid.uuid4())
        
        self.collection.add(
            documents=[node.divergence_point],
            metadatas=[doc],
            ids=[code_pair_id]
        )

    def search_similar(self, query_text: str, n: int = 5):
        """Find past mistakes with similar divergence patterns."""
        return self.collection.query(
            query_texts=[query_text],
            n_results=n
        )

    def count(self):
        return self.collection.count()

store = MemoryStore()