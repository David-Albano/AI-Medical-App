// src/App.jsx
import { Routes, Route, Link } from "react-router-dom";
import KnowledgeUploadPage from "./chatbot/pages/KnowledgeUploadPage";

function MainPage() {
  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Main Dashboard</h1>
      <div style={{ display: "flex", justifyContent: "center", gap: "20px", marginTop: "30px" }}>
        {/* Future apps here */}
        <Link to="/knowledge-upload">
          <div style={{
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "20px",
            width: "200px",
            cursor: "pointer",
            backgroundColor: "#f5f5f5",
          }}>
            <h3>Knowledge Upload</h3>
            <p>Go to chatbot</p>
          </div>
        </Link>
      </div>
    </div>
  );
}

export default function App() {
  return (
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/knowledge-upload" element={<KnowledgeUploadPage />} />
      </Routes>
      
  );
}
