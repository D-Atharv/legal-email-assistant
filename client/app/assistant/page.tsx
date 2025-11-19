/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState } from "react";
import { analyzeEmail, draftReply } from "@/lib/api";
import { EmailInput } from "@/components/EmailInput";
import { ContractInput } from "@/components/ContractInput";
import { JsonViewer } from "@/components/JsonViewer";
import { DraftPreview } from "@/components/DraftPreview";
import { Button } from "@/components/ui/button";
import { normalizeToJson } from "@/lib/json_converter";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

export default function IntelligentAssistantPage() {
  const [step, setStep] = useState(1);

  const [emailText, setEmailText] = useState("");
  const [analysisJson, setAnalysisJson] = useState("");
  const [analysisObj, setAnalysisObj] = useState<any>(null);
  const [contractText, setContractText] = useState("");
  const [draftOutput, setDraftOutput] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const gradientButtonClass =
    "bg-gradient-to-r from-orange-500 to-red-600 text-white font-semibold hover:from-orange-600 hover:to-red-700";

  async function handleAnalyze() {
    setLoading(true);
    setError("");

    try {
      const result = await analyzeEmail(emailText);
      setAnalysisObj(result);
      setAnalysisJson(JSON.stringify(result, null, 2));
      setStep(2);
    } catch (e: any) {
      setError(e.message || "Failed to analyze email.");
    }

    setLoading(false);
  }

  async function handleDraft() {
    setLoading(true);
    setError("");

    let normalizedAnalysis: any;
    try {
      normalizedAnalysis = normalizeToJson(analysisJson);
    } catch {
      setError("Invalid JSON or key-value format in analysis.");
      setLoading(false);
      return;
    }

    try {
      const res = await draftReply(emailText, normalizedAnalysis, contractText);
      setDraftOutput(res.draft);
      setStep(4);
    } catch (e: any) {
      setError(e.message || "Failed to draft reply.");
    }

    setLoading(false);
  }

  return (
    <div className="dark min-h-screen w-full bg-black text-white p-8 md:p-16">
      <main className="max-w-4xl mx-auto space-y-20">
        {/* ================================
            HEADER + SCROLL INDICATOR
        ================================= */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold">
            <span className="bg-linear-to-r from-yellow-400 via-orange-500 to-red-600 bg-clip-text text-transparent">
              Intelligent Assistant
            </span>
          </h1>

          <p className="text-gray-400 text-lg">
            A step-by-step workflow to analyze emails and draft legal replies.
          </p>

          {/* Scroll Indicator */}
          <div className="mt-6 animate-bounce text-gray-500">
            ▼ Scroll to begin
          </div>
        </div>

        {/* =====================================================
            STEP 1 — EMAIL INPUT
        ===================================================== */}
        <section>
          <h2 className="text-3xl font-semibold mb-6">Step 1: Analyze Email</h2>

          <Card className="bg-neutral-900 border-neutral-800">
            <CardHeader>
              <CardTitle className="text-2xl text-yellow-400">
                Enter Email
              </CardTitle>
            </CardHeader>

            <CardContent>
              <EmailInput value={emailText} onChange={setEmailText} />
            </CardContent>

            {step === 1 && (
              <CardFooter>
                <Button
                  onClick={handleAnalyze}
                  disabled={loading || !emailText}
                  className={gradientButtonClass}
                >
                  {loading ? "Analyzing..." : "Analyze Email"}
                </Button>
              </CardFooter>
            )}
          </Card>
        </section>

        {/* =====================================================
            STEP 2 — REVIEW / EDIT JSON ANALYSIS
        ===================================================== */}
        {step >= 2 && (
          <section>
            <h2 className="text-3xl font-semibold mb-6">
              Step 2: Review & Edit Analysis
            </h2>

            <Card className="bg-neutral-900 border-neutral-800">
              <CardHeader>
                <CardTitle className="text-2xl text-orange-400">
                  Editable JSON
                </CardTitle>
              </CardHeader>

              <CardContent className="space-y-4">
                <Textarea
                  className="w-full p-4 border rounded-lg h-64 font-mono bg-neutral-800 border-neutral-700 text-gray-200"
                  value={analysisJson}
                  onChange={(e) => setAnalysisJson(e.target.value)}
                />

                <label className="font-medium text-gray-300">Pretty View</label>
                <JsonViewer data={analysisObj} />
              </CardContent>

              {step === 2 && (
                <CardFooter>
                  <Button
                    onClick={() => setStep(3)}
                    variant="secondary"
                    className="bg-neutral-800 text-white hover:bg-neutral-700"
                  >
                    Confirm & Continue
                  </Button>
                </CardFooter>
              )}
            </Card>
          </section>
        )}

        {/* =====================================================
            STEP 3 — CONTRACT SNIPPET
        ===================================================== */}
        {step >= 3 && (
          <section>
            <h2 className="text-3xl font-semibold mb-6">
              Step 3: Provide Contract Snippet
            </h2>

            <Card className="bg-neutral-900 border-neutral-800">
              <CardHeader>
                <CardTitle className="text-2xl text-red-500">
                  Contract Input
                </CardTitle>
              </CardHeader>

              <CardContent>
                <ContractInput
                  value={contractText}
                  onChange={setContractText}
                />
              </CardContent>

              {step === 3 && (
                <CardFooter>
                  <Button
                    onClick={handleDraft}
                    disabled={loading}
                    className={gradientButtonClass}
                  >
                    {loading ? "Drafting..." : "Generate Draft Reply"}
                  </Button>
                </CardFooter>
              )}
            </Card>
          </section>
        )}

        {/* =====================================================
            STEP 4 — OUTPUT DRAFT
        ===================================================== */}
        {step === 4 && draftOutput && (
          <section>
            <h2 className="text-3xl font-semibold text-green-400 text-center mb-6">
              Final Draft Generated
            </h2>

            <DraftPreview text={draftOutput} />
          </section>
        )}

        {/* ERROR */}
        {error && (
          <p className="text-red-500 font-medium text-center text-lg p-4 bg-neutral-900 border border-red-800 rounded-lg">
            {error}
          </p>
        )}
      </main>
    </div>
  );
}
