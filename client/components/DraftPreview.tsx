"use client";

import { Card, CardContent } from "@/components/ui/card";

export function DraftPreview({ text }: { text: string }) {
  return (
    <Card className="mt-6 bg-neutral-900 border-neutral-800 shadow-lg">
      <CardContent className="whitespace-pre-wrap p-6 leading-relaxed text-gray-200 text-lg">
        {text}
      </CardContent>
    </Card>
  );
}
