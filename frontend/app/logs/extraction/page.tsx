"use client";

import { useEffect, useState } from "react";
import { getExtractionLogs } from "@/lib/api";

interface ExtractionLog {
  id: string;
  video_id: string;
  chair_id: string | null;
  raw_mention: string;
  context: string;
  timestamp_hint: string;
  confidence: string;
  status: string;
  created_at: string;
}

export default function ExtractionLogsPage() {
  const [logs, setLogs] = useState<ExtractionLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState("");
  const [confidenceFilter, setConfidenceFilter] = useState("");

  useEffect(() => {
    const params: Record<string, string> = {};
    if (statusFilter) params.status = statusFilter;
    if (confidenceFilter) params.confidence = confidenceFilter;
    getExtractionLogs(params)
      .then(setLogs)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [statusFilter, confidenceFilter]);

  if (loading) return <p>読み込み中...</p>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">抽出ログ</h2>
      <div className="flex gap-4 mb-4">
        <select
          className="border rounded px-3 py-1 text-sm"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="">全ステータス</option>
          <option value="auto_matched">自動マッチ</option>
          <option value="manually_matched">手動マッチ</option>
          <option value="unresolved">未解決</option>
          <option value="ignored">無視</option>
        </select>
        <select
          className="border rounded px-3 py-1 text-sm"
          value={confidenceFilter}
          onChange={(e) => setConfidenceFilter(e.target.value)}
        >
          <option value="">全確信度</option>
          <option value="high">高</option>
          <option value="medium">中</option>
          <option value="low">低</option>
        </select>
      </div>
      {logs.length === 0 ? (
        <p className="text-gray-500">ログがありません。</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-100">
                <th className="border p-2 text-left">言及表現</th>
                <th className="border p-2 text-left">文脈</th>
                <th className="border p-2 text-left">確信度</th>
                <th className="border p-2 text-left">ステータス</th>
                <th className="border p-2 text-left">日時</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-gray-50">
                  <td className="border p-2 font-medium">{log.raw_mention}</td>
                  <td className="border p-2 text-gray-600 max-w-xs truncate">{log.context}</td>
                  <td className="border p-2">{log.confidence}</td>
                  <td className="border p-2">{log.status}</td>
                  <td className="border p-2">{new Date(log.created_at).toLocaleString("ja-JP")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
