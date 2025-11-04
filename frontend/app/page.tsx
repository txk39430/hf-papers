"use client";

import { useEffect, useState } from "react";

interface Paper {
  id: number;
  title: string;
  authors: string;
  published: string;
  url: string;
  source: string;
}

export default function Home() {
  const [papers, setPapers] = useState<Paper[]>([]);
  const [title, setTitle] = useState("");
  const [authors, setAuthors] = useState("");
  const [published, setPublished] = useState("");
  const [url, setUrl] = useState("");
  const [source, setSource] = useState("");
  const [search, setSearch] = useState("");
  const [filterSource, setFilterSource] = useState("");

  // ✅ Fetch papers from backend
  const fetchPapers = async () => {
    try {
      const params = new URLSearchParams();
      if (search) params.append("q", search);
      if (filterSource) params.append("source", filterSource);

      const res = await fetch(
        `http://127.0.0.1:8000/api/papers?${params.toString()}`,
        { cache: "no-store" }
      );
      const data = await res.json();
      setPapers(data.results || data || []);
    } catch (err) {
      console.error("Error fetching papers:", err);
    }
  };

  useEffect(() => {
    fetchPapers();
  }, []);

  // ✅ Add new paper
  const addPaper = async () => {
    if (!title || !authors || !published || !url || !source) return;
    try {
      const res = await fetch("http://127.0.0.1:8000/api/papers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, authors, published, url, source }),
      });

      if (res.ok) {
        setTitle("");
        setAuthors("");
        setPublished("");
        setUrl("");
        setSource("");
        fetchPapers();
      } else {
        console.error("Failed to add paper");
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <main className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-center mb-6 text-blue-600">
        📄 HuggingFace Papers Clone
      </h1>

      {/* Add New Paper Form */}
      <div className="border p-4 rounded mb-6">
        <h2 className="font-semibold mb-3">➕ Add New Paper</h2>
        <div className="grid grid-cols-2 gap-2 mb-2">
          <input
            className="border p-2"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <input
            className="border p-2"
            placeholder="Authors (e.g., Alice; Bob)"
            value={authors}
            onChange={(e) => setAuthors(e.target.value)}
          />
          <input
            className="border p-2"
            placeholder="Published (YYYY-MM-DD)"
            value={published}
            onChange={(e) => setPublished(e.target.value)}
          />
          <input
            className="border p-2"
            placeholder="URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <input
            className="border p-2 col-span-2"
            placeholder="Source (e.g., arxiv)"
            value={source}
            onChange={(e) => setSource(e.target.value)}
          />
        </div>
        <button
          onClick={addPaper}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Add Paper
        </button>
      </div>

      {/* Search Section */}
      <div className="flex gap-2 mb-6">
        <input
          className="border p-2 flex-grow"
          placeholder="Search..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <input
          className="border p-2 w-48"
          placeholder="Source (e.g., arxiv)"
          value={filterSource}
          onChange={(e) => setFilterSource(e.target.value)}
        />
        <button
          onClick={fetchPapers}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Search
        </button>
      </div>

      {/* Papers List */}
      {papers.length === 0 ? (
        <p className="text-center text-gray-500">No papers found.</p>
      ) : (
        <div className="space-y-4">
          {papers.map((paper) => (
            <div
              key={paper.id}
              className="border rounded p-4 hover:shadow transition"
            >
              <a
                href={paper.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-lg font-semibold text-blue-700 hover:underline"
              >
                {paper.title}
              </a>
              <p className="text-sm text-gray-600">{paper.authors}</p>
              <p className="text-sm text-gray-500">
                📅 {paper.published} | 🧩 {paper.source}
              </p>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}

