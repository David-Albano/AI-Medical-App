import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles/GuidelinesUploadPage.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function GuidelinesUploadPage() {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFiles(e.target.files);
  };


  const handleUpload = async () => {
    if (!files.length) {
      alert("Please select at least one file.");
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

    try {
      const res = await axios.post(`${API_BASE_URL}/guidelines/upload-guideline/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setResult(res.data);
      console.log('res.data: ', res.data)
      
      // Reset the form after successful upload
      setFiles([]);
      document.querySelector('input[type="file"]').value = null; // clear file input
      
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || "Upload failed.");

    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-page">
      <h2>Upload Guidelines Files</h2>

      <div className="file-upload-container">

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
