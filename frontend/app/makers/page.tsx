"use client";

import { useEffect, useState } from "react";
import { getMakers, getMakerProducts, createScrapeConfig } from "@/lib/api";

interface ScrapeConfig {
  id: string;
  maker: string;
  url: string;
  scrape_method: string | null;
  last_scraped_at: string | null;
}

interface Product {
  id: string;
  product_name: string;
  model_number: string | null;
}

export default function MakersPage() {
  const [configs, setConfigs] = useState<ScrapeConfig[]>([]);
  const [selectedMaker, setSelectedMaker] = useState<string | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [newMaker, setNewMaker] = useState("");
  const [newUrl, setNewUrl] = useState("");

  useEffect(() => {
    getMakers()
      .then(setConfigs)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleSelectMaker = async (maker: string) => {
    setSelectedMaker(maker);
    try {
      const data = await getMakerProducts(maker);
      setProducts(data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleAddConfig = async () => {
    if (!newMaker || !newUrl) return;
    try {
      await createScrapeConfig({ maker: newMaker, url: newUrl });
      setNewMaker("");
      setNewUrl("");
      const data = await getMakers();
      setConfigs(data);
    } catch (e) {
      alert(e instanceof Error ? e.message : "エラーが発生しました");
    }
  };

  if (loading) return <p>読み込み中...</p>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">メーカー商品一覧</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h3 className="font-medium mb-3">メーカー設定</h3>
          <div className="space-y-2 mb-4">
            {configs.map((c) => (
              <div
                key={c.id}
                onClick={() => handleSelectMaker(c.maker)}
                className={`border rounded p-3 cursor-pointer hover:bg-gray-50 ${
                  selectedMaker === c.maker ? "border-blue-500 bg-blue-50" : ""
                }`}
              >
                <p className="font-medium">{c.maker}</p>
                <p className="text-xs text-gray-500 truncate">{c.url}</p>
              </div>
            ))}
          </div>
          <div className="border-t pt-4 space-y-2">
            <input
              placeholder="メーカー名"
              value={newMaker}
              onChange={(e) => setNewMaker(e.target.value)}
              className="w-full border rounded px-3 py-1 text-sm"
            />
            <input
              placeholder="商品一覧URL"
              value={newUrl}
              onChange={(e) => setNewUrl(e.target.value)}
              className="w-full border rounded px-3 py-1 text-sm"
            />
            <button
              onClick={handleAddConfig}
              className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
            >
              追加
            </button>
          </div>
        </div>
        <div>
          <h3 className="font-medium mb-3">
            {selectedMaker ? `${selectedMaker} の商品一覧` : "メーカーを選択してください"}
          </h3>
          {products.length > 0 ? (
            <div className="space-y-2">
              {products.map((p) => (
                <div key={p.id} className="border rounded p-3">
                  <p className="font-medium text-sm">{p.product_name}</p>
                  {p.model_number && <p className="text-xs text-gray-500">型番: {p.model_number}</p>}
                </div>
              ))}
            </div>
          ) : selectedMaker ? (
            <p className="text-gray-500 text-sm">商品データがありません。</p>
          ) : null}
        </div>
      </div>
    </div>
  );
}
