from ..data_ingestion.paper_collector import ArxivPaperCollection
from ..data_ingestion.text_chunker import TextChunker
from ..data_ingestion.store_data import DataStore

if __name__ == "__main__":
    query = "transformer"
    collector = ArxivPaperCollection(query, max_results=5)
    papers = collector.fetch_papers()
    
    chunker = TextChunker(method='statistical')
    store = DataStore()
    
    for idx, paper in enumerate(papers):
        print(f"Paper {idx + 1}:")
        print(f"Title: {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Published: {paper['published']}")
        print(f"Link: {paper['link']}")
        print(f"PDF Link: {paper['pdf_link']}")
        print(f"Full Text (first 200 chars): {paper['full_text'][:200]}...")  # Print first 200 characters of full text
        print("\n" + "-"*80 + "\n")
        
        # Chunk and store the full text
        chunks = chunker.chunk_text(paper['full_text'])
        store.add_chunks(chunks)
        print(f"Stored {len(chunks)} chunks for paper {idx + 1}")
    
    # Optionally, retrieve and print all stored chunks
    all_chunks = store.get_all_chunks()
    print(f"Total chunks stored: {len(all_chunks)}")