
from llm.llm_client import LLMClient
from pathlib import Path
from mcp.mcp_core import MCP


class ScholarshipAgent:
    def __init__(self, config_path: str):
        self.llm_client = LLMClient()
        self.mcp = MCP()
        self.prompt_template = Path("llm/prompt_templates/scholarship_prompt.txt"
                                    ).read_text(encoding="utf-8")
        

    def answer(self, question: str) -> str:
        query_vector = self.llm_client.get_embedding(question)
        context = "\n".join(self.mcp.query_vector_db(query_vector, domain="scholarship"))
        external = self.mcp.query_external(question, domain="scholarship")
        full_context = context + "\n" + external if external else context
        prompt = self.prompt_template.replace("{{context}}", full_context).replace("{{question}}", question)
        messages = [
            {"role": "system", "content": "Bạn là agent về học bổng của học viện ngân hàng"},
            {"role": "user", "content": prompt}
        ]
        return self.llm_client.generate(messages)