"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [papers, setPapers] = useState<any[]>([]);
  const [q, setQ] = useState("");
  const [source, setSource] = useState("");
  const [limit] = useState(5);
  const [offset, setOffset] = useState(0);
  const [total, setTotal] = useState(0);

  // New state for add form
  const [newPaper, setNewPaper] = useState({
    title: "",
    authors: "",
    published: "",
    url: "",
    source: "",
  });

  async function fetchPapers() {
    const params = new URLSearchParams();
    if (q) params.append("q", q);
    if (source) params.append("source", source);
    params.append("limit", limit.toString());
    params.append("offset", offset.toString());

    try {
      const res = await fetch(`http://localhost:8000/api/papers?${params.toString()}`);
      const data = await res.json();
      setPapers(data.results || []);
      setTotal(data.total || 0);
    } catch (err) {
      console.error("Error fetching papers:", err);
    }
  }

  async function addPaper(e: React.FormEvent) {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/api/papers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newPaper),
      });
      if (res.ok) {
        setNewPaper({ title: "", authors: "", published: "", url: "", source: "" });
        fetchPapers(); // refresh list
        alert("✅ Paper added!");
      } else {
        alert("❌ Failed to add paper.");
      }
    } catch (err) {
      console.error("Error adding paper:", err);
    }
  }

  useEffect(() => {
    fetchPapers();
  }, [offset]);

  const totalPages = Math.ceil(total / limit);

  return (
    <div className="max-w-4xl mx-auto py-10 px-4">
      <h1 className="text-3xl font-bold mb-6 text-center text-blue-700">
        📄 HuggingFace Papers Clone
      </h1>

      {/* Add Paper Form */}
      <form onSubmit={addPaper} className="border p-4 rounded mb-6 shadow">
        <h2 className="text-xl font-semibold mb-3">➕ Add New Paper</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <input
            required
            placeholder="Title"
            value={newPaper.title}
            onChange={(e) => setNewPaper({ ...newPaper, title: e.target.value })}
            className="border rounded px-3 py-2"
          />
          <input
            required
            placeholder="Authors (e.g., Alice; Bob)"
            value={newPaper.authors}
            onChange={(e) => setNewPaper({ ...newPaper, authors: e.target.value })}
            className="border rounded px-3 py-2"
          />
          <input
            required
            placeholder="Published (YYYY-MM-DD)"
            value={newPaper.published}
            onChange={(e) => setNewPaper({ ...newPaper, published: e.target.value })}
            className="border rounded px-3 py-2"
          />
          <input
            required
            placeholder="URL"
            value={newPaper.url}
            onChange={(e) => setNewPaper({ ...newPaper, url: e.target.value })}
            className="border rounded px-3 py-2"
          />
          <input
            required
            placeholder="Source (e.g., arxiv)"
            value={newPaper.source}
            onChange={(e) => setNewPaper({ ...newPaper, source: e.target.value })}
            className="border rounded px-3 py-2"
          />
        </div>
        <button
          type="submit"
          className="bg-green-600 text-white px-4 py-2 rounded mt-3 hover:bg-green-700"
        >
          Add Paper
        </button>
      </form>

      {/* Search + Filter */}
      <div className="flex flex-col sm:flex-row gap-2 mb-6">
        <input
          placeholder="Search..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
          className="border rounded px-3 py-2 flex-1"
        />
        <input
          placeholder="Source (e.g., arxiv)"
          value={source}
          onChange={(e) => setSource(e.target.value)}
          className="border rounded px-3 py-2"
        />
        <button
          onClick={() => {
            setOffset(0);
            fetchPapers();
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Search
        </button>
      </div>

      {/* Results */}
      <div className="border rounded p-4 shadow">
        {papers.length === 0 ? (
          <p className="text-gray-500 text-center">No papers found.</p>
        ) : (
          papers.map((p) => (
            <div key={p.id} className="py-3 border-b last:border-none">
              <a href={p.url} target="_blank" className="text-blue-600 hover:underline font-medium">
                {p.title}
              </a>
              <div className="text-sm text-gray-600">
                {p.authors} — <span className="italic">{p.source}</span>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center gap-4 mt-6">
          <button
            onClick={() => setOffset(Math.max(0, offset - limit))}
            disabled={offset === 0}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            Prev
          </button>
          <span>
            Page {Math.floor(offset / limit) + 1} of {totalPages}
          </span>
          <button
            onClick={() => setOffset(offset + limit)}
            disabled={offset + limit >= total}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}

