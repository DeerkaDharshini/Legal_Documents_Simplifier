import React from "react";
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import FeatureCard from "../components/FeatureCard";
import Footer from "../components/Footer";

function Home() {

  return (
    <div>

      <Navbar />

      <Hero />

      <section className="features">

        <FeatureCard
          icon="📄"
          title="Upload Documents"
          description="Upload legal PDF, DOCX or TXT documents."
        />

        <FeatureCard
          icon="⚡"
          title="AI Simplification"
          description="Convert complex legal language into simple English."
        />

        <FeatureCard
          icon="🌍"
          title="Tamil Translation"
          description="Understand legal documents in Tamil."
        />

        <FeatureCard
          icon="⚠"
          title="Risk Analysis"
          description="Detect hidden risks in contracts."
        />

      </section>

      <Footer />

    </div>
  );
}

export default Home;