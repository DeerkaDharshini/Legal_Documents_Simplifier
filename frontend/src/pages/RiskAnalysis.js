import React from "react";
import Navbar from "../components/Navbar";
import RiskCard from "../components/RiskCard";

function RiskAnalysis() {

  return (
    <div>

      <Navbar />

      <h1>Legal Risk Analysis</h1>

      <RiskCard
        title="Payment Obligation"
        level="Medium"
        description="Payment must be made before services begin."
      />

      <RiskCard
        title="Liability Clause"
        level="High"
        description="User assumes all legal responsibility."
      />

    </div>
  );
}

export default RiskAnalysis;