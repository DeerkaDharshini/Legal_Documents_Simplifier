import React from "react";

function ResultCard({ title, text }) {

  return (
    <div className="result-card">

      <h2>{title}</h2>

      <p>{text}</p>

    </div>
  );
}

export default ResultCard;