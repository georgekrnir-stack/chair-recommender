"use client";

import { useEffect, useState } from "react";
import ChairCard from "@/components/ChairCard";
import { getChairs, toggleRecommendable } from "@/lib/api";

interface Chair {
  id: string;
  canonical_name: string;
  maker: string | null;
  price_range: string | null;
  is_recommendable: boolean;
  features: string[];
  pros: string[];
  cons: string[];
}

export default function ChairsPage() {
  const [chairs, setChairs] = useState<Chair[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchChairs = () => {
    getChairs()
      .then(setChairs)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchChairs(); }, []);

  const handleToggle = async (id: string, value: boolean) => {
    try {
      await toggleRecommendable(id, value);
      fetchChairs();
    } catch (e) {
      console.error(e);
    }
  };

  if (loading) return <p>読み込み中...</p>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">椅子マスタ管理</h2>
      {chairs.length === 0 ? (
        <p className="text-gray-500">椅子データがありません。一括構築を実行してください。</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {chairs.map((chair) => (
            <ChairCard key={chair.id} chair={chair} onToggleRecommendable={handleToggle} />
          ))}
        </div>
      )}
    </div>
  );
}
