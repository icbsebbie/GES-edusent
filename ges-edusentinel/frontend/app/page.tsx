export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <div className="p-6 bg-white border rounded w-[420px]">
        <h1 className="text-xl font-semibold">GES EduSentinel</h1>
        <p className="text-sm text-slate-600 mt-2">Education Intelligence System</p>
        <a className="mt-4 inline-block px-4 py-2 rounded bg-slate-900 text-white" href="/login">
          Login
        </a>
      </div>
    </div>
  );
}
