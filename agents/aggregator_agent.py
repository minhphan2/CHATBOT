from llm.llm_client import LLMClient
from pathlib import Path

class AggregatorAgent:
    def __init__(self, agents: dict):

        self.agents = agents
        self.llm_client = LLMClient()
        self.prompt_template = Path("llm/prompt_templates/aggregator_prompt.txt"
                                    ).read_text(encoding="utf-8")
        

    def aggregate(self, question: str, domains: list[str]) -> str:
        results = {}

        for domain in domains:
            agent = self.agents.get(domain)
            if agent:
                results[domain] = agent.answer(question)

        context = "\n\n".join(
            f"{domain.upper()}:\n{answer}"
            for domain, answer in results.items()
        )

        prompt = (
            self.prompt_template
            .replace("{{context}}", context)
            .replace("{{question}}", question)
        )

        messages = [
            {
                "role": "system",
                "content": "You are an aggregation agent for a university AI assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        return self.llm_client.generate(messages)