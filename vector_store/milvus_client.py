from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType

class MilvusClient:
    def __init__(self, host="localhost", port= "19530", collection_name="hvnh_documents"):
        self.collection_name = collection_name
        connections.connect(alias="default", host=host, port=port)
        self.collection = Collection(self.collection_name)

    def insert(self, embeddings, contents, domains, sources):
        data = [      
            embeddings,
            contents,
            domains,
            sources
        ]
        self.collection.insert(data)

    def search(self, query_vector, top_k =5, expr=None):
        results = self.collection.search(
            data=[query_vector],
            anns_field="embedding",
            param={"metric_type": "L2", "params": {"nprobe": 10}},
            limit=top_k,
            expr=expr,
            output_fields=["metadata"]
        )
        return results
        
    def create_index(self):
        self.collection.create_index(
            field_name="embedding",
            index_params={
                "index_type": "IVF_FLAT",
                "metric_type": "L2",
                "params": {"nlist": 128}
            }
        )

    def load_collection(self):
        self.collection.load()    