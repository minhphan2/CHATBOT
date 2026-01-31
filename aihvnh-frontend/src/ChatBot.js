import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

function ChatBot() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [displayedAnswer, setDisplayedAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const answerRef = useRef(null);

  // Hiệu ứng typing từng ký tự
  useEffect(() => {
    if (!answer) {
      setDisplayedAnswer("");
      return;
    }
    let i = 0;
    setDisplayedAnswer("");
    const interval = setInterval(() => {
      setDisplayedAnswer(prev => prev + answer[i]);
      i++;
      if (i >= answer.length) clearInterval(interval);
    }, 18); // tốc độ gõ, càng nhỏ càng nhanh
    return () => clearInterval(interval);
  }, [answer]);

  // Tự động cuộn xuống khi có câu trả lời mới
  useEffect(() => {
    if (answerRef.current) {
      answerRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [displayedAnswer]);

  const handleAsk = async () => {
    if (!question) return;
    setLoading(true);
    setAnswer("");
    setDisplayedAnswer("");
    try {
      const res = await axios.post("http://localhost:8001/chat/", { question });
      setAnswer(res.data.answer);
    } catch {
      setAnswer("Lỗi kết nối server chatbot!");
    }
    setLoading(false);
  };

  return (
    <div
      style={{
        border: "1px solid #1976d2",
        padding: 24,
        borderRadius: 16,
        background: "#f7faff",
        boxShadow: "0 2px 8px #0001",
        marginTop: 20,
      }}
    >
      <h2 style={{ color: "#1976d2", marginBottom: 16, fontWeight: 700 }}>Chatbot HVNH</h2>
      <textarea
        rows={3}
        value={question}
        onChange={e => setQuestion(e.target.value)}
        style={{
          width: "100%",
          borderRadius: 8,
          border: "1px solid #bbb",
          padding: 10,
          fontSize: 16,
          resize: "vertical",
          marginBottom: 12,
        }}
        placeholder="Nhập câu hỏi..."
        disabled={loading}
      />
      <br />
      <button
        onClick={handleAsk}
        disabled={loading || !question}
        style={{
          background: "#1976d2",
          color: "#fff",
          border: "none",
          borderRadius: 8,
          padding: "8px 24px",
          fontSize: 16,
          cursor: loading || !question ? "not-allowed" : "pointer",
          fontWeight: 600,
          boxShadow: "0 1px 4px #0001",
        }}
      >
        {loading ? "Đang trả lời..." : "Hỏi"}
      </button>
      <div
        ref={answerRef}
        style={{
          marginTop: 28,
          minHeight: 32,
          background: "#fff",
          borderRadius: 8,
          padding: displayedAnswer ? "16px" : "0",
          color: "#222",
          fontSize: 17,
          whiteSpace: "pre-line",
          boxShadow: displayedAnswer ? "0 1px 4px #0001" : "none",
          transition: "all 0.2s",
        }}
      >
        {displayedAnswer}
        {loading && <span className="blinking-cursor">|</span>}
      </div>
    </div>
  );
}

export default ChatBot;