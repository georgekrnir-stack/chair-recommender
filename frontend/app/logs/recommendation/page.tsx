"use client";

import { useEffect, useState } from "react";
import { getRecommendationLogs } from "@/lib/api";

interface RecommendationLog {
  id: string;
  form_input: string;
  parsed_conditions: Record<string, unknown>;
  recommended_chair_ids: string[];
  response_text: string;
  created_at: string;
}

export default function RecommendationLogsPage() {
  const [logs, setLogs] = useState<RecommendationLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => {
    getRecommendationLogs()
      .then(setLogs)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>読み込み中...</p>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">推薦ログ</h2>
      {logs.length === 0 ? (
        <p className="text-gray-500">推薦ログがありません。</p>
      ) : (
        <div className="space-y-3">
          {logs.map((log) => (
            <div key={log.id} className="border rounded-lg p-4">
              <div
                className="flex items-center justify-between cursor-pointer"
                onClick={() => setExpanded(expanded === log.id ? null : log.id)}
              >
                <div>
                  <p className="font-medium text-sm truncate max-w-lg">
                    {log.form_input.slice(0, 100)}...
                  </p>
                  <p className="text-xs text-gray-500">
                    {new Date(log.created_at).toLocaleString("ja-JP")} / 推薦{log.recommended_chair_ids?.length || 0}件
                  </p>
                </div>
                <span className="text-gray-400">{expanded === log.id ? "▲" : "▼"}</span>
              </div>
              {expanded === log.id && (
                <div className="mt-4 space-y-3 border-t pt-3">
                  <div>
                    <h4 className="text-xs font-medium text-gray-500 mb-1">入力</h4>
                    <p className="text-sm bg-gray-50 p-2 rounded whitespace-pre-wrap">{log.form_input}</p>
                  </div>
                  <div>
                    <h4 className="text-xs font-medium text-gray-500 mb-1">パース結果</h4>
                    <pre className="text-xs bg-gray-50 p-2 rounded overflow-x-auto">
                      {JSON.stringify(log.parsed_conditions, null, 2)}
                    </pre>
                  </div>
                  <div>
                    <h4 className="text-xs font-medium text-gray-500 mb-1">推薦文</h4>
                    <p className="text-sm bg-green-50 p-2 rounded whitespace-pre-wrap">{log.response_text}</p>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
