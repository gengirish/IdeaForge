import { ClerkProvider } from "@clerk/nextjs";
import type { Metadata } from "next";

import { AppHeader } from "@/components/app-header";
import "./globals.css";

const siteDescription =
  "ThesisRadar is customer discovery SaaS for founders with an active thesis — not hardware radar. Daily evidence-grade signals from Reddit, HN, and G2 with source receipts and interview targets.";

export const metadata: Metadata = {
  title: "ThesisRadar — Customer discovery SaaS for founders with a bet",
  description: siteDescription,
};

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "ThesisRadar",
  applicationCategory: "BusinessApplication",
  operatingSystem: "Web",
  description:
    "Customer discovery SaaS for thesis-driven founders. Daily signals from Reddit, HN, and G2 — software for evidence-grade customer discovery, not physical radar hardware.",
  offers: {
    "@type": "Offer",
    price: "49",
    priceCurrency: "USD",
    priceSpecification: {
      "@type": "UnitPriceSpecification",
      price: "49",
      priceCurrency: "USD",
      billingDuration: "P1M",
    },
  },
  provider: {
    "@type": "Organization",
    name: "IntelliForge",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <head>
          <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
          />
        </head>
        <body className="min-h-screen bg-slate-950 text-slate-100 antialiased">
          <AppHeader />
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
