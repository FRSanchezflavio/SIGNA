"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import CargaShapefile from "@/components/Mapa/CargaShapefile";
import { Shield } from "lucide-react";

// Dynamically import the map component to avoid SSR issues with Leaflet
const MapaInteractivo = dynamic(() => import("@/components/Mapa/MapaInteractivo"), {
  ssr: false,
  loading: () => <div className="h-[600px] w-full rounded-xl border bg-muted flex items-center justify-center">Cargando mapa...</div>
});

export default function MapaPage() {
  const [geoJsonData, setGeoJsonData] = useState<any | null>(null);

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-14 items-center">
          <div className="mr-4 hidden md:flex">
            <a className="mr-6 flex items-center space-x-2" href="/">
              <Shield className="h-6 w-6 text-primary" />
              <span className="hidden font-bold sm:inline-block">
                SIGNA
              </span>
            </a>
            <nav className="flex items-center space-x-6 text-sm font-medium">
              <a className="transition-colors hover:text-foreground/80 text-foreground/60" href="/">
                Dashboard
              </a>
              <a className="transition-colors hover:text-foreground/80 text-foreground" href="/mapa">
                Mapa del Delito
              </a>
              <a className="transition-colors hover:text-foreground/80 text-foreground/60" href="/analisis">
                Análisis
              </a>
              <a className="transition-colors hover:text-foreground/80 text-foreground/60" href="/reportes">
                Reportes
              </a>
            </nav>
          </div>
        </div>
      </header>
      <main className="flex-1 space-y-4 p-8 pt-6">
        <div className="flex items-center justify-between space-y-2">
          <h2 className="text-3xl font-bold tracking-tight">Mapa del Delito</h2>
        </div>
        
        <div className="grid gap-4 md:grid-cols-12">
          <div className="md:col-span-3 space-y-4">
            <CargaShapefile onDataLoaded={setGeoJsonData} />
            {/* Aquí se podrían agregar más controles de filtros en el futuro */}
          </div>
          
          <div className="md:col-span-9">
            <MapaInteractivo geoJsonData={geoJsonData} />
          </div>
        </div>
      </main>
    </div>
  );
}
