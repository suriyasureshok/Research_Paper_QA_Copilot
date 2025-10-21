from semantic_router.encoders import HuggingFaceEncoder
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

encoder = HuggingFaceEncoder(model_name="sentence-transformers/all-MiniLM-L6-v2")

class DataStore:
    def __init__(self):
        self.client = QdrantClient(path="./qdrant_db")
        self.collection_name = "chunks"
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
        except ValueError:
            # Collection already exists
            pass
        self.id_counter = self.get_chunk_count()

    def add_chunks(self, chunks):
        points = []
        for chunk in chunks:
            try:
                vector = encoder(docs=[chunk])[0]
                point = PointStruct(id=self.id_counter, vector=vector, payload={"text": chunk})
                points.append(point)
                self.id_counter += 1
            except Exception as e:
                print(f"Error encoding chunk: {e}, skipping")
        if points:
            self.client.upsert(collection_name=self.collection_name, points=points)

    def get_all_chunks(self):
        scroll_result = self.client.scroll(collection_name=self.collection_name, limit=10000)
        return [point.payload["text"] for point in scroll_result[0]]

    def get_chunk_count(self):
        info = self.client.get_collection(collection_name=self.collection_name)
        return info.points_count

    def search_chunks(self, query, limit=5):
        query_vector = encoder(docs=[query])[0]
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        return [(hit.payload["text"], hit.score) for hit in search_result]