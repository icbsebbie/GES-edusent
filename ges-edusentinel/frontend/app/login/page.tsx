"use client";

import { useState } from "react";
import { api } from "../lib/api";
import { saveToken } from "../lib/auth";

export default function LoginPage() {
  const [email, setEmail] = useState("admin@ges.local");
  const [password, setPassword] = useState("admin123");
  const [error, setError] = useState("");

  async function onLogin() {
    setError("");
    try {
      const res = await api("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      saveToken(data.access_token);
      window.location.href = "/dashboard";
    } catch (e: any) {
      setError(e.message);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <div className="p-6 bg-white border rounded w-[420px]">
        <h1 className="text-xl font-semibold">Login</h1>
        <div className="mt-4 space-y-3">
          <input className="w-full border rounded p-2" value={email} onChange={(e)=>setEmail(e.target.value)} />
          <input className="w-full border rounded p-2" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} />
          {error && <div className="text-red-600 text-sm">{error}</div>}
          <button className="w-full px-4 py-2 rounded bg-slate-900 text-white" onClick={onLogin}>
            Sign in
          </button>
        </div>
      </div>
    </div>
  );
}
