"use client";

import { useState } from "react";
import { updatePrompt, testPrompt } from "@/lib/api";

interface PromptEditorProps {
  promptKey: string;
  initialContent: string;
  onSaved?: () => void;
}

export default function PromptEditor({ promptKey, initialContent, onSaved }: PromptEditorProps) {
  const [content, setContent] = useState(initialContent);
  const [testInput, setTestInput] = useState("");
  const [testResult, setTestResult] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [testing, setTesting] = useState(false);

  const handleSave = async () => {
    setSaving(true);
    try {
      await updatePrompt(promptKey, content);
      onSaved?.();
    } catch (e) {
      alert(e instanceof Error ? e.message : "保存に失敗しました");
    } finally {
      setSaving(false);
    }
  };

  const handleTest = async () => {
    if (!testInput.trim()) return;
    setTesting(true);
    setTestResult(null);
    try {
      const data = await testPrompt(promptKey, testInput);
      setTestResult(data.result);
    } catch (e) {
      setTestResult(`エラー: ${e instanceof Error ? e.message : "不明なエラー"}`);
    } finally {
      setTesting(false);
    }
  };

  return (
    <div className="space-y-4">
      <textarea
        className="w-full h-64 border rounded-lg p-3 text-sm font-mono resize-y"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <div className="flex gap-2">
        <button
          onClick={handleSave}
          disabled={saving}
          className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700 disabled:opacity-50"
        >
          {saving ? "保存中..." : "保存"}
        </button>
      </div>
      <div className="border-t pt-4">
        <h4 className="text-sm font-medium mb-2">テスト実行</h4>
        <textarea
          className="w-full h-24 border rounded-lg p-3 text-sm resize-y"
          placeholder="テスト入力..."
          value={testInput}
          onChange={(e) => setTestInput(e.target.value)}
        />
        <button
          onClick={handleTest}
          disabled={testing || !testInput.trim()}
          className="mt-2 bg-gray-600 text-white px-4 py-2 rounded text-sm hover:bg-gray-700 disabled:opacity-50"
        >
          {testing ? "実行中..." : "テスト実行"}
        </button>
        {testResult && (
          <div className="mt-2 bg-gray-50 border rounded-lg p-3 text-sm whitespace-pre-wrap">
            {testResult}
          </div>
        )}
      </div>
    </div>
  );
}
