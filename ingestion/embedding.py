from llm.llm_client import LLMClient

def get_embeddings(text_chunks: list[str]) -> list[list[float]]:
    """
    Sinh embedding cho từng đoạn văn bản (chunk).
    """
    llm = LLMClient()
    return [llm.get_embedding(chunk) for chunk in text_chunks]