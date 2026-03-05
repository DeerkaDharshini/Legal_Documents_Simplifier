import React from "react";
import Navbar from "../components/Navbar";

function About() {

  return (
    <div>

      <Navbar />

      <h1>About This Project</h1>

      <p>

      Legal documents are difficult for many people to understand.

      This AI system simplifies legal text, translates it into Tamil,
      and provides an audio explanation.

      </p>

      <h3>Technologies Used</h3>

      <ul>

        <li>React</li>

        <li>FastAPI</li>

        <li>LangChain</li>

        <li>Mistral LLM</li>

        <li>gTTS</li>

      </ul>

    </div>
  );
}

export default About;