import React from "react";

function RiskCard({ title, level, description }) {

  return (
    <div className={`risk-card ${level}`}>

      <h3>{title}</h3>

      <p>Risk Level: {level}</p>

      <p>{description}</p>

    </div>
  );
}

export default RiskCard;