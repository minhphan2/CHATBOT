from ingestion.digitize import extract_pdf, extract_docx, ocr_image
from ingestion.clean_text import clean_text
from ingestion.chunking import chunk_text
from ingestion.embedding import get_embeddings
from vector_store.milvus_client import MilvusClient
from llm.llm_client import LLMClient
import os

def detect_domains(text: str) -> list[str]:
    llm = LLMClient()
    prompt = (
        "Các domain khả dụng: scholarship, subject, course.\n"
        "Văn bản sau thuộc những domain nào? Trả về danh sách domain, cách nhau bởi dấu phẩy, không giải thích.\n"
        f"Văn bản:\n{text[:1000]}"
    )
    messages = [
        {"role": "system", "content": "Bạn là AI phân loại domain tài liệu."},
        {"role": "user", "content": prompt}
    ]
    domains = llm.generate(messages).strip().lower()
    return [d.strip() for d in domains.split(",") if d.strip()]

def ingest_file(file_path, source=None):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        text = extract_pdf(file_path)
    elif ext == ".docx":
        text = extract_docx(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        text = ocr_image(file_path)
    else:
        with open(file_path, encoding="utf-8") as f:
            text = f.read()

    text = clean_text(text)
    chunks = chunk_text(text, max_length=512)
    embeddings = get_embeddings(chunks)

    milvus = MilvusClient()
    milvus.load_collection()


    domains = []
    for chunk in chunks:
        chunk_domains = detect_domains(chunk)
        domains.append(",".join(chunk_domains))  
    contents = chunks
    sources = [source or file_path] * len(chunks)
    milvus.insert(embeddings, contents, domains, sources)

    print(f"Đã nạp {len(chunks)} đoạn vào Milvus với các domain liên quan.")