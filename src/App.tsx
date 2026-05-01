/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
      <div className="bg-white p-8 rounded-lg shadow-sm border max-w-xl w-full text-center">
        <h1 className="text-2xl font-semibold mb-4 text-slate-900">Project Scaffolded Successfully</h1>
        <p className="text-slate-600 mb-6 leading-relaxed">
          The <strong>GES EduSentinel</strong> backend (Python/FastAPI) and frontend (Next.js) code base you provided has been fully scaffolded into the <code>ges-edusentinel/</code> directory, including the completed <code>dashboard/page.tsx</code>.
        </p>
        
        <div className="bg-blue-50 text-blue-800 p-4 rounded text-sm text-left mb-6 border border-blue-100">
          <strong>Note on Environment:</strong> This preview environment natively runs a single Node.js container, so it cannot spin up the provided Docker Compose stack (Postgres, Redis, Python, Celery, n8n). 
        </div>

        <p className="text-md text-slate-700 font-medium mb-2">How to run it:</p>
        <ul className="text-left text-sm text-slate-600 space-y-2 list-disc pl-8 mb-8">
          <li>Click the <strong>Settings (gear) icon</strong> at the top right of the editor.</li>
          <li>Select <strong>Export to ZIP</strong> or <strong>Export to GitHub</strong>.</li>
          <li>Once exported, navigate to the <code>ges-edusentinel/</code> directory on your machine.</li>
          <li>Run <code>docker-compose up --build</code> to start all services.</li>
        </ul>
      </div>
    </div>
  );
}
