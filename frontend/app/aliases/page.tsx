"use client";

import { useEffect, useState } from "react";
import AliasResolver from "@/components/AliasResolver";
import { getUnresolvedLogs, getChairs } from "@/lib/api";

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

export default function AliasesPage() {
  const [logs, setLogs] = useState<ExtractionLogEntry[]>([]);
  const [chairs, setChairs] = useState<Chair[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [logsData, chairsData] = await Promise.all([getUnresolvedLogs(), getChairs()]);
      setLogs(logsData);
      setChairs(chairsData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, []);

  if (loading) return <p>読み込み中...</p>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">名寄せ確認・修正</h2>
      {logs.length === 0 ? (
        <p className="text-gray-500">未解決の言及はありません。</p>
      ) : (
        <div className="space-y-3">
          <p className="text-sm text-gray-600">{logs.length}件の未解決言及</p>
          {logs.map((log) => (
            <AliasResolver key={log.id} log={log} chairs={chairs} onResolved={fetchData} />
          ))}
        </div>
      )}
    </div>
  );
}
