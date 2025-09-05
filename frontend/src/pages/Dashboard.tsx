import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic, Table, Tag, Progress } from 'antd';
import { 
  UserOutlined, 
  PhoneOutlined, 
  MessageOutlined, 
  EyeOutlined,
  TrendingUpOutlined,
  TrendingDownOutlined
} from '@ant-design/icons';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState({
    totalCustomers: 0,
    churnRate: 0,
    aiInteractions: 0,
    satisfactionScore: 0
  });

  const [recentInteractions, setRecentInteractions] = useState([]);

  // Mock data for demonstration
  useEffect(() => {
    setStats({
      totalCustomers: 1247,
      churnRate: 23.4,
      aiInteractions: 3421,
      satisfactionScore: 4.2
    });

    setRecentInteractions([
      {
        key: '1',
        customer: 'John Smith',
        interaction: 'Room service inquiry',
        aiResponse: 'Automated response provided',
        satisfaction: 5,
        timestamp: '2024-01-15 14:30'
      },
      {
        key: '2',
        customer: 'Maria Garcia',
        interaction: 'Check-in assistance',
        aiResponse: 'Escalated to human agent',
        satisfaction: 4,
        timestamp: '2024-01-15 13:45'
      },
      {
        key: '3',
        customer: 'David Chen',
        interaction: 'Complaint resolution',
        aiResponse: 'AI suggested solution',
        satisfaction: 5,
        timestamp: '2024-01-15 12:20'
      }
    ]);
  }, []);

  const churnData = [
    { month: 'Jan', rate: 25.2 },
    { month: 'Feb', rate: 23.8 },
    { month: 'Mar', rate: 22.1 },
    { month: 'Apr', rate: 24.5 },
    { month: 'May', rate: 23.4 },
    { month: 'Jun', rate: 21.9 }
  ];

  const interactionTypes = [
    { name: 'Room Service', value: 35, color: '#8884d8' },
    { name: 'Check-in/out', value: 28, color: '#82ca9d' },
    { name: 'Complaints', value: 20, color: '#ffc658' },
    { name: 'General Info', value: 17, color: '#ff7300' }
  ];

  const columns = [
    {
      title: 'Customer',
      dataIndex: 'customer',
      key: 'customer',
    },
    {
      title: 'Interaction Type',
      dataIndex: 'interaction',
      key: 'interaction',
    },
    {
      title: 'AI Response',
      dataIndex: 'aiResponse',
      key: 'aiResponse',
      render: (text: string) => (
        <Tag color={text.includes('Automated') ? 'green' : 'orange'}>
          {text}
        </Tag>
      ),
    },
    {
      title: 'Satisfaction',
      dataIndex: 'satisfaction',
      key: 'satisfaction',
      render: (rating: number) => (
        <Progress 
          percent={rating * 20} 
          size="small" 
          format={() => `${rating}/5`}
          strokeColor={rating >= 4 ? '#52c41a' : rating >= 3 ? '#faad14' : '#ff4d4f'}
        />
      ),
    },
    {
      title: 'Time',
      dataIndex: 'timestamp',
      key: 'timestamp',
    },
  ];

  return (
    <div>
      <h1>Hotel AI Dashboard</h1>
      <p style={{ color: '#666', marginBottom: '24px' }}>
        Real-time insights into AI-powered customer service operations
      </p>

      {/* Key Metrics */}
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Customers"
              value={stats.totalCustomers}
              prefix={<UserOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Churn Rate"
              value={stats.churnRate}
              suffix="%"
              prefix={<TrendingDownOutlined />}
              valueStyle={{ color: '#cf1322' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="AI Interactions"
              value={stats.aiInteractions}
              prefix={<MessageOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Satisfaction Score"
              value={stats.satisfactionScore}
              suffix="/5"
              prefix={<TrendingUpOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Charts */}
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={12}>
          <Card title="Churn Rate Trend" style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={churnData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="rate" stroke="#1890ff" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Interaction Types Distribution" style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={interactionTypes}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {interactionTypes.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </Col>
      </Row>

      {/* Recent Interactions */}
      <Card title="Recent AI Interactions">
        <Table 
          columns={columns} 
          dataSource={recentInteractions} 
          pagination={{ pageSize: 5 }}
          size="small"
        />
      </Card>
    </div>
  );
};

export default Dashboard;
