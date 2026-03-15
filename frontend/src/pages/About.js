import React from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

function About() {
  return (
    <div>
      <Navbar />

      <section className="about-section">
        <h1>About Legal Document Simplifier & Risk Analyzer</h1>

        <p className="about-intro">
          Legal documents are difficult for many people to understand.
          This AI system simplifies legal text, translates it into Tamil,
          and provides an audio explanation to make legal documents
          accessible to everyone.
        </p>

        <div className="about-grid">

          <div className="about-card">
            <img
              src="https://images.unsplash.com/photo-1521791136064-7986c2920216?w=800"
              alt="Person reading legal document"
            />
            <p>Uploading and reviewing contracts or agreements.</p>
          </div>

          <div className="about-card">
            <img
              src="https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=800"
              alt="AI document analysis"
            />
            <p>AI analyzing complex legal text and simplifying it.</p>
          </div>

          <div className="about-card">
            <img
              src="https://images.unsplash.com/photo-1556761175-b413da4baf72?w=800"
              alt="People discussing documents"
            />
            <p>Understanding contract terms before signing.</p>
          </div>

          <div className="about-card">
            <img
              src="https://images.unsplash.com/photo-1581092335397-9583eb92d232?w=800"
              alt="Business meeting contract"
            />
            <p>Identifying risks and important clauses in documents.</p>
          </div>

        </div>
      </section>

      <Footer />
    </div>
  );
}

export default About;