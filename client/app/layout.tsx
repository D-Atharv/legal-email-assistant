import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Legal Email Assistant",
  description: "Analyze legal email & draft replies using AI + MCP",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 text-gray-900">
        <div>
          {children}
        </div>
      </body>
    </html>
  );
}
