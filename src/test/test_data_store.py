from ..data_ingestion.store_data import DataStore

if __name__ == "__main__":
    datastore = DataStore()
    
    # Add some test chunks
    test_chunks = ["This is a test chunk.", "Another test chunk for verification."]
    datastore.add_chunks(test_chunks)
    
    # Get count
    count = datastore.get_chunk_count()
    print(f"Total chunks stored: {count}")
    
    # Retrieve and print chunks
    retrieved_chunks = datastore.get_all_chunks()
    
    for idx, chunk in enumerate(retrieved_chunks):
        print(f"Retrieved Chunk {idx + 1}: {chunk}\n")