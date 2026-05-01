import React from "react";

export default function SchoolLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="flex">
        <aside className="w-64 bg-white border-r min-h-screen p-4">
          <div className="font-bold text-lg">SchoolFlow</div>
          <nav className="mt-4 space-y-2 text-sm">
            <a className="block p-2 rounded hover:bg-slate-100" href="/dashboard">Overview</a>
            <a className="block p-2 rounded hover:bg-slate-100" href="/dashboard?tab=submissions">Data Collection</a>
            <a className="block p-2 rounded hover:bg-slate-100" href="/dashboard?tab=reports">Reports</a>
          </nav>
        </aside>
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}
