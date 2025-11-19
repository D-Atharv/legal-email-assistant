"use client";

import { useEffect, useState } from "react";
import { JsonView, darkStyles } from "react-json-view-lite";

export function AuditLogViewer() {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [logs, setLogs] = useState<any[]>([]);

  useEffect(() => {
    const url = process.env.NEXT_PUBLIC_BACKEND_URL;

    if (!url) {
      // backend URL not configured; skip fetching
      console.log("Backend url empty");
      return;
    }

    fetch(url) // only if backend exposes this route
      .then((r) => r.json())
      .then(setLogs)
      .catch((err) => {
        // handle fetch errors gracefully
        console.error("Failed to fetch audit logs:", err);
      });
  }, []);

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold text-orange-400">Audit Logs</h2>

      {logs.length === 0 && (
        <p className="text-gray-400">No audit logs found.</p>
      )}

      {logs.map((log, i) => (
        <div
          key={i}
          className="border rounded-lg p-4 bg-neutral-900 border-neutral-800 shadow-sm"
        >
          <JsonView data={log} style={darkStyles} />
        </div>
      ))}
    </div>
  );
}
