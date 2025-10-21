from ..data_ingestion.store_data import DataStore

if __name__ == "__main__":
    datastore = DataStore()
    
    # Example query
    query = "transformer architecture"
    results = datastore.search_chunks(query, limit=3)
    
    print(f"Search results for query: '{query}'")
    for idx, (chunk, score) in enumerate(results):
        print(f"Result {idx + 1} (Score: {score:.4f}): {chunk[:200]}...")