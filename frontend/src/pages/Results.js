import React from "react";
import Navbar from "../components/Navbar";
import ResultCard from "../components/ResultCard";
import AudioPlayer from "../components/AudioPlayer";

function Results({ simplified, tamil, audio }) {

  return (
    <div>

      <Navbar />

      <h1>Analysis Results</h1>

      <ResultCard
        title="Simplified English"
        text={simplified}
      />

      <ResultCard
        title="Tamil Translation"
        text={tamil}
      />

      <AudioPlayer audio={audio} />

    </div>
  );
}

export default Results;