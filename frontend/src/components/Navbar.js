import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">

      <div className="logo">
        LegalAI
      </div>

      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/analyzer">Analyzer</Link>
        <Link to="/risk">Risk Analysis</Link>
        <Link to="/how">How It Works</Link>
        <Link to="/about">About</Link>
      </div>

    </nav>
  );
}

export default Navbar;