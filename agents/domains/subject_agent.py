
from llm.llm_client import LLMClient
from mcp.mcp_core import MCP
from pathlib import Path
import yaml


class SubjectAgent:
    def __init__(self, config_path: str):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        self.llm_client = LLMClient()
        self.mcp = MCP()
        self.prompt_template = Path("llm/prompt_templates/subject_prompt.txt"
                                    ).read_text(encoding="utf-8")
        
    def answer(self, question: str) -> str:
        query_vector = self.llm_client.get_embedding(question)
        context = "\n".join(self.mcp.query_vector_db(query_vector, domain="subject"))
        external = self.mcp.query_external(question, domain="subject")
        full_context = context + "\n" + external if external else context
        prompt = self.prompt_template.replace("{{context}}", full_context).replace("{{question}}", question)
        messages = [
            {"role": "system", "content": "Bạn là agent về môn học của học viện ngân hàng"},
            {"role": "user", "content": prompt}
        ]
        return self.llm_client.generate(messages)