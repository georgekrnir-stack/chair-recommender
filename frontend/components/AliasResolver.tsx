"use client";

import { useState } from "react";
import { resolveLog, ignoreLog } from "@/lib/api";

interface ExtractionLogEntry {
  id: string;
  raw_mention: string;
  context: string;
  confidence: string;
  status: string;
}

interface Chair {
  id: string;
  canonical_name: string;
}

interface AliasResolverProps {
  log: ExtractionLogEntry;
  chairs: Chair[];
  onResolved?: () => void;
}

export default function AliasResolver({ log, chairs, onResolved }: AliasResolverProps) {
  const [selectedChairId, setSelectedChairId] = useState("");
  const [loading, setLoading] = useState(false);

  const handleResolve = async () => {
    if (!selectedChairId) return;
    setLoading(true);
    try {
      await resolveLog(log.id, selectedChairId);
      onResolved?.();
    } catch (e) {
      alert(e instanceof Error ? e.message : "エラーが発生しました");
    } finally {
      setLoading(false);
    }
  };

  const handleIgnore = async () => {
    setLoading(true);
    try {
      await ignoreLog(log.id);
      onResolved?.();
    } catch (e) {
      alert(e instanceof Error ? e.message : "エラーが発生しました");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="border rounded-lg p-4">
      <div className="mb-2">
        <span className="font-medium">&quot;{log.raw_mention}&quot;</span>
        <span className={`ml-2 text-xs px-2 py-0.5 rounded ${
          log.confidence === "high" ? "bg-green-100 text-green-700" :
          log.confidence === "medium" ? "bg-yellow-100 text-yellow-700" :
          "bg-red-100 text-red-700"
        }`}>
          {log.confidence}
        </span>
      </div>
      {log.context && (
        <p className="text-sm text-gray-500 mb-3">文脈: {log.context}</p>
      )}
      <div className="flex gap-2 items-center">
        <select
          className="border rounded px-2 py-1 text-sm flex-1"
          value={selectedChairId}
          onChange={(e) => setSelectedChairId(e.target.value)}
        >
          <option value="">椅子を選択...</option>
          {chairs.map((c) => (
            <option key={c.id} value={c.id}>{c.canonical_name}</option>
          ))}
        </select>
        <button
          onClick={handleResolve}
          disabled={loading || !selectedChairId}
          className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 disabled:opacity-50"
        >
          紐づけ
        </button>
        <button
          onClick={handleIgnore}
          disabled={loading}
          className="bg-gray-200 text-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-300 disabled:opacity-50"
        >
          無視
        </button>
      </div>
    </div>
  );
}
