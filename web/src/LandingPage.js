import React from "react";
import "./LandingPage.css";

export default function LandingPage() {
  return (
    <div className="landing-root">
      <header className="hero">
        <h1>ALL AI AGENTS MAPS: ROX AVENUS</h1>
        <p className="tagline">
          Discover, compare, and explore every AI agent, model, and tool—open, unified, and for everyone.
        </p>
        <a href="/search" className="cta-btn">Explore Now</a>
      </header>
      <section className="features">
        <h2>Why use this?</h2>
        <ul>
          <li>🔍 Unified, blazing-fast search across all major AI sources</li>
          <li>🧠 Smart deduplication, auto-tagging, and analytics</li>
          <li>🌐 100% open-source, automated, and community-driven</li>
          <li>🚀 Export, filter, and analyze with ease</li>
        </ul>
      </section>
      <footer>
        <a href="https://github.com/riteshroshann/ALL-AI-AGENTS-MAPS-ROX-Avenus">GitHub</a> | MIT License
      </footer>
    </div>
  );
}
