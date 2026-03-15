import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import "./App.css";

import Home from "./pages/Home";
import Analyzer from "./pages/Analyzer";
import Results from "./pages/Results";
import RiskAnalysis from "./pages/RiskAnalysis";
import HowItWorks from "./pages/HowItWorks";
import About from "./pages/About";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/analyzer" element={<Analyzer />} />
        <Route path="/results" element={<Results />} />
        <Route path="/risk" element={<RiskAnalysis />} />
        <Route path="/how" element={<HowItWorks />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;