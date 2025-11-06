import { Routes, Route, Link } from "react-router-dom";
import KnowledgeUploadPage from "./chatbot/pages/KnowledgeUploadPage";
import ChatBot from "./chatbot/pages/ChatBot";
import "./App.css";
import JournalEntryPage from "./journal/pages/JournalEntryPage";
import JournalDashboardsPage from "./journal/pages/JournalDashboardsPage";

// Navbar component
function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="logo">
        MyApp
      </Link>
    </nav>
  );
}

// Reusable DashboardCard component
function DashboardCard({ title, to }) {
  return (
    <Link to={to} className="dashboard-card">
      <h3>{title}</h3>
    </Link>
  );
}

// Main dashboard page
function MainPage() {
  return (
    <div className="main-page">
      <h1>Main Dashboard</h1>
      <div className="cards-container">
        <DashboardCard title="Chatbot" to="/chatbot" />
        <DashboardCard title="Journal Entries" to="/journal-entries" />
        <DashboardCard title="Knowledge Upload" to="/knowledge-upload" />
      </div>
    </div>
  );
}

// Layout component to wrap all pages with Navbar
function Layout({ children }) {
  return (
    <div>
      <Navbar />
      <div className="page-content">{children}</div>
    </div>
  );
}

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/chatbot" element={<ChatBot />} />
        <Route path="/journal-entries" element={<JournalEntryPage />} />
        <Route path="/journal-dashboard" element={<JournalDashboardsPage />} />
        <Route path="/knowledge-upload" element={<KnowledgeUploadPage />} />
      </Routes>
    </Layout>
  );
}
