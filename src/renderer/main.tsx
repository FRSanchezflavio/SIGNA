import React from 'react';
import ReactDOM from 'react-dom/client';
import { ConfigProvider } from 'antd';
import esES from 'antd/locale/es_ES';
import dayjs from 'dayjs';
import 'dayjs/locale/es';
import App from './App';
import './styles/global.css';

// Configurar dayjs en español
dayjs.locale('es');

// Tema personalizado de SIGNA
const theme = {
  token: {
    colorPrimary: '#1890FF',
    colorSuccess: '#52C41A',
    colorWarning: '#FAAD14',
    colorError: '#F5222D',
    colorInfo: '#1890FF',
    fontSize: 14,
    borderRadius: 4,
    fontFamily:
      'Roboto, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif',
  },
  components: {
    Layout: {
      headerBg: '#001529',
      siderBg: '#001529',
    },
    Menu: {
      darkItemBg: '#001529',
      darkItemSelectedBg: '#1890FF',
    },
    Button: {
      primaryColor: '#1890FF',
    },
    Form: {
      labelFontSize: 14,
      itemMarginBottom: 16,
    },
  },
};

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ConfigProvider theme={theme} locale={esES}>
      <App />
    </ConfigProvider>
  </React.StrictMode>
);
