import google.generativeai as genai
from src.data_ingestion.store_data import DataStore
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

class GeminiQAHandler:
    def __init__(self, api_key, datastore):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        self.datastore = datastore

    def answer_question(self, question, limit=5):
        # Search for relevant chunks
        results = self.datastore.search_chunks(question, limit=limit)
        if not results:
            return "No relevant information found in the database."
        
        # Build context from top chunks
        context = "\n\n".join([f"Chunk {i+1}: {chunk}" for i, (chunk, score) in enumerate(results)])
        
        # Create prompt
        prompt = f"""Based on the following context from research papers, answer the question accurately and concisely. If the context doesn't contain enough information, say so.

Question: {question}

Context:
{context}

Answer:"""
        
        # Generate response
        response = self.model.generate_content(prompt)
        return response.text
