import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TibbWell — Discover Your Unani Temperament",
  description:
    "Take the free Unani-Tibb temperament quiz and unlock your personalised health programme. Discover your unique mind-body constitution with TibbWell.",
  keywords: [
    "Unani Tibb",
    "temperament quiz",
    "health programme",
    "wellness",
    "Sanguinous",
    "Phlegmatic",
    "Melancholic",
    "Bilious",
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen">{children}</body>
    </html>
  );
}
