import React from 'react';
import { Typography } from 'antd';

const { Title } = Typography;

const Configuracion: React.FC = () => {
  return (
    <div>
      <Title level={2}>Configuración</Title>
      <p>Configuración del sistema y preferencias del usuario</p>
    </div>
  );
};

export default Configuracion;
