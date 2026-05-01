"use client";

import { useEffect, useMemo, useState } from "react";
import { api } from "../lib/api";
import SchoolLayout from "../components/SchoolLayout";
import HqLayout from "../components/HqLayout";

export default function Dashboard() {
  const [me, setMe] = useState<any>(null);
  const [completion, setCompletion] = useState<any>(null);
  const [termId, setTermId] = useState<number>(1);
  const [dataset, setDataset] = useState<string>("attendance");
  const [msg, setMsg] = useState<string>("");

  const isHq = useMemo(() => me?.role?.includes("HQ"), [me]);

  useEffect(() => {
    (async () => {
      try {
        const res = await api("/api/auth/me");
        setMe(await res.json());
      } catch (e) {
        window.location.href = "/login";
      }
    })();
  }, []);

  async function loadCompletion() {
    setMsg("");
    try {
      const res = await api(`/api/analytics/completion?term_id=${termId}&dataset=${dataset}`);
      setCompletion(await res.json());
    } catch (e: any) {
      setMsg(e.message);
    }
  }

  async function deepScan() {
    setMsg("Queued DeepScan...");
    try {
      const res = await api(`/api/analytics/deepscan?term_id=${termId}&dataset=${dataset}`, { method: "POST" });
      const data = await res.json();
      setMsg(`DeepScan queued. Job ID: ${data.job_id}`);
    } catch (e: any) {
      setMsg(e.message);
    }
  }

  const Layout = isHq ? HqLayout : SchoolLayout;

  return (
    <Layout>
      <div className={isHq ? "max-w-5xl mx-auto" : "max-w-6xl"}>
        <h1 className="text-2xl font-semibold">
          {isHq ? "HQ / Regional Intelligence" : "School Overview"}
        </h1>

        {me && (
          <div className={isHq ? "mt-2 text-slate-300 text-sm" : "mt-2 text-slate-600 text-sm"}>
            Welcome, {me.full_name} ({me.role}). Connected to {me.org_unit?.name}
          </div>
        )}

        <div className="mt-8 space-y-6">
           <div className={`p-4 border rounded ${isHq ? 'bg-slate-900 border-slate-700' : 'bg-white'}`}>
             <h2 className="text-lg font-medium mb-4">Analytics & DeepScan</h2>
             
             <div className="flex items-end gap-4 mb-4">
               <div>
                  <label className="block text-sm mb-1 opacity-80">Term ID</label>
                  <input type="number" className={`border p-2 rounded w-24 ${isHq ? 'bg-slate-800 border-slate-700 text-white' : 'text-black'}`} value={termId} onChange={(e)=>setTermId(parseInt(e.target.value)||1)} />
               </div>
               <div>
                  <label className="block text-sm mb-1 opacity-80">Dataset</label>
                  <input type="text" className={`border p-2 rounded ${isHq ? 'bg-slate-800 border-slate-700 text-white' : 'text-black'}`} value={dataset} onChange={(e)=>setDataset(e.target.value)} />
               </div>
               <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition" onClick={loadCompletion}>
                 Load Completion
               </button>
               {isHq && (
                 <button className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 transition" onClick={deepScan}>
                   Run DeepScan
                 </button>
               )}
             </div>

             {msg && <div className="text-sm p-2 bg-blue-50 text-blue-800 border border-blue-200 rounded my-2">{msg}</div>}

             {completion && (
               <div className={`mt-4 p-4 rounded border ${isHq ? 'bg-slate-800 border-slate-700' : 'bg-slate-50'}`}>
                 <h3 className="font-semibold mb-2">Completion Results</h3>
                 <div className="grid grid-cols-3 gap-4">
                    <div>
                      <div className="text-sm opacity-70">Total Schools</div>
                      <div className="text-xl font-bold">{completion.total_schools}</div>
                    </div>
                    <div>
                      <div className="text-sm opacity-70">Submitted</div>
                      <div className="text-xl font-bold">{completion.submitted}</div>
                    </div>
                    <div>
                      <div className="text-sm opacity-70">Rate</div>
                      <div className="text-xl font-bold">{Math.round(completion.completion_rate * 100)}%</div>
                    </div>
                 </div>
               </div>
             )}
           </div>

           <div className={`p-4 border rounded ${isHq ? 'bg-slate-900 border-slate-700' : 'bg-white'}`}>
              <h2 className="text-lg font-medium mb-4">Reports</h2>
              <div className="flex flex-wrap gap-4">
                 <a href={`/api/reports/term.docx?term_id=${termId}&dataset=${dataset}`} className="text-blue-500 hover:text-blue-400 hover:underline">Download DOCX</a>
                 <a href={`/api/reports/term.pdf?term_id=${termId}&dataset=${dataset}`} className="text-blue-500 hover:text-blue-400 hover:underline">Download PDF</a>
              </div>
           </div>
        </div>
      </div>
    </Layout>
  );
}
