export default function AnalisisPage() {
  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Análisis Estadístico</h2>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-6">
          <h3 className="font-semibold">Correlaciones</h3>
          <p className="text-sm text-muted-foreground mt-2">Análisis de variables correlacionadas.</p>
        </div>
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-6">
          <h3 className="font-semibold">Predicciones</h3>
          <p className="text-sm text-muted-foreground mt-2">Modelos predictivos de tendencias.</p>
        </div>
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-6">
          <h3 className="font-semibold">Comparativas</h3>
          <p className="text-sm text-muted-foreground mt-2">Comparación entre periodos y zonas.</p>
        </div>
      </div>
    </div>
  );
}
