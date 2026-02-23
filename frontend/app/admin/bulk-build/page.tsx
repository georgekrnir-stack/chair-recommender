"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { startBulkBuild, getBulkBuildStatus } from "@/lib/api";

interface BuildStatus {
  running: boolean;
  total: number;
  completed: number;
  current_phase: string;
}

export default function BulkBuildPage() {
  const { isAdmin, loading: authLoading } = useAuth();
  const router = useRouter();
  const [status, setStatus] = useState<BuildStatus | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!authLoading && !isAdmin) {
      router.push("/login");
    }
  }, [isAdmin, authLoading, router]);

  const fetchStatus = async () => {
    try {
      const data = await getBulkBuildStatus();
      setStatus(data);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    if (isAdmin) fetchStatus();
  }, [isAdmin]);

  // Poll status while running
  useEffect(() => {
    if (!status?.running) return;
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, [status?.running]);

  const handleStart = async () => {
    setLoading(true);
    try {
      await startBulkBuild();
      fetchStatus();
    } catch (e) {
      alert(e instanceof Error ? e.message : "エラーが発生しました");
    } finally {
      setLoading(false);
    }
  };

  if (authLoading) return <p>読み込み中...</p>;
  if (!isAdmin) return null;

  return (
    <div className="max-w-2xl">
      <h2 className="text-2xl font-bold mb-6">一括構築</h2>
      <p className="text-gray-600 mb-6">
        全動画に対して文字起こし・椅子情報抽出・名寄せを実行します。初期構築時に使用します。
      </p>

      <div className="space-y-6">
        <div className="border rounded-lg p-4">
          <h3 className="font-medium mb-2">構築フェーズ</h3>
          <ol className="list-decimal list-inside text-sm space-y-1 text-gray-600">
            <li>全動画の文字起こし取得</li>
            <li>メーカー商品一覧スクレイピング</li>
            <li>LLMによる椅子言及抽出</li>
            <li>クラスタリング・名寄せ</li>
            <li>確認・修正（手動）</li>
            <li>DB投入・構造化抽出</li>
          </ol>
        </div>

        {status?.running ? (
          <div className="border rounded-lg p-4 bg-blue-50">
            <h3 className="font-medium mb-2">実行中</h3>
            <p className="text-sm">フェーズ: {status.current_phase}</p>
            {status.total > 0 && (
              <div className="mt-2">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all"
                    style={{ width: `${(status.completed / status.total) * 100}%` }}
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  {status.completed} / {status.total} 完了
                </p>
              </div>
            )}
          </div>
        ) : (
          <button
            onClick={handleStart}
            disabled={loading}
            className="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 disabled:opacity-50"
          >
            {loading ? "開始中..." : "一括構築を開始"}
          </button>
        )}
      </div>
    </div>
  );
}
