// Global Layout wrapper that loads fonts, sets page metadata and wraps every route, apply global
// CSS

import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

// Load Giest font and assign it as a CSS variable
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// Metadata for what appears in the browser tab and search engine results
export const metadata: Metadata = {
  title: "Lobang",
  description: "Your Student Discount Radar",
};

// children == whatever page is currently being visited
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
