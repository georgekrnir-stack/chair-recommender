"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { getPrompts, getPromptVersions } from "@/lib/api";
import PromptEditor from "@/components/PromptEditor";

interface PromptData {
  id: string;
  key: string;
  name: string;
  description: string;
  content: string;
  version: number;
}

interface VersionData {
  id: string;
  version: number;
  content: string;
  created_at: string;
}

export default function PromptsPage() {
  const { isAdmin, loading: authLoading } = useAuth();
  const router = useRouter();
  const [prompts, setPrompts] = useState<PromptData[]>([]);
  const [selected, setSelected] = useState<PromptData | null>(null);
  const [versions, setVersions] = useState<VersionData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !isAdmin) {
      router.push("/login");
    }
  }, [isAdmin, authLoading, router]);

  const fetchPrompts = () => {
    getPrompts()
      .then((data) => {
        setPrompts(data);
        if (!selected && data.length > 0) setSelected(data[0]);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchPrompts(); }, []);

  useEffect(() => {
    if (selected) {
      getPromptVersions(selected.key).then(setVersions).catch(console.error);
    }
  }, [selected]);

  if (authLoading || loading) return <p>読み込み中...</p>;
  if (!isAdmin) return null;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">プロンプト編集</h2>
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="space-y-1">
          {prompts.map((p) => (
            <div
              key={p.key}
              onClick={() => setSelected(p)}
              className={`border rounded p-3 cursor-pointer text-sm ${
                selected?.key === p.key ? "border-blue-500 bg-blue-50" : "hover:bg-gray-50"
              }`}
            >
              <p className="font-medium">{p.name}</p>
              <p className="text-xs text-gray-500">v{p.version}</p>
            </div>
          ))}
        </div>
        <div className="lg:col-span-3">
          {selected ? (
            <div>
              <h3 className="font-medium mb-1">{selected.name}</h3>
              <p className="text-sm text-gray-500 mb-4">{selected.description}</p>
              <PromptEditor
                key={selected.key}
                promptKey={selected.key}
                initialContent={selected.content}
                onSaved={fetchPrompts}
              />
              {versions.length > 0 && (
                <div className="mt-6">
                  <h4 className="text-sm font-medium mb-2">バージョン履歴</h4>
                  <div className="space-y-2">
                    {versions.map((v) => (
                      <div key={v.id} className="border rounded p-2 text-xs">
                        <span className="font-medium">v{v.version}</span>
                        <span className="text-gray-500 ml-2">
                          {new Date(v.created_at).toLocaleString("ja-JP")}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <p className="text-gray-500">プロンプトを選択してください</p>
          )}
        </div>
      </div>
    </div>
  );
}
