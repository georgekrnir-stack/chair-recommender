"use client";

import { useEffect, useState } from "react";
import { getVideos, syncVideos } from "@/lib/api";

interface Video {
  id: string;
  youtube_video_id: string;
  title: string;
  published_at: string;
  url: string;
  status: string;
}

const statusColors: Record<string, string> = {
  pending: "bg-gray-100 text-gray-700",
  transcribed: "bg-blue-100 text-blue-700",
  extracted: "bg-yellow-100 text-yellow-700",
  reviewed: "bg-green-100 text-green-700",
};

export default function VideosPage() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);

  const fetchVideos = () => {
    getVideos()
      .then(setVideos)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchVideos(); }, []);

  const handleSync = async () => {
    setSyncing(true);
    try {
      const result = await syncVideos();
      alert(result.message);
      fetchVideos();
    } catch (e) {
      alert(e instanceof Error ? e.message : "エラーが発生しました");
    } finally {
      setSyncing(false);
    }
  };

  if (loading) return <p>読み込み中...</p>;

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">動画一覧</h2>
        <button
          onClick={handleSync}
          disabled={syncing}
          className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700 disabled:opacity-50"
        >
          {syncing ? "チェック中..." : "新着チェック"}
        </button>
      </div>
      {videos.length === 0 ? (
        <p className="text-gray-500">動画データがありません。</p>
      ) : (
        <div className="space-y-3">
          {videos.map((video) => (
            <div key={video.id} className="border rounded-lg p-4 flex items-center justify-between">
              <div>
                <a href={video.url} target="_blank" rel="noopener noreferrer" className="font-medium hover:text-blue-600">
                  {video.title}
                </a>
                <p className="text-sm text-gray-500">
                  {new Date(video.published_at).toLocaleDateString("ja-JP")}
                </p>
              </div>
              <span className={`text-xs px-2 py-1 rounded ${statusColors[video.status] || "bg-gray-100"}`}>
                {video.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
