import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [explainer, setExplainer] = useState(false);
  const [categories, setCategories] = useState([]);
  const [selectedCategories, setSelectedCategories] = useState(["all"]);

  // Fetch all categories
  const fetchCategories = async () => {
    const res = await fetch("http://127.0.0.1:8000/categories");
    const data = await res.json();
    setCategories(data);
  };

  // Fetch News
  const fetchNews = async () => {
    setLoading(true);
    const catQuery = selectedCategories.includes("all")
      ? "all"
      : selectedCategories.join(",");
    const res = await fetch(
      `http://127.0.0.1:8000/news?explainer=${explainer}&categories=${catQuery}`
    );
    const data = await res.json();
    setNews(data);
    setLoading(false);
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  useEffect(() => {
    fetchNews();
  }, [explainer, selectedCategories]);

  // Subscribe
  const handleSubscribe = async () => {
    if (!email) return alert("Enter your email");

    const res = await fetch("http://127.0.0.1:8000/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });

    if (res.ok) alert("✅ Subscribed! Newsletter will be sent.");
    setEmail("");
  };

  // Run AI Agent
  const handleRunAgent = async () => {
    const res = await fetch("http://127.0.0.1:8000/run");
    if (res.ok) {
      alert("🤖 AI Agent ran! Newsletter sent & news updated.");
      fetchCategories();
      fetchNews();
    }
  };

  // Handle category selection
  const toggleCategory = (cat) => {
    if (cat === "all") {
      setSelectedCategories(["all"]);
    } else {
      let updated = selectedCategories.includes(cat)
        ? selectedCategories.filter((c) => c !== cat)
        : [...selectedCategories.filter((c) => c !== "all"), cat];
      if (updated.length === 0) updated = ["all"];
      setSelectedCategories(updated);
    }
  };

  return (
    <div className="app-container">
      <h1 className="title">Tech-UpNext 🧠</h1>

      {/* Controls */}
      <div className="controls">
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="email-input"
        />

        <label className="checkbox">
          <input
            type="checkbox"
            checked={explainer}
            onChange={() => setExplainer(!explainer)}
          />
          Explainer Mode
        </label>

        <button className="btn btn-blue" onClick={handleSubscribe}>
          Subscribe
        </button>

        <button className="btn btn-green" onClick={handleRunAgent}>
          Run Agent
        </button>
      </div>

      {/* Category Filters */}
      <div className="categories">
        <strong>Filter by Category:</strong>
        <label>
          <input
            type="checkbox"
            checked={selectedCategories.includes("all")}
            onChange={() => toggleCategory("all")}
          />
          All
        </label>
        {categories.map((c) => (
          <label key={c}>
            <input
              type="checkbox"
              checked={selectedCategories.includes(c)}
              onChange={() => toggleCategory(c)}
            />
            {c}
          </label>
        ))}
      </div>

      {/* News Display */}
      {loading ? (
        <p className="loading-text">Loading personalized news...</p>
      ) : (
        <div className="news-list">
          {news.map((n, i) => (
            <div key={i} className="news-card">
              <h3 className="news-title">{n.title}</h3>
              {n.category && <p className="news-category">Category: {n.category}</p>}
              <p className="news-summary">{explainer ? n.explainer : n.summary}</p>
              {explainer && n.link && (
                <a
                  href={n.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="read-more"
                >
                  Read Full Article →
                </a>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
