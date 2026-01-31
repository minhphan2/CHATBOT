from pymilvus import connections, Collection

connections.connect(host="localhost", port="19530")
collection = Collection("hvnh_documents")
collection.load()
results = collection.query(expr="id >= 0", output_fields=["content", "domain", "source"], limit=5)
for i, doc in enumerate(results, 1):
    print(f"--- Document {i} ---")
    print("Domain:", doc.get("domain"))
    print("Source:", doc.get("source"))
    print("Content:", doc.get("content")[:200], "...")
    print()