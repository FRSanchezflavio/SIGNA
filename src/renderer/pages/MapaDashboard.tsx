import React, { useState } from 'react';
import { Row, Col, Card, Button, Space, Drawer } from 'antd';
import { PlusOutlined, FilterOutlined } from '@ant-design/icons';
import MapaInteractivo from '../components/Mapa/MapaInteractivo';
import FormularioRegistro from '../components/Mapa/FormularioRegistro';
import ControlCapas from '../components/Mapa/ControlCapas';

const MapaDashboard: React.FC = () => {
  const [drawerVisible, setDrawerVisible] = useState(false);
  const [capasVisible, setCapasVisible] = useState(false);
  const [coordenadasSeleccionadas, setCoordenadasSeleccionadas] = useState<{
    lat: number;
    lng: number;
  } | null>(null);

  const handleMapClick = (lat: number, lng: number) => {
    setCoordenadasSeleccionadas({ lat, lng });
    setDrawerVisible(true);
  };

  const handleCloseDrawer = () => {
    setDrawerVisible(false);
    setCoordenadasSeleccionadas(null);
  };

  const handleRegistroExitoso = () => {
    setDrawerVisible(false);
    setCoordenadasSeleccionadas(null);
    // TODO: Refrescar marcadores en el mapa
  };

  return (
    <div style={{ height: 'calc(100vh - 180px)' }}>
      <Card
        style={{ height: '100%' }}
        bodyStyle={{ padding: 0, height: '100%', position: 'relative' }}
      >
        {/* Controles flotantes */}
        <div
          style={{
            position: 'absolute',
            top: 16,
            right: 16,
            zIndex: 1000,
          }}
        >
          <Space direction="vertical">
            <Button
              type="primary"
              icon={<PlusOutlined />}
              size="large"
              onClick={() => setDrawerVisible(true)}
            >
              Nuevo Registro
            </Button>
            <Button
              icon={<FilterOutlined />}
              size="large"
              onClick={() => setCapasVisible(true)}
            >
              Capas
            </Button>
          </Space>
        </div>

        {/* Mapa */}
        <MapaInteractivo onMapClick={handleMapClick} />

        {/* Drawer de Registro */}
        <Drawer
          title="Registro de Evento Delictivo"
          placement="right"
          width={800}
          onClose={handleCloseDrawer}
          open={drawerVisible}
          className="registro-drawer"
        >
          <FormularioRegistro
            coordenadas={coordenadasSeleccionadas}
            onSuccess={handleRegistroExitoso}
            onCancel={handleCloseDrawer}
          />
        </Drawer>

        {/* Drawer de Control de Capas */}
        <Drawer
          title="Control de Capas"
          placement="left"
          width={400}
          onClose={() => setCapasVisible(false)}
          open={capasVisible}
        >
          <ControlCapas />
        </Drawer>
      </Card>
    </div>
  );
};

export default MapaDashboard;
