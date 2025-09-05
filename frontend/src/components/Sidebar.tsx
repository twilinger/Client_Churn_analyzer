import React from 'react';
import { Layout, Menu } from 'antd';
import { 
  DashboardOutlined, 
  UserOutlined, 
  MessageOutlined, 
  PhoneOutlined,
  EyeOutlined,
  RobotOutlined
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';

const { Sider } = Layout;

const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
    },
    {
      key: '/analysis',
      icon: <UserOutlined />,
      label: 'Customer Analysis',
    },
    {
      key: '/chat',
      icon: <RobotOutlined />,
      label: 'AI Assistant',
    },
    {
      key: '/call-center',
      icon: <PhoneOutlined />,
      label: 'Call Center AI',
    },
    {
      key: '/computer-vision',
      icon: <EyeOutlined />,
      label: 'Computer Vision',
    },
  ];

  return (
    <Sider width={250} style={{ background: '#fff' }}>
      <div style={{ 
        padding: '20px', 
        textAlign: 'center', 
        borderBottom: '1px solid #f0f0f0',
        marginBottom: '20px'
      }}>
        <h2 style={{ margin: 0, color: '#1890ff' }}>🏨 Hotel AI Suite</h2>
        <p style={{ margin: '5px 0 0 0', color: '#666', fontSize: '12px' }}>
          Powered by Архитех ИИ
        </p>
      </div>
      <Menu
        mode="inline"
        selectedKeys={[location.pathname]}
        items={menuItems}
        onClick={({ key }) => navigate(key)}
        style={{ border: 'none' }}
      />
    </Sider>
  );
};

export default Sidebar;
