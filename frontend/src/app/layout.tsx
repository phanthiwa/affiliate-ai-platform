import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Affiliate Growth OS | ระบบ AI ผลิตคอนเทนต์นายหน้า 15 คลิป/วัน",
  description: "AI Content Automation Platform for Thai Affiliate Creators with Google Flow & Multi-Platform Publishing",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="th" className="dark">
      <body className="bg-slate-950 text-slate-100 min-h-screen antialiased selection:bg-purple-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
