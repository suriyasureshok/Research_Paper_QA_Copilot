from ..data_ingestion.store_data import DataStore

if __name__ == "__main__":
    datastore = DataStore()
    print(datastore.get_all_chunks())