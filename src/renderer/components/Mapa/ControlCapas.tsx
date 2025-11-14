import React from 'react';
import { Tree, Switch, Space, Typography } from 'antd';
import type { DataNode } from 'antd/es/tree';

const { Title, Text } = Typography;

const ControlCapas: React.FC = () => {
  const capasData: DataNode[] = [
    {
      title: 'Capas Base',
      key: 'base',
      children: [
        { title: 'OpenStreetMap', key: 'osm' },
        { title: 'Satelital', key: 'satelital' },
      ],
    },
    {
      title: 'Capas Delictivas',
      key: 'delictivas',
      children: [
        { title: 'Eventos Delictivos', key: 'eventos' },
        { title: 'Mapa de Calor', key: 'calor' },
        { title: 'Hotspots', key: 'hotspots' },
      ],
    },
    {
      title: 'Capas Administrativas',
      key: 'admin',
      children: [
        { title: 'Comisarías', key: 'comisarias' },
        { title: 'Jurisdicciones', key: 'jurisdicciones' },
        { title: 'Rutas y Calles', key: 'rutas' },
      ],
    },
    {
      title: 'Capas Personalizadas',
      key: 'personalizadas',
      children: [],
    },
  ];

  return (
    <div>
      <Title level={4}>Control de Capas</Title>
      <Text type="secondary">Seleccione las capas a visualizar en el mapa</Text>

      <div style={{ marginTop: 24 }}>
        <Tree checkable defaultExpandAll treeData={capasData} />
      </div>
    </div>
  );
};

export default ControlCapas;
