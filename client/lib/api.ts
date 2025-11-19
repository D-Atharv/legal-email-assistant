// frontend/lib/api.ts
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type AnalysisResult = any;

const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

/**
 * POST /analyze
 * Request: { email_text: string, contract_text?: string }
 * Response: JSON analysis
 */
export async function analyzeEmail(
  emailText: string,
  contractText?: string
): Promise<AnalysisResult> {
  const url = `${BACKEND_URL}/analyze/`;
  const body = {
    email_text: emailText,
    contract_text: contractText ?? null,
  };

  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(
      `Analyze failed: ${res.status} ${res.statusText} — ${text}`
    );
  }

  const json = await res.json();
  return json;
}

/**
 * POST /draft
 * Request: { email_text, analysis, contract_text }
 * Response: { draft: string }
 */
export async function draftReply(
  emailText: string,
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  analysis: any,
  contractText: string
): Promise<{ draft: string }> {
  const url = `${BACKEND_URL}/draft/`;
  const body = {
    email_text: emailText,
    analysis,
    contract_text: contractText,
  };

  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Draft failed: ${res.status} ${res.statusText} — ${text}`);
  }

  const json = await res.json();
  return json;
}

/**
 * Optional: fetch audit logs (if backend exposes GET /audit)
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export async function fetchAuditLogs(): Promise<any[]> {
  const url = `${BACKEND_URL}/audit/`;
  const res = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) {
    return [];
  }

  return res.json();
}
