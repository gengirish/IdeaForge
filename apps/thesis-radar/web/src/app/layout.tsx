import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ThesisRadar — Daily evidence for founders with a bet",
  description:
    "Thesis-driven signal engine. Is your problem hair-on-fire for this buyer — and who do you talk to next?",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased">{children}</body>
    </html>
  );
}
