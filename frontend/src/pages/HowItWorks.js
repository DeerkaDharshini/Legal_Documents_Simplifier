import React from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

function HowItWorks() {
  return (
    <div>
      <Navbar />

      <section className="how-section">
        <h1>How It Works</h1>

        <ol className="steps-list">
          <li>Upload a legal document (PDF, DOCX, or TXT) or paste text</li>
          <li>AI processes the document using Google Gemini language model</li>
          <li>Complex legal text is simplified into plain English</li>
          <li>Tamil translation is generated using Google Gemini</li>
          <li>Audio explanation is created for accessibility</li>
          <li>Risk analysis identifies potential legal risks</li>
        </ol>
      </section>

      <Footer />
    </div>
  );
}

export default HowItWorks;