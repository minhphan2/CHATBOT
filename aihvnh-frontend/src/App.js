import React from "react";
import FileUploader from "./FileUploader";
import ChatBot from "./ChatBot";

function App() {
  return (
    <div style={{ maxWidth: 600, margin: "40px auto" }}>
      <FileUploader />
      <ChatBot />
    </div>
  );
}

export default App;