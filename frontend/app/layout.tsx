"use client";

import "./globals.css";
import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import { AuthContext } from "@/lib/auth";
import { getMe } from "@/lib/api";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMe()
      .then((data) => setIsAdmin(data.is_admin))
      .catch(() => setIsAdmin(false))
      .finally(() => setLoading(false));
  }, []);

  return (
    <html lang="ja">
      <body>
        <AuthContext.Provider value={{ isAdmin, loading }}>
          <div className="flex min-h-screen">
            <Navbar />
            <main className="flex-1 p-6 bg-gray-50">{children}</main>
          </div>
        </AuthContext.Provider>
      </body>
    </html>
  );
}
