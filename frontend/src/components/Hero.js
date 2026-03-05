import React from "react";
import { Link } from "react-router-dom";

function Hero() {
  return (
    <section className="hero">

      <h1>AI Legal Document Simplifier</h1>

      <p>
        Understand complex legal documents instantly
        in plain English and Tamil.
      </p>

      <div className="hero-buttons">
        <Link to="/analyzer">
          <button className="primary-btn">Start Analyzing</button>
        </Link>

        <Link to="/risk">
          <button className="secondary-btn">Risk Analysis</button>
        </Link>
      </div>

    </section>
  );
}

export default Hero;