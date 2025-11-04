"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [papers, setPapers] = useState<any[]>([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);

  const limit = 9;
  const totalPages = Math.ceil(total / limit);

  const fetchPapers = async (pageNum = 1) => {
    setLoading(true);
    try {
      const skip = (pageNum - 1) * limit;
      const res = await fetch(
        `http://127.0.0.1:8000/api/papers?skip=${skip}&limit=${limit}`,
        { cache: "no-store" }
      );
      const data = await res.json();
      setPapers(data.results || []);
      setTotal(data.total || 0);
    } catch (err) {
      console.error("❌ Fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPapers(page);
  }, [page]);

  return (
    <main className="bg-gray-50 min-h-screen py-10">
      <div className="max-w-7xl mx-auto px-6">
        <h1 className="text-4xl font-bold mb-10 text-gray-900">
          🧠 Daily Papers
        </h1>

        {loading ? (
          <p className="text-center text-gray-500">Loading papers...</p>
        ) : papers.length === 0 ? (
          <p className="text-center text-gray-500">No papers found.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {papers.map((paper) => (
              <div
                key={paper.id}
                className="bg-white rounded-2xl shadow-sm border hover:shadow-md transition-all overflow-hidden"
              >
                <div className="aspect-[4/3] bg-gray-100 flex items-center justify-center text-gray-400 text-sm font-medium">
                  🧾 Paper Preview
                </div>
                <div className="p-5">
                  <a
                    href={paper.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block text-lg font-semibold text-gray-900 hover:text-blue-600 transition"
                  >
                    {paper.title}
                  </a>
                  <p className="text-gray-600 text-sm mt-2">
                    {paper.authors || "Unknown authors"}
                  </p>
                  <div className="flex justify-between items-center mt-3 text-gray-400 text-sm">
                    <span
                    >📅 {paper.published}</span>
                    <span>🌐 {paper.source}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Pagination Controls */}
        <div className="flex justify-center items-center gap-6 mt-12">
          <button
            disabled={page === 1}
            onClick={() => setPage(page - 1)}
            className={`px-5 py-2 rounded-full border text-sm transition-all duration-200 ${
              page === 1
                ? "border-gray-200 text-gray-400 bg-gray-100 cursor-not-allowed"
                : "border-gray-300 text-gray-700 bg-white hover:bg-gray-50 hover:shadow-sm"
            }`}
          >
            ← Previous
          </button>

          <span className="text-gray-500 font-medium">
            Page {page} of {totalPages}
          </span>

          <button
            disabled={page === totalPages}
            onClick={() => setPage(page + 1)}
            className={`px-5 py-2 rounded-full border text-sm transition-all duration-200 ${
              page === totalPages
                ? "border-gray-200 text-gray-400 bg-gray-100 cursor-not-allowed"
                : "border-gray-300 text-gray-700 bg-white hover:bg-gray-50 hover:shadow-sm"
            }`}
          >
            Next →
          </button>
        </div>
      </div>
    </main>
  );
}

