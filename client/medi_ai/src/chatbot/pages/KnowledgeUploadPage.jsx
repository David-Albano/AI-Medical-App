import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles/upload.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function KnowledgeUploadPage() {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const [medicalCategories, setMedicalCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("");

  // Fetch medical categories on mount
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await axios.get(`${API_BASE_URL}/chatbot/get-medical-categories/`);
        setMedicalCategories(res.data.medical_categories || []);
      } catch (err) {
        console.error("Failed to fetch categories:", err);
        setError("Could not load medical categories.");
      }
    };
    fetchCategories();
  }, []);

  const handleFileChange = (e) => {
    setFiles(e.target.files);
  };

  const handleCategoryChange = (e) => {
    setSelectedCategory(Number(e.target.value));
  };

  const handleUpload = async () => {
    if (!files.length) {
      alert("Please select at least one file.");
      return;
    }

    if (!selectedCategory) {
      alert("Please select a medical category.");
      return;
    }

    setUploading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();

    // Add files
    for (let file of files) {
      formData.append("files", file);
    }

    // Add selected category (single value)
    formData.append("medical_category_pk", selectedCategory);

    try {
      const res = await axios.post(`${API_BASE_URL}/chatbot/upload-knowledge/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setResult(res.data);
      
      // Reset the form after successful upload
      setFiles([]);
      setSelectedCategory("");
      document.querySelector('input[type="file"]').value = null; // clear file inpu
      
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || "Upload failed.");

    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-page">
      <h2>Upload Knowledge Files</h2>
      <p>Select a file and assign it to one medical category.</p>

      <div className="file-upload-container">
        <div className="form-group">
          <label>Medical Category:</label>
          <select
            value={selectedCategory}
            onChange={handleCategoryChange}
            className="category-select"
          >
            <option value="">-- Select a category --</option>
            {medicalCategories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <input type="file" multiple onChange={handleFileChange} />
        </div>

        <button onClick={handleUpload} disabled={uploading}>
          {uploading ? "Uploading..." : "Upload"}
        </button>

        {error && <p className="error">{error}</p>}

        {result && (
          <div className="result">
            <h3>Upload Summary</h3>
            <p>Total Chunks Created: {result.total_chunks}</p>
            <ul>
              {result.details.map((r, i) => (
                <li key={i}>
                  <strong>{r.file}:</strong>{" "}
                  {r.status === "no_text_found"
                    ? "No text found"
                    : `${r.chunks_created} chunks created`}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
