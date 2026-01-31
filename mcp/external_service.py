import requests
import os
from crawler.crawler_core import crawl_hvnh_sites


class ExternalService:
    def __init__(self):
        self.allowed_domains = ["hvnh.edu.vn"]

        self.domain_keywords = {
            "course": "môn học học viện ngân hàng",
            "scholarship": "học bổng học viện ngân hàng"
        }

    def search(self, query_text: str, domain: str) -> str:
        crawled_text = crawl_hvnh_sites(query_text)
        if crawled_text:
            return crawled_text

        subscription_key = os.getenv("BING_API_KEY")
        if not subscription_key:
            return ""

        search_url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}

        keyword = self.domain_keywords.get(domain, domain)
        params = {"q": f"{query_text} {keyword}", "count": 5}

        try:
            response = requests.get(
                search_url,
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()

            search_results = response.json()
            results = []

            for item in search_results.get("webPages", {}).get("value", []):
                url = item.get("displayUrl", "")
                name = item.get("name", "")
                if any(d in url for d in self.allowed_domains):
                    results.append(f"{name}\n{url}")

            return "\n\n".join(results) if results else ""

        except Exception:
            return ""
