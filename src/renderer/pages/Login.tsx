import React, { useState } from 'react';
import { Card, Form, Input, Button, Alert, Typography, Space } from 'antd';
import {
  UserOutlined,
  LockOutlined,
  DashboardOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';

const { Title, Text } = Typography;

const Login: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const login = useAuthStore(state => state.login);

  const handleSubmit = async (values: {
    username: string;
    password: string;
  }) => {
    setLoading(true);
    setError(null);

    try {
      await login(values.username, values.password);
      navigate('/mapa');
    } catch (err: any) {
      setError(err.message || 'Error al iniciar sesión');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #001529 0%, #1890FF 100%)',
      }}
    >
      <Card
        style={{
          width: 450,
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
        }}
      >
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div style={{ textAlign: 'center' }}>
            <DashboardOutlined
              style={{ fontSize: 64, color: '#1890FF', marginBottom: 16 }}
            />
            <Title level={2} style={{ margin: 0 }}>
              SIGNA
            </Title>
            <Text type="secondary">
              Sistema de Inteligencia y Gestión de Análisis
            </Text>
            <br />
            <Text type="secondary" style={{ fontSize: 12 }}>
              Policía de Tucumán - Departamento de Inteligencia Criminal
            </Text>
          </div>

          {error && <Alert message={error} type="error" showIcon closable />}

          <Form
            name="login"
            onFinish={handleSubmit}
            layout="vertical"
            size="large"
          >
            <Form.Item
              name="username"
              rules={[
                { required: true, message: 'Por favor ingrese su usuario' },
              ]}
            >
              <Input prefix={<UserOutlined />} placeholder="Usuario" />
            </Form.Item>

            <Form.Item
              name="password"
              rules={[
                { required: true, message: 'Por favor ingrese su contraseña' },
              ]}
            >
              <Input.Password
                prefix={<LockOutlined />}
                placeholder="Contraseña"
              />
            </Form.Item>

            <Form.Item>
              <Button type="primary" htmlType="submit" loading={loading} block>
                Iniciar Sesión
              </Button>
            </Form.Item>
          </Form>

          <div style={{ textAlign: 'center' }}>
            <Text type="secondary" style={{ fontSize: 12 }}>
              Usuario de prueba: admin / Contraseña: admin123
            </Text>
          </div>
        </Space>
      </Card>
    </div>
  );
};

export default Login;
