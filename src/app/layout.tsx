import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SIGNA - Centro Estadístico Policial",
  description: "Sistema de Inteligencia y Gestión de Análisis",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className="dark">
      <body className="min-h-screen bg-background font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
