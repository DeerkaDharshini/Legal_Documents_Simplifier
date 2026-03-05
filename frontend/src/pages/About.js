import React from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

function About() {
  return (
    <div>
      <Navbar />

      <section className="about-section">
        <h1>About This Project</h1>

        <p>
          Legal documents are difficult for many people to understand.
          This AI system simplifies legal text, translates it into Tamil,
          and provides an audio explanation to make legal documents
          accessible to everyone.
        </p>

        <h3>Technologies Used</h3>

        <ul>
          <li>React</li>
          <li>FastAPI</li>
          <li>Google Gemini 2.0 Flash — Text Simplification, Risk Analysis &amp; Translation</li>
          <li>gTTS — Audio Generation</li>
        </ul>
      </section>

      <Footer />
    </div>
  );
}

export default About;