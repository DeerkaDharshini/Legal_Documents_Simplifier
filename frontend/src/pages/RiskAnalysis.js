import React, { useState } from "react";
import axios from "axios";

import Navbar from "../components/Navbar";
import UploadBox from "../components/UploadBox";
import TextInput from "../components/TextInput";
import Loader from "../components/Loader";
import RiskCard from "../components/RiskCard";
import Footer from "../components/Footer";

const API_BASE = "http://127.0.0.1:8000";

function RiskAnalysis() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [risks, setRisks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [analyzed, setAnalyzed] = useState(false);

  const analyzeRisks = async () => {
    setError("");
    setRisks([]);
    setAnalyzed(false);

    if (!text && !file) {
      setError("Please enter text or upload a file before analyzing.");
      return;
    }

    setLoading(true);

    try {
      let res;

      if (file) {
        const formData = new FormData();
        formData.append("file", file);
        res = await axios.post(`${API_BASE}/risk-analysis/upload/`, formData);
      } else {
        res = await axios.post(`${API_BASE}/risk-analysis/`, { text });
      }

      setRisks(res.data.risks || []);
      setAnalyzed(true);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else if (err.message) {
        setError(`Connection error: ${err.message}`);
      } else {
        setError("An unexpected error occurred. Please try again.");
      }
    }

    setLoading(false);
  };

  return (
    <div>
      <Navbar />

      <section className="analyzer">
        <h1>Legal Risk Analysis</h1>
        <p className="section-subtitle">
          Upload a legal document or paste text to identify potential risks.
        </p>

        <UploadBox setFile={setFile} />

        <p>OR</p>

        <TextInput text={text} setText={setText} />

        {error && <div className="error-message">{error}</div>}

        <p></p>

        <button onClick={analyzeRisks} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Risks"}
        </button>
      </section>

      {loading && <Loader />}

      {analyzed && risks.length === 0 && (
        <div className="no-risks">
          <h2>No Risks Detected</h2>
          <p>No significant risks were found in the provided text.</p>
        </div>
      )}

      {risks.length > 0 && (
        <section className="risk-results">
          <h2>Identified Risks ({risks.length})</h2>
          {risks.map((risk, index) => (
            <RiskCard
              key={index}
              title={risk.title}
              level={risk.level}
              description={risk.description}
            />
          ))}
        </section>
      )}

      <Footer />
    </div>
  );
}

export default RiskAnalysis;