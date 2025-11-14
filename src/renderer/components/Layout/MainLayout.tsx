import React from 'react';
import { Layout, Menu, Avatar, Dropdown, Space, Typography } from 'antd';
import {
  UserOutlined,
  LogoutOutlined,
  SettingOutlined,
  DashboardOutlined,
  BarChartOutlined,
  BulbOutlined,
  EnvironmentOutlined,
} from '@ant-design/icons';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../stores/authStore';
import type { MenuProps } from 'antd';

const { Header, Sider, Content, Footer } = Layout;
const { Text } = Typography;

const MainLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { usuario, logout } = useAuthStore();

  const menuItems: MenuProps['items'] = [
    {
      key: '/mapa',
      icon: <EnvironmentOutlined />,
      label: 'Mapa Delictual',
    },
    {
      key: '/analisis',
      icon: <BarChartOutlined />,
      label: 'Análisis Estadístico',
    },
    {
      key: '/mia',
      icon: <BulbOutlined />,
      label: 'Inteligencia Avanzada',
    },
    {
      key: '/configuracion',
      icon: <SettingOutlined />,
      label: 'Configuración',
    },
  ];

  const userMenuItems: MenuProps['items'] = [
    {
      key: 'perfil',
      icon: <UserOutlined />,
      label: 'Mi Perfil',
    },
    {
      key: 'configuracion',
      icon: <SettingOutlined />,
      label: 'Configuración',
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Cerrar Sesión',
      onClick: () => {
        logout();
        navigate('/login');
      },
    },
  ];

  const handleMenuClick: MenuProps['onClick'] = e => {
    navigate(e.key);
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <DashboardOutlined style={{ fontSize: '24px', color: '#fff' }} />
          <Text style={{ color: '#fff', fontSize: '18px', fontWeight: 600 }}>
            SIGNA
          </Text>
        </div>

        <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
          <Space style={{ cursor: 'pointer' }}>
            <Avatar icon={<UserOutlined />} />
            <Text style={{ color: '#fff' }}>
              {usuario?.nombre} {usuario?.apellido}
            </Text>
            <Text style={{ color: '#8C8C8C', fontSize: '12px' }}>
              {usuario?.rol}
            </Text>
          </Space>
        </Dropdown>
      </Header>

      <Layout>
        <Sider width={250} theme="dark">
          <Menu
            mode="inline"
            selectedKeys={[location.pathname]}
            items={menuItems}
            onClick={handleMenuClick}
            theme="dark"
          />
        </Sider>

        <Layout>
          <Content style={{ margin: '24px', minHeight: 280 }}>
            <Outlet />
          </Content>

          <Footer style={{ textAlign: 'center', background: '#fafafa' }}>
            SIGNA ©{new Date().getFullYear()} - Policía de Tucumán -
            Departamento de Inteligencia Criminal
          </Footer>
        </Layout>
      </Layout>
    </Layout>
  );
};

export default MainLayout;
