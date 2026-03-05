import React from "react";

function AudioPlayer({ audio }) {

  if (!audio) return null;

  return (
    <div className="audio-player">

      <h3>Audio Explanation</h3>

      <audio controls src={audio}></audio>

    </div>
  );
}

export default AudioPlayer;