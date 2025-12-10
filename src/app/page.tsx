import { Activity, BarChart3, FileText, Map, Shield, Users } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function Dashboard() {
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
              <a className="transition-colors hover:text-foreground/80 text-foreground" href="/">
                Dashboard
              </a>
              <a className="transition-colors hover:text-foreground/80 text-foreground/60" href="/mapa">
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
          <h2 className="text-3xl font-bold tracking-tight">Dashboard Estratégico</h2>
          <div className="flex items-center space-x-2">
            <Button>Descargar Reporte</Button>
          </div>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Incidentes</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">2,350</div>
              <p className="text-xs text-muted-foreground">+20.1% respecto al mes anterior</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Operativos Activos</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">+573</div>
              <p className="text-xs text-muted-foreground">+201 desde la última hora</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Tasa de Resolución</CardTitle>
              <BarChart3 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">12.5%</div>
              <p className="text-xs text-muted-foreground">+4% respecto al mes anterior</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Alertas Críticas</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">7</div>
              <p className="text-xs text-muted-foreground">Requieren atención inmediata</p>
            </CardContent>
          </Card>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
          <Card className="col-span-4">
            <CardHeader>
              <CardTitle>Resumen Semanal</CardTitle>
              <CardDescription>Tendencia de delitos en los últimos 7 días.</CardDescription>
            </CardHeader>
            <CardContent className="pl-2">
              <div className="h-[200px] w-full bg-muted/10 flex items-center justify-center rounded-md border border-dashed">
                <span className="text-muted-foreground">Gráfico de Tendencias (Placeholder)</span>
              </div>
            </CardContent>
          </Card>
          <Card className="col-span-3">
            <CardHeader>
              <CardTitle>Actividad Reciente</CardTitle>
              <CardDescription>Últimos eventos registrados.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-8">
                <div className="flex items-center">
                  <div className="space-y-1">
                    <p className="text-sm font-medium leading-none">Robo en vía pública</p>
                    <p className="text-sm text-muted-foreground">San Miguel de Tucumán - Hace 10 min</p>
                  </div>
                  <div className="ml-auto font-medium text-destructive">Alta Prioridad</div>
                </div>
                <div className="flex items-center">
                  <div className="space-y-1">
                    <p className="text-sm font-medium leading-none">Control Vehicular</p>
                    <p className="text-sm text-muted-foreground">Yerba Buena - Hace 45 min</p>
                  </div>
                  <div className="ml-auto font-medium text-primary">En Curso</div>
                </div>
                <div className="flex items-center">
                  <div className="space-y-1">
                    <p className="text-sm font-medium leading-none">Denuncia Civil</p>
                    <p className="text-sm text-muted-foreground">Comisaría 1ra - Hace 1h</p>
                  </div>
                  <div className="ml-auto font-medium text-muted-foreground">Registrado</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
