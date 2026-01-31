from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ingestion.ingest_file import ingest_file
import os
import shutil

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        ingest_file(temp_path)
        os.remove(temp_path)
        return {"status": "success", "filename": file.filename}
    except Exception as e:
        os.remove(temp_path)
        return {"status": "error", "detail": str(e)}