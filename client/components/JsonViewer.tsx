"use client";

import { JsonView, darkStyles } from "react-json-view-lite";
import "react-json-view-lite/dist/index.css";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function JsonViewer({ data }: { data: any }) {
  return (
    <div className="p-4 border rounded-lg bg-neutral-900 border-neutral-700 shadow-sm overflow-x-auto">
      <JsonView data={data} style={darkStyles} />
    </div>
  );
}
