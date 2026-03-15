import React from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

function HowItWorks() {
  return (
    <div>
      <Navbar />

      <section className="how-section">
        <h1>How It Works</h1>
        <p className="section-subtitle">
          Our AI processes legal documents step-by-step to make them easy to understand.
        </p>

        <div className="steps-container">

          <div className="step-card">
            <img
              src="https://images.unsplash.com/photo-1517842645767-c639042777db?w=800"
              alt="Upload document"
            />
            <div>
              <h3>1. Document Upload</h3>
              <p>Users upload legal documents like agreements, contracts, or policies to the system.</p>
            </div>
          </div>

          <div className="step-card">
            <img
              src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800"
              alt="Text extraction"
            />
            <div>
              <h3>2. Text Extraction</h3>
              <p>The system extracts readable text from the uploaded document for processing.</p>
            </div>
          </div>

          <div className="step-card">
            <img
              src="https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800"
              alt="AI processing"
            />
            <div>
              <h3>3. Content Processing</h3>
              <p>AI models analyze the document structure and identify important clauses.</p>
            </div>
          </div>

          <div className="step-card">
            <img
              src="https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800"
              alt="Legal simplification"
            />
            <div>
              <h3>4. Legal Simplification</h3>
              <p>Complex legal language is simplified into clear and easy explanations.</p>
            </div>
          </div>

          <div className="step-card">
            <img
              src="https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800"
              alt="Translation"
            />
            <div>
              <h3>5. Tamil Translation</h3>
              <p>The simplified content is translated into Tamil for better accessibility.</p>
            </div>
          </div>

          <div className="step-card">
            <img
              src="https://images.unsplash.com/photo-1589254065878-42c9da997008?w=800"
              alt="Audio explanation"
            />
            <div>
              <h3>6. Audio Generation</h3>
              <p>The system converts explanations into audio for users who prefer listening.</p>
            </div>
          </div>

          <div className="step-card">
            <img
              src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800"
              alt="Risk analysis"
            />
            <div>
              <h3>7. Risk Detection</h3>
              <p>The AI detects risky clauses and highlights potential legal issues.</p>
            </div>
          </div>

          <div className="step-card">
            <img
              src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800"
              alt="Results"
            />
            <div>
              <h3>8. Result Display</h3>
              <p>The simplified explanation, translation, and risk report are displayed to the user.</p>
            </div>
          </div>

        </div>
      </section>

      <Footer />
    </div>
  );
}

export default HowItWorks;