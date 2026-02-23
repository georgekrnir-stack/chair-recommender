"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth";

const publicLinks = [
  { href: "/", label: "推薦" },
  { href: "/videos", label: "動画一覧" },
  { href: "/chairs", label: "椅子マスタ" },
  { href: "/makers", label: "メーカー商品" },
  { href: "/aliases", label: "名寄せ" },
  { href: "/logs/extraction", label: "抽出ログ" },
  { href: "/logs/recommendation", label: "推薦ログ" },
];

const adminLinks = [
  { href: "/admin/prompts", label: "プロンプト編集" },
  { href: "/admin/bulk-build", label: "一括構築" },
];

export default function Navbar() {
  const { isAdmin } = useAuth();

  return (
    <nav className="w-60 min-h-screen bg-gray-900 text-white p-4 flex-shrink-0">
      <h1 className="text-lg font-bold mb-6 px-2">椅子レコメンド</h1>
      <ul className="space-y-1">
        {publicLinks.map((link) => (
          <li key={link.href}>
            <Link
              href={link.href}
              className="block px-3 py-2 rounded hover:bg-gray-700 transition-colors text-sm"
            >
              {link.label}
            </Link>
          </li>
        ))}
        {isAdmin && (
          <>
            <li className="pt-4 pb-1 px-3 text-xs text-gray-400 uppercase">管理者</li>
            {adminLinks.map((link) => (
              <li key={link.href}>
                <Link
                  href={link.href}
                  className="block px-3 py-2 rounded hover:bg-gray-700 transition-colors text-sm"
                >
                  {link.label}
                </Link>
              </li>
            ))}
          </>
        )}
      </ul>
      <div className="mt-auto pt-8 px-2">
        {isAdmin ? (
          <Link href="/" className="text-xs text-gray-400 hover:text-white">
            ログアウト
          </Link>
        ) : (
          <Link href="/login" className="text-xs text-gray-400 hover:text-white">
            管理者ログイン
          </Link>
        )}
      </div>
    </nav>
  );
}
