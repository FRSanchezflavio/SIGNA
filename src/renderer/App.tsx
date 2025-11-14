import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './components/Layout/MainLayout';
import Login from './pages/Login';
import MapaDashboard from './pages/MapaDashboard';
import AnalisisEstadistico from './pages/AnalisisEstadistico';
import InteligenciaAvanzada from './pages/InteligenciaAvanzada';
import Configuracion from './pages/Configuracion';
import { useAuthStore } from './stores/authStore';

const App: React.FC = () => {
  const isAuthenticated = useAuthStore(state => state.isAuthenticated);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        {isAuthenticated ? (
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Navigate to="/mapa" replace />} />
            <Route path="mapa" element={<MapaDashboard />} />
            <Route path="analisis" element={<AnalisisEstadistico />} />
            <Route path="mia" element={<InteligenciaAvanzada />} />
            <Route path="configuracion" element={<Configuracion />} />
          </Route>
        ) : (
          <Route path="*" element={<Navigate to="/login" replace />} />
        )}
      </Routes>
    </BrowserRouter>
  );
};

export default App;
