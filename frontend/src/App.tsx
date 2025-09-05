import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import { Layout } from 'antd';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import CustomerAnalysis from './pages/CustomerAnalysis';
import AIChat from './pages/AIChat';
import CallCenter from './pages/CallCenter';
import ComputerVision from './pages/ComputerVision';
import './App.css';

const { Content } = Layout;

const App: React.FC = () => {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1890ff',
          borderRadius: 6,
        },
      }}
    >
      <Router>
        <Layout style={{ minHeight: '100vh' }}>
          <Sidebar />
          <Layout>
            <Content style={{ margin: '24px 16px', padding: 24, background: '#fff', borderRadius: 8 }}>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/analysis" element={<CustomerAnalysis />} />
                <Route path="/chat" element={<AIChat />} />
                <Route path="/call-center" element={<CallCenter />} />
                <Route path="/computer-vision" element={<ComputerVision />} />
              </Routes>
            </Content>
          </Layout>
        </Layout>
      </Router>
    </ConfigProvider>
  );
};

export default App;
