import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import "../styles/ChatBot.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function ChatBot() {
  const [categories, setCategories] = useState([]);
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const chatHistoryRef = useRef(null); // <-- Add ref here

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/chatbot/get-medical-categories/`)
      .then((res) => setCategories(res.data.medical_categories))
      .catch((err) => console.error("Error fetching categories:", err));
  }, []);

  useEffect(() => {
    // Scroll to the bottom whenever chatHistory changes
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [chatHistory]);

  const handleCategoryChange = (e) => {
    const options = Array.from(e.target.selectedOptions, (option) => option.value);
    setSelectedCategories(options);
  };

  const handleSendMessage = async () => {
    if (!message) return;

    const userMessage = { role: "user", content: message };
    setChatHistory((prev) => [...prev, userMessage]);
    setMessage("");
    setLoading(true);

    const categoriesForPost = selectedCategories.map((categoryPk) => Number(categoryPk));

    try {
      const res = await axios.post(`${API_BASE_URL}/chatbot/chat/`, {
        message,
        knowledge_categories: categoriesForPost,
      });

      const botMessage = { role: "assistant", content: res.data.answer };
      setChatHistory((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error("Error sending message:", err);
      const errorMessage = { role: "assistant", content: "Error: Could not get response." };
      setChatHistory((prev) => [...prev, errorMessage]);
    }

    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chatbot">
      <aside>
        <div className="sidebar">
            <h2>Medical Categories</h2>
            <p className="guide-info">
            Pick one or multiple categories to guide the assistant and receive more accurate, topic-focused answers.
            </p>
            <select multiple value={selectedCategories} onChange={handleCategoryChange}>
            {categories.map((category) => (
                <option key={category.id} value={category.id}>
                {category.name}
                </option>
            ))}
            </select>
            <p className="selection-guide-info">
                Hold <strong>Ctrl</strong> (Windows) or <strong>Cmd</strong> (Mac) while clicking to select multiple options.
            </p>
        </div>
      </aside>

      <main className="chat-container">
        <div className="chat-header">
          <h2>Medical Chat Assistant</h2>
          <p className="guide-info">
            Ask your medical questions below. Press "Enter" to send or Shift+Enter for a new line.
          </p>
        </div>

        <div className="chat-history" ref={chatHistoryRef}>
            {chatHistory.map((msg, index) => (
                <div
                key={index}
                className={`chat-message ${msg.role === "user" ? "user" : "assistant"}`}
                >
                <span>{msg.content}</span>
                </div>
            ))}
            {loading && <div className="chat-message assistant typing">Typing</div>}
        </div>

        <div className="chat-input">
          <textarea
            placeholder="Type your message here..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button onClick={handleSendMessage}>Send</button>
        </div>
      </main>
    </div>
  );
}

export default ChatBot;
