import { ClerkProvider } from "@clerk/nextjs";
import type { Metadata } from "next";

import { AppHeader } from "@/components/app-header";
import "./globals.css";

export const metadata: Metadata = {
  title: "ThesisRadar — Daily evidence for founders with a bet",
  description:
    "Thesis-driven signal engine. Is your problem hair-on-fire for this buyer — and who do you talk to next?",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className="min-h-screen bg-slate-950 text-slate-100 antialiased">
          <AppHeader />
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
