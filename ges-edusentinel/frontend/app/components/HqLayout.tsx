import React from "react";

export default function HqLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[#0b1220] text-slate-100">
      <header className="border-b border-slate-800 p-4 flex items-center justify-between">
        <div className="font-semibold">GES EduSentinel Command Center</div>
        <a className="text-sm text-slate-300 hover:text-white" href="/dashboard">Dashboard</a>
      </header>
      <div className="p-6">{children}</div>
    </div>
  );
}
