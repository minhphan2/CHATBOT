from mcp.milvus_service import MilvusService
from mcp.external_service import ExternalService
from mcp.logging_service import LoggingService

class MCP:
    def __init__(self):
        self.milvus_service = MilvusService()
        self.external_service = ExternalService()
        self.logging_service = LoggingService()


    def query_vector_db(self, 
                        query_vector:list[float],
                        domain:str,
                        top_k:int=5
    )->list[str]:
        
        self.logging_service.log(
            f"Query Milvus | domain={domain} | top_k={top_k}"
        )


        results = self.milvus_service.search(
            query_vector=query_vector,
            domain=domain,
            top_k=top_k
        )

        return results
    


    def query_external(self,
                        query_text:str,
                        domain:str
    )->str:
        
        self.logging_service.log(
            f"Query External Service | domain={domain}"
        )


        result = self.external_service.search(
            query_text=query_text,
            domain=domain
        )

        return result