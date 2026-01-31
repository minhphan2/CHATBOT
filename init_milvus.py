from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType

connections.connect(host="localhost", port="19530")
try:
    Collection("hvnh_documents").drop()
    print("Đã xóa collection cũ.")
except Exception as e:
    print("Collection chưa tồn tại hoặc đã xóa.")

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384), 
    FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=2048),
    FieldSchema(name="domain", dtype=DataType.VARCHAR, max_length=64),
    FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=256)
]
schema = CollectionSchema(fields, description="HVNH documents")
collection = Collection("hvnh_documents", schema=schema)
collection.create_index(field_name="embedding", index_params={
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 128}
})
collection.load()
print("Milvus collection and index created!")