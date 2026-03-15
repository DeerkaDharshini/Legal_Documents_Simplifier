import React from "react";

function AudioPlayer({ audio, tamilAudio }) {

  if (!audio && !tamilAudio) return null;

  return (
    <div className="audio-player">

      {audio && (
        <>
          <h3>English Audio Explanation</h3>
          <audio controls src={audio}></audio>
        </>
      )}

      {tamilAudio && (
        <>
          <h3>Tamil Audio Explanation</h3>
          <audio controls src={tamilAudio}></audio>
        </>
      )}

    </div>
  );
}

export default AudioPlayer;