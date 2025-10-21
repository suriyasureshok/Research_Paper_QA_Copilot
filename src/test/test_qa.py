from ..chat.gemini_client import GeminiQAHandler
import os

if __name__ == "__main__":
    # Set your Gemini API key here or via environment variable
    api_key = os.getenv("GEMINI_API_KEY")  # Replace with your actual key or set env var
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable.")
        exit(1)
    
    handler = GeminiQAHandler(api_key)
    
    question = "What are the advantages of Transformer models?"
    answer = handler.answer_question(question)
    
    print(f"Question: {question}")
    print(f"Answer: {answer}")