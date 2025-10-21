from ..data_ingestion.text_chunker import TextChunker

if __name__ == "__main__":
    sample_text = """Transformers have revolutionized the field of natural language processing.
        They utilize self-attention mechanisms to capture long-range dependencies in text.
        This has led to significant improvements in various NLP tasks such as translation, summarization, and question answering. 
        The introduction of models like BERT and GPT has further pushed the boundaries of what is possible with machine learning in language understanding."""
    
    chunker = TextChunker(method='statistical')
    chunks = chunker.chunk_text(sample_text)
    
    print(f"Chunk: {chunks}\n")