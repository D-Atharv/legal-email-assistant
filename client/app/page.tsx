// /* eslint-disable @typescript-eslint/no-explicit-any */
// "use client";

// import Link from "next/link";
// import { Button } from "@/components/ui/button";
// import {
//   Card,
//   CardContent,
//   CardDescription,
//   CardFooter,
//   CardHeader,
//   CardTitle,
// } from "@/components/ui/card";
// import { Check } from "lucide-react";

// export default function HomePage() {
//   return (
//     <div className="dark min-h-screen w-full bg-black text-white p-8 md:p-16">
//       <div className="max-w-7xl mx-auto">
//         <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
//           {/* Main Hero Box */}
//           <Card className="lg:col-span-2 bg-neutral-900 border-neutral-800 p-6 md:p-10 flex flex-col justify-between">
//             <div>
//               <CardTitle className="text-5xl md:text-6xl font-bold">
//                 <span className="bg-linear-to-r from-yellow-400 via-orange-500 to-red-600 bg-clip-text text-transparent">
//                   Legal Email Assistant
//                 </span>
//               </CardTitle>
//               <CardDescription className="text-gray-300 text-lg md:text-xl mt-4 max-w-2xl">
//                 Analyze legal emails and draft professional replies using AI,
//                 MCP tools, and contract clauses.
//               </CardDescription>
//             </div>
//             <CardFooter className="p-0 pt-8">
//               <Link href="/assistant">
//                 <Button
//                   size="lg"
//                   className="text-lg font-semibold bg-linear-to-r from-orange-500 to-red-600 text-white hover:from-orange-600 hover:to-red-700"
//                 >
//                   Get Started
//                 </Button>
//               </Link>
//             </CardFooter>
//           </Card>

//           {/* Features Box */}
//           <Card className="bg-neutral-900 border-neutral-800">
//             <CardHeader>
//               <CardTitle className="text-2xl text-orange-400">
//                 Key Features
//               </CardTitle>
//             </CardHeader>
//             <CardContent className="space-y-3">
//               {[
//                 "AI-Powered Analysis",
//                 "Contextual Drafts",
//                 "Contract Clause Integration",
//                 "Editable JSON Output",
//               ].map((feature) => (
//                 <div key={feature} className="flex items-center space-x-2">
//                   <Check className="h-5 w-5 text-green-500" />
//                   <span className="text-gray-300">{feature}</span>
//                 </div>
//               ))}
//             </CardContent>
//           </Card>

//           {/* Step Boxes */}
//           <Card className="bg-neutral-900 border-neutral-800">
//             <CardHeader>
//               <CardTitle className="text-2xl font-semibold text-yellow-400">
//                 1. Analyze
//               </CardTitle>
//             </CardHeader>
//             <CardContent>
//               <p className="text-gray-400">
//                 Paste an email to instantly extract key points, sentiment, and
//                 legal queries.
//               </p>
//             </CardContent>
//           </Card>

//           <Card className="bg-neutral-900 border-neutral-800">
//             <CardHeader>
//               <CardTitle className="text-2xl font-semibold text-orange-400">
//                 2. Review
//               </CardTitle>
//             </CardHeader>
//             <CardContent>
//               <p className="text-gray-400">
//                 Edit the AIs JSON analysis to ensure 100% accuracy before
//                 drafting.
//               </p>
//             </CardContent>
//           </Card>

//           <Card className="bg-neutral-900 border-neutral-800">
//             <CardHeader>
//               <CardTitle className="text-2xl font-semibold text-red-500">
//                 3. Draft
//               </CardTitle>
//             </CardHeader>
//             <CardContent>
//               <p className="text-gray-400">
//                 Generate a professional reply based on the analysis and your
//                 provided contract clauses.
//               </p>
//             </CardContent>
//           </Card>
//         </div>
//       </div>
//     </div>
//   );
// }

"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Check } from "lucide-react";

export default function HomePage() {
  return (
    <div className="dark relative min-h-screen w-full overflow-hidden bg-black text-white p-8 md:p-16">
      {/* ————— GRID BACKGROUND ————— */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.08),transparent_70%)]" />
      <div className="pointer-events-none absolute inset-0 bg-[url('/grid.svg')] opacity-10 mix-blend-soft-light" />

      <div className="relative max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* ————— HERO SECTION ————— */}
          <Card className="lg:col-span-2 bg-neutral-900/60 border-neutral-800 p-8 md:p-12 backdrop-blur-md flex flex-col justify-between">
            <div>
              <CardTitle className="text-5xl md:text-6xl font-extrabold leading-tight tracking-tight">
                <span className="bg-linear-to-r from-yellow-400 via-orange-500 to-red-600 bg-clip-text text-transparent">
                  Legal Email Assistant
                </span>
              </CardTitle>

              <CardDescription className="text-gray-300 text-xl md:text-2xl mt-6 max-w-2xl leading-relaxed">
                A next-generation tool that analyzes legal emails, extracts
                intent, references contract clauses, and drafts accurate,
                professional responses in seconds.
              </CardDescription>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-10">
                <div className="text-gray-300">
                  <h3 className="text-lg font-semibold text-orange-400">
                    Why this tool?
                  </h3>
                  <p className="mt-2 text-gray-400">
                    Legal email writing is slow, complex, and error-prone. This
                    assistant ensures precision, compliance, and clarity — every
                    single time.
                  </p>
                </div>
                <div className="text-gray-300">
                  <h3 className="text-lg font-semibold text-yellow-400">
                    Powered by MCP + LLMs
                  </h3>
                  <p className="mt-2 text-gray-400">
                    Run structured parsers through MCP tools, combine them with
                    LLM reasoning, and generate actionable legal responses
                    instantly.
                  </p>
                </div>
              </div>
            </div>

            <CardFooter className="p-0 pt-12">
              <Link href="/assistant">
                <Button
                  size="lg"
                  className="text-lg px-8 py-6 font-semibold bg-linear-to-r from-orange-500 to-red-600 text-white hover:from-orange-600 hover:to-red-700 shadow-lg shadow-red-900/30"
                >
                  Get Started
                </Button>
              </Link>
            </CardFooter>
          </Card>

          {/* ————— FEATURES ————— */}
          <Card className="bg-neutral-900/60 border-neutral-800 backdrop-blur-md">
            <CardHeader>
              <CardTitle className="text-3xl text-orange-400">
                Key Features
              </CardTitle>
              <CardDescription className="text-gray-400 mt-2">
                Everything you need for fast, compliant legal communication.
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4 pt-2">
              {[
                "AI-Powered Email Interpretation",
                "Intent, Facts & Legal Query Extraction",
                "Clause-Based Draft Generation",
                "Editable JSON Analyzer (no black-box)",
                "MCP Tool Integration for Accuracy",
                "Context-Aware Professional Responses",
              ].map((feature) => (
                <div key={feature} className="flex items-start space-x-3">
                  <Check className="h-5 w-5 text-green-500 mt-1" />
                  <span className="text-gray-300 leading-tight">{feature}</span>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* ————— STEPS ————— */}
          {[
            {
              title: "1. Analyze",
              color: "text-yellow-400",
              text: "Paste an email. The system extracts intent, tone, entities, clauses, and legal questions.",
            },
            {
              title: "2. Review",
              color: "text-orange-400",
              text: "Edit the structured JSON analysis. Maintain full control over facts and interpretation.",
            },
            {
              title: "3. Draft",
              color: "text-red-500",
              text: "Generate polished, compliant replies aligned with your contract clauses and policies.",
            },
          ].map((step) => (
            <Card
              key={step.title}
              className="bg-neutral-900/60 border-neutral-800 backdrop-blur-md"
            >
              <CardHeader>
                <CardTitle className={`text-2xl font-semibold ${step.color}`}>
                  {step.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-400">{step.text}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* ————— BOTTOM CTA ————— */}
        <div className="mt-20 text-center">
          <h2 className="text-3xl md:text-4xl font-bold bg-clip-text text-transparent bg-linear-to-r from-yellow-400 to-red-600">
            Ready to supercharge your legal workflow?
          </h2>
          <p className="text-gray-400 mt-4 max-w-2xl mx-auto">
            Start analyzing emails with precision, reduce manual effort, and
            deliver legally sound responses faster than ever before.
          </p>

          <Link href="/assistant">
            <Button className="mt-8 px-10 py-6 text-lg bg-linear-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 shadow-lg shadow-red-900/30">
              Launch Assistant
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
