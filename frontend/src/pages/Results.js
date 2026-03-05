import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";
import ResultCard from "../components/ResultCard";
import AudioPlayer from "../components/AudioPlayer";
import Footer from "../components/Footer";

function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const { simplified, tamil, audio } = location.state || {};

  if (!simplified) {
    return (
      <div>
        <Navbar />
        <section className="analyzer">
          <h1>No Results Found</h1>
          <p>Please analyze a document first.</p>
          <button onClick={() => navigate("/analyzer")}>Go to Analyzer</button>
        </section>
        <Footer />
      </div>
    );
  }

  return (
    <div>
      <Navbar />

      <section className="results-section">
        <h1>Analysis Results</h1>

        <ResultCard title="Simplified English" text={simplified} />

        {tamil && <ResultCard title="Tamil Translation" text={tamil} />}

        <AudioPlayer audio={audio} />

        <div className="results-actions">
          <button onClick={() => navigate("/analyzer")}>Analyze Another</button>
          <button
            className="secondary-btn"
            onClick={() => navigate("/risk")}
          >
            Risk Analysis
          </button>
        </div>
      </section>

      <Footer />
    </div>
  );
}

export default Results;