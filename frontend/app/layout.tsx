import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ScreeningProvider } from "@/context/ScreeningContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Dementia Detection System",
  description: "AI-Powered Multimodal Dementia Detection",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ScreeningProvider>
          {children}
        </ScreeningProvider>
      </body>
    </html>
  );
}
