import React from "react";
import FileUpload from "../components/FileUpload";
import "../styles/upload.css";

export default function KnowledgeUploadPage() {
  return (
    <div className="upload-page">
      <h2>Upload Knowledge Files</h2>
      <p>Select one or more files to upload and embed into the knowledge base.</p>
      <FileUpload />
    </div>
  );
}