from ingestion.digitize import extract_pdf, extract_docx, ocr_image
from ingestion.clean_text import clean_text
from ingestion.chunking import chunk_text
from ingestion.embedding import get_embeddings
from vector_store.milvus_client import MilvusClient
import os

def ingest_file(file_path, domain="course", source=None):
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

    # Insert từng chunk vào Milvus
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        ids = [None]  # auto_id
        embeddings_list = [embedding]
        metadatas = [{
            "content": chunk,
            "domain": domain,
            "source": source or file_path
        }]
        milvus.insert(ids, embeddings_list, metadatas)
    print(f"Đã nạp {len(chunks)} đoạn vào Milvus.")

if __name__ == "__main__":
    # Ví dụ: thay đường dẫn file và domain cho phù hợp
    ingest_file(r"D:\Desktop\AIHVNH\data\sample.pdf", domain="course")