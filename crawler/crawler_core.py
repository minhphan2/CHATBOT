import yaml
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

def load_sites(yaml_path="crawler/sites.yaml"):
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("sites", [])

def log_crawl(url, status, log_dir="crawler/craw_logs"):
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "crawl.log")
    with open(log_file, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {url} | {status}\n")

def crawl_hvnh_sites(query_text, yaml_path="crawler/sites.yaml"):
    sites = load_sites(yaml_path)
    results = []
    for url in sites:
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text(separator="\n")
            if query_text.lower() in text.lower():
                results.append(f"Thông tin tìm thấy tại {url}\n{text[:500]}...")
                log_crawl(url, "FOUND")
            else:
                log_crawl(url, "NO_MATCH")
        except Exception as e:
            log_crawl(url, f"ERROR: {e}")
    return "\n\n".join(results) if results else ""