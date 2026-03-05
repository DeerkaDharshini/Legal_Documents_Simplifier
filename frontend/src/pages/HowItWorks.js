import React from "react";
import Navbar from "../components/Navbar";

function HowItWorks() {

  return (
    <div>

      <Navbar />

      <h1>How It Works</h1>

      <ol>

        <li>Upload legal document</li>

        <li>AI processes document using Mistral model</li>

        <li>Legal text simplified</li>

        <li>Tamil translation generated</li>

        <li>Audio explanation created</li>

        <li>Risk analysis performed</li>

      </ol>

    </div>
  );
}

export default HowItWorks;