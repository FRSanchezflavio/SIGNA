"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Upload, AlertCircle, CheckCircle2 } from "lucide-react";

interface CargaShapefileProps {
  onDataLoaded: (data: any) => void;
}

export default function CargaShapefile({ onDataLoaded }: CargaShapefileProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
      setSuccess(false);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Por favor seleccione un archivo ZIP.");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/api/upload-shapefile", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Error al cargar el archivo.");
      }

      // Parse GeoJSON string if it's a string, otherwise use as is
      const geoJson = typeof data.data === 'string' ? JSON.parse(data.data) : data.data;
      
      onDataLoaded(geoJson);
      setSuccess(true);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Cargar Capa Geográfica</CardTitle>
        <CardDescription>
          Suba un archivo ZIP con los archivos Shapefile (.shp, .shx, .dbf) exportados de QGIS.
          <br />
          <span className="text-xs text-muted-foreground">
            Compatibilidad optimizada para QGIS 2.14 "Essen" y codificaciones antiguas (Latin1/System).
          </span>
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid w-full max-w-sm items-center gap-1.5">
          <Label htmlFor="shapefile">Archivo ZIP</Label>
          <Input id="shapefile" type="file" accept=".zip" onChange={handleFileChange} />
        </div>
        
        {error && (
          <div className="flex items-start text-destructive text-sm p-3 bg-destructive/10 rounded-md">
            <AlertCircle className="mr-2 h-4 w-4 mt-0.5 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="flex items-center text-green-600 text-sm p-3 bg-green-50 rounded-md">
            <CheckCircle2 className="mr-2 h-4 w-4" />
            Carga exitosa. Capa visualizada en el mapa.
          </div>
        )}

        <Button onClick={handleUpload} disabled={loading || !file} className="w-full sm:w-auto">
          {loading ? (
            <>Cargando...</>
          ) : (
            <>
              <Upload className="mr-2 h-4 w-4" />
              Procesar y Visualizar
            </>
          )}
        </Button>
      </CardContent>
    </Card>
  );
}
