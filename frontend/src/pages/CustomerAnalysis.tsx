import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Table, 
  Tag, 
  Progress, 
  Row, 
  Col, 
  Statistic, 
  Typography,
  Button,
  Space,
  Select,
  DatePicker,
  Input
} from 'antd';
import { 
  UserOutlined, 
  PhoneOutlined, 
  MailOutlined,
  WarningOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import axios from 'axios';

const { Title, Text } = Typography;
const { Search } = Input;
const { RangePicker } = DatePicker;

interface Customer {
  id: string;
  name: string;
  email: string;
  phone: string;
  churnProbability: number;
  lastInteraction: string;
  totalSpent: number;
  satisfactionScore: number;
  riskLevel: 'low' | 'medium' | 'high';
  segment: string;
}

const CustomerAnalysis: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedSegment, setSelectedSegment] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Mock data for demonstration
    setCustomers([
      {
        id: '1',
        name: 'John Smith',
        email: 'john.smith@email.com',
        phone: '+1-555-0123',
        churnProbability: 0.85,
        lastInteraction: '2024-01-10',
        totalSpent: 2450,
        satisfactionScore: 2.1,
        riskLevel: 'high',
        segment: 'Business'
      },
      {
        id: '2',
        name: 'Maria Garcia',
        email: 'maria.garcia@email.com',
        phone: '+1-555-0124',
        churnProbability: 0.25,
        lastInteraction: '2024-01-14',
        totalSpent: 1200,
        satisfactionScore: 4.5,
        riskLevel: 'low',
        segment: 'Leisure'
      },
      {
        id: '3',
        name: 'David Chen',
        email: 'david.chen@email.com',
        phone: '+1-555-0125',
        churnProbability: 0.65,
        lastInteraction: '2024-01-08',
        totalSpent: 3200,
        satisfactionScore: 3.2,
        riskLevel: 'medium',
        segment: 'VIP'
      },
      {
        id: '4',
        name: 'Sarah Johnson',
        email: 'sarah.johnson@email.com',
        phone: '+1-555-0126',
        churnProbability: 0.15,
        lastInteraction: '2024-01-15',
        totalSpent: 1800,
        satisfactionScore: 4.8,
        riskLevel: 'low',
        segment: 'Leisure'
      },
      {
        id: '5',
        name: 'Michael Brown',
        email: 'michael.brown@email.com',
        phone: '+1-555-0127',
        churnProbability: 0.92,
        lastInteraction: '2024-01-05',
        totalSpent: 1500,
        satisfactionScore: 1.8,
        riskLevel: 'high',
        segment: 'Business'
      }
    ]);
  }, []);

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'high': return 'red';
      case 'medium': return 'orange';
      case 'low': return 'green';
      default: return 'default';
    }
  };

  const getRiskIcon = (risk: string) => {
    switch (risk) {
      case 'high': return <WarningOutlined />;
      case 'medium': return <ExclamationCircleOutlined />;
      case 'low': return <CheckCircleOutlined />;
      default: return null;
    }
  };

  const columns = [
    {
      title: 'Customer',
      dataIndex: 'name',
      key: 'name',
      render: (text: string, record: Customer) => (
        <div>
          <div style={{ fontWeight: 'bold' }}>{text}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>
            {record.email}
          </div>
        </div>
      ),
    },
    {
      title: 'Phone',
      dataIndex: 'phone',
      key: 'phone',
    },
    {
      title: 'Churn Risk',
      dataIndex: 'churnProbability',
      key: 'churnProbability',
      render: (probability: number, record: Customer) => (
        <div>
          <Progress 
            percent={Math.round(probability * 100)} 
            size="small"
            strokeColor={probability > 0.7 ? '#ff4d4f' : probability > 0.4 ? '#faad14' : '#52c41a'}
          />
          <Tag 
            color={getRiskColor(record.riskLevel)} 
            icon={getRiskIcon(record.riskLevel)}
            style={{ marginTop: '4px' }}
          >
            {record.riskLevel.toUpperCase()}
          </Tag>
        </div>
      ),
    },
    {
      title: 'Satisfaction',
      dataIndex: 'satisfactionScore',
      key: 'satisfactionScore',
      render: (score: number) => (
        <Progress 
          percent={score * 20} 
          size="small"
          format={() => `${score}/5`}
          strokeColor={score >= 4 ? '#52c41a' : score >= 3 ? '#faad14' : '#ff4d4f'}
        />
      ),
    },
    {
      title: 'Total Spent',
      dataIndex: 'totalSpent',
      key: 'totalSpent',
      render: (amount: number) => `$${amount.toLocaleString()}`,
    },
    {
      title: 'Segment',
      dataIndex: 'segment',
      key: 'segment',
      render: (segment: string) => (
        <Tag color="blue">{segment}</Tag>
      ),
    },
    {
      title: 'Last Interaction',
      dataIndex: 'lastInteraction',
      key: 'lastInteraction',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (record: Customer) => (
        <Space>
          <Button size="small" type="primary">
            Contact
          </Button>
          <Button size="small">
            Analyze
          </Button>
        </Space>
      ),
    },
  ];

  const filteredCustomers = customers.filter(customer => {
    const matchesSearch = customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         customer.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSegment = selectedSegment === 'all' || customer.segment === selectedSegment;
    return matchesSearch && matchesSegment;
  });

  const churnTrendData = [
    { month: 'Jan', rate: 25.2 },
    { month: 'Feb', rate: 23.8 },
    { month: 'Mar', rate: 22.1 },
    { month: 'Apr', rate: 24.5 },
    { month: 'May', rate: 23.4 },
    { month: 'Jun', rate: 21.9 }
  ];

  const segmentDistribution = [
    { name: 'Business', value: 35, color: '#8884d8' },
    { name: 'Leisure', value: 45, color: '#82ca9d' },
    { name: 'VIP', value: 20, color: '#ffc658' }
  ];

  const riskDistribution = [
    { name: 'High Risk', value: customers.filter(c => c.riskLevel === 'high').length, color: '#ff4d4f' },
    { name: 'Medium Risk', value: customers.filter(c => c.riskLevel === 'medium').length, color: '#faad14' },
    { name: 'Low Risk', value: customers.filter(c => c.riskLevel === 'low').length, color: '#52c41a' }
  ];

  const stats = {
    totalCustomers: customers.length,
    highRiskCustomers: customers.filter(c => c.riskLevel === 'high').length,
    avgChurnProbability: customers.length > 0 ? 
      (customers.reduce((sum, c) => sum + c.churnProbability, 0) / customers.length * 100).toFixed(1) : 0,
    avgSatisfaction: customers.length > 0 ? 
      (customers.reduce((sum, c) => sum + c.satisfactionScore, 0) / customers.length).toFixed(1) : 0
  };

  return (
    <div>
      <Title level={2}>👥 Customer Analysis</Title>
      <Text type="secondary">
        AI-powered customer churn prediction and satisfaction analysis
      </Text>

      {/* Statistics */}
      <Row gutter={16} style={{ marginBottom: '24px', marginTop: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Customers"
              value={stats.totalCustomers}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="High Risk Customers"
              value={stats.highRiskCustomers}
              prefix={<WarningOutlined />}
              valueStyle={{ color: '#cf1322' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Avg Churn Probability"
              value={stats.avgChurnProbability}
              suffix="%"
              prefix={<ExclamationCircleOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Avg Satisfaction"
              value={stats.avgSatisfaction}
              suffix="/5"
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Charts */}
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={8}>
          <Card title="Churn Rate Trend" style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={churnTrendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="rate" stroke="#ff4d4f" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        <Col span={8}>
          <Card title="Customer Segments" style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={segmentDistribution}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {segmentDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        <Col span={8}>
          <Card title="Risk Distribution" style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={riskDistribution}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#1890ff" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Col>
      </Row>

      {/* Filters */}
      <Card style={{ marginBottom: '16px' }}>
        <Row gutter={16} align="middle">
          <Col span={8}>
            <Search
              placeholder="Search customers..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ width: '100%' }}
            />
          </Col>
          <Col span={8}>
            <Select
              placeholder="Filter by segment"
              value={selectedSegment}
              onChange={setSelectedSegment}
              style={{ width: '100%' }}
            >
              <Select.Option value="all">All Segments</Select.Option>
              <Select.Option value="Business">Business</Select.Option>
              <Select.Option value="Leisure">Leisure</Select.Option>
              <Select.Option value="VIP">VIP</Select.Option>
            </Select>
          </Col>
          <Col span={8}>
            <Space>
              <Button type="primary">Export Data</Button>
              <Button>Refresh Analysis</Button>
            </Space>
          </Col>
        </Row>
      </Card>

      {/* Customer Table */}
      <Card title="Customer Details">
        <Table
          columns={columns}
          dataSource={filteredCustomers}
          loading={loading}
          pagination={{ pageSize: 10 }}
          scroll={{ x: 1200 }}
        />
      </Card>
    </div>
  );
};

export default CustomerAnalysis;
