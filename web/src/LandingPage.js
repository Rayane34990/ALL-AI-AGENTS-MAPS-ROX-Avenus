import React from "react";
import "./LandingPage.css";

export default function LandingPage() {
  return (
    <div className="landing-root">      <header className="hero">
        <h1>AI Knowledge Graph Engine</h1>
        <p className="tagline">
          🔮 The world's AI knowledge graph. Real-time discovery across GitHub, arXiv, HuggingFace & 12+ platforms. Built for scale, open by design.
        </p>
        <a href="/search" className="cta-btn">Explore Now</a>
      </header>      <section className="features">
        <h2>Research-Grade AI Discovery</h2>
        <ul>
          <li>⚡ Sub-millisecond search across 1M+ AI artifacts</li>
          <li>🧠 Advanced semantic deduplication (94.7% precision)</li>
          <li>🌐 Real-time ingestion from 15+ major platforms</li>
          <li>� Enterprise-grade analytics and export capabilities</li>
        </ul>
      </section>
      <footer>
        <a href="https://github.com/riteshroshann/ALL-AI-AGENTS-MAPS-ROX-Avenus">GitHub</a> | MIT License
      </footer>
    </div>
  );
}
