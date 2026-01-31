from pymilvus import Collection

def create_index(collection_name: str, field_name: str = "embedding"):
    collection = Collection(collection_name)
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 128}
    }
    collection.create_index(field_name=field_name, index_params=index_params)

def drop_index(collection_name: str, field_name: str = "embedding"):

    collection = Collection(collection_name)
    collection.drop_index(field_name=field_name)