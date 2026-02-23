"use client";

import { useState } from "react";
import { recommend } from "@/lib/api";

export default function RecommendForm() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await recommend(input);
      setResult(data.response_text);
    } catch (e) {
      setError(e instanceof Error ? e.message : "エラーが発生しました");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">
          フォーム回答を貼り付けてください
        </label>
        <textarea
          className="w-full h-48 border rounded-lg p-3 text-sm resize-y"
          placeholder="公式LINEフォームの回答内容をここに貼り付け..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
      </div>
      <button
        onClick={handleSubmit}
        disabled={loading || !input.trim()}
        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? "分析中..." : "おすすめを聞く"}
      </button>
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg text-sm">
          {error}
        </div>
      )}
      {result && (
        <div className="bg-green-50 border border-green-200 p-4 rounded-lg">
          <h3 className="font-medium mb-2">おすすめ結果</h3>
          <div className="text-sm whitespace-pre-wrap">{result}</div>
        </div>
      )}
    </div>
  );
}
