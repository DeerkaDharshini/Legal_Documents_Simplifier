import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import Navbar from "../components/Navbar";
import UploadBox from "../components/UploadBox";
import TextInput from "../components/TextInput";
import Loader from "../components/Loader";
import Footer from "../components/Footer";

const API_BASE = "http://127.0.0.1:8000";

function Analyzer() {
  const navigate = useNavigate();
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyze = async () => {
    setError("");

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
        res = await axios.post(`${API_BASE}/upload/`, formData);
      } else {
        res = await axios.post(`${API_BASE}/simplify/`, { text });
      }

      navigate("/results", {
        state: {
          simplified: res.data.simplified_text,
          tamil: res.data.tamil_text,
          audio: res.data.audio_url,
        },
      });
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
        <h1>Analyze Legal Document</h1>

        <UploadBox setFile={setFile} />

        <p>OR</p>

        <TextInput text={text} setText={setText} />

        {error && <div className="error-message">{error}</div>}

        <button onClick={analyze} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Document"}
        </button>
      </section>

      {loading && <Loader />}

      <Footer />
    </div>
  );
}

export default Analyzer;