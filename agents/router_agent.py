import json
from llm.llm_client import LLMClient
from pathlib import Path

class RouterAgent:
    def __init__(self):
        self.llm_client = LLMClient()
        self.prompt_template = Path("llm/prompt_templates/router_prompt.txt"
                                    ).read_text(encoding="utf-8")
        

    def route(self,query: str)-> dict:
        prompt = self.prompt_template.replace("{{question}}", query)
        messages = [
            {
                "role": "system",
                "content": "You are a routing agent for a university AI assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        response = self.llm_client.generate(messages)

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "domains": ["document"],
                "need_aggregation": False
            }
