import { Routes, Route, Link } from "react-router-dom";
import KnowledgeUploadPage from "./chatbot/pages/KnowledgeUploadPage";
import ChatBot from "./chatbot/pages/ChatBot";
import "./App.css";

// Reusable DashboardCard component
function DashboardCard({ title, to }) {
  return (
    <Link to={to} className="dashboard-card">
      <h3>{title}</h3>
    </Link>
  );
}

function MainPage() {
  return (
    <div className="main-page">
      <h1>Main Dashboard</h1>
      <div className="cards-container">
        <DashboardCard title="Chatbot" to="/chatbot" />
        <DashboardCard title="Knowledge Upload" to="/knowledge-upload" />
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<MainPage />} />
      <Route path="/chatbot" element={<ChatBot />} />
      <Route path="/knowledge-upload" element={<KnowledgeUploadPage />} />
    </Routes>
  );
}
