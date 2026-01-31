from pymilvus import Collection, connections
from typing import List


class MilvusService:
    def __init__(self):
        connections.connect(
            alias="default",
            host="localhost",
            port="19530"
        )

        self.collection = Collection("hvnh_documents")
        self.collection.load()

    def search(
        self,
        query_vector: List[float],
        domain: str,
        top_k: int = 5
    ) -> List[str]:

        expr = f'domain == "{domain}"'

        search_results = self.collection.search(
            data=[query_vector],
            anns_field="embedding",
            param={"metric_type": "L2", "params": {"nprobe": 10}},
            limit=top_k,
            expr=expr,
            output_fields=["content", "source"]
        )

        documents = []
        for hits in search_results:
            for hit in hits:
                content = hit.entity.get("content")
                if content:
                    documents.append(content)

        if not documents:
            return ["Không tìm thấy dữ liệu liên quan trong hệ thống."]

        return documents
