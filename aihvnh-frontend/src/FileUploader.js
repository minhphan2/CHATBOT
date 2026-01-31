import React, { useState } from "react";
import axios from "axios";

function FileUploader() {
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) {
      setMsg("Hãy chọn một file!");
      return;
    }
    setLoading(true);
    setMsg("");
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await axios.post("http://localhost:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      if (res.data.status === "success") {
        setMsg("Nạp file thành công!");
      } else {
        setMsg("Lỗi: " + res.data.detail);
      }
    } catch (err) {
      setMsg("Không kết nối được tới server!");
    }
    setLoading(false);
  };

  return (
    <div style={{ border: "1px solid #ccc", padding: 20, borderRadius: 8, marginBottom: 30 }}>
      <h2>Nạp tài liệu vào Milvus</h2>
      <input type="file" onChange={handleFileChange} />
      <br /><br />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Đang nạp..." : "Nạp file"}
      </button>
      <div style={{ marginTop: 20, color: msg.startsWith("Lỗi") ? "red" : "green" }}>{msg}</div>
    </div>
  );
}

export default FileUploader;