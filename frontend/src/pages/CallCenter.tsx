import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Button, 
  Input, 
  List, 
  Avatar, 
  Typography, 
  Space, 
  Tag, 
  Row, 
  Col,
  Statistic,
  Progress,
  Alert
} from 'antd';
import { 
  PhoneOutlined, 
  MessageOutlined, 
  RobotOutlined, 
  UserOutlined,
  SoundOutlined,
  StopOutlined,
  PlayCircleOutlined
} from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;
const { TextArea } = Input;

interface CallRecord {
  id: string;
  customerName: string;
  phoneNumber: string;
  duration: string;
  status: 'completed' | 'in-progress' | 'queued';
  aiHandled: boolean;
  satisfaction: number;
  transcript: string;
  timestamp: string;
}

const CallCenter: React.FC = () => {
  const [calls, setCalls] = useState<CallRecord[]>([]);
  const [currentCall, setCurrentCall] = useState<CallRecord | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [aiResponse, setAiResponse] = useState('');
  const [customerInput, setCustomerInput] = useState('');

  useEffect(() => {
    // Mock data for demonstration
    setCalls([
      {
        id: '1',
        customerName: 'John Smith',
        phoneNumber: '+1-555-0123',
        duration: '3:45',
        status: 'completed',
        aiHandled: true,
        satisfaction: 5,
        transcript: 'Customer called about room service. AI provided automated response with menu options.',
        timestamp: '2024-01-15 14:30'
      },
      {
        id: '2',
        customerName: 'Maria Garcia',
        phoneNumber: '+1-555-0124',
        duration: '2:15',
        status: 'completed',
        aiHandled: false,
        satisfaction: 4,
        transcript: 'Customer needed help with check-in. Escalated to human agent.',
        timestamp: '2024-01-15 13:45'
      },
      {
        id: '3',
        customerName: 'David Chen',
        phoneNumber: '+1-555-0125',
        duration: '0:00',
        status: 'in-progress',
        aiHandled: true,
        satisfaction: 0,
        transcript: 'Customer calling about billing inquiry...',
        timestamp: '2024-01-15 15:20'
      }
    ]);
  }, []);

  const handleStartCall = () => {
    const newCall: CallRecord = {
      id: Date.now().toString(),
      customerName: 'New Customer',
      phoneNumber: '+1-555-XXXX',
      duration: '0:00',
      status: 'in-progress',
      aiHandled: true,
      satisfaction: 0,
      transcript: '',
      timestamp: new Date().toLocaleString()
    };
    setCurrentCall(newCall);
    setIsRecording(true);
  };

  const handleEndCall = () => {
    if (currentCall) {
      setCalls(prev => [currentCall, ...prev]);
      setCurrentCall(null);
      setIsRecording(false);
    }
  };

  const handleCustomerMessage = async () => {
    if (!customerInput.trim()) return;

    try {
      // Simulate AI response
      const response = await axios.post('/api/call-center/process', {
        message: customerInput,
        context: 'hotel_customer_service'
      });
      
      setAiResponse(response.data.response);
      
      if (currentCall) {
        setCurrentCall({
          ...currentCall,
          transcript: currentCall.transcript + `\nCustomer: ${customerInput}\nAI: ${response.data.response}`
        });
      }
      
      setCustomerInput('');
    } catch (error) {
      console.error('Error processing message:', error);
      setAiResponse('Sorry, I encountered an error. Let me connect you to a human agent.');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'green';
      case 'in-progress': return 'blue';
      case 'queued': return 'orange';
      default: return 'default';
    }
  };

  const stats = {
    totalCalls: calls.length,
    aiHandled: calls.filter(c => c.aiHandled).length,
    avgSatisfaction: calls.length > 0 ? 
      (calls.reduce((sum, c) => sum + c.satisfaction, 0) / calls.length).toFixed(1) : 0,
    avgDuration: '2:30'
  };

  return (
    <div>
      <Title level={2}>🤖 AI-Powered Call Center</Title>
      <Text type="secondary">
        Automated customer service for hotel operations
      </Text>

      {/* Statistics */}
      <Row gutter={16} style={{ marginBottom: '24px', marginTop: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Calls Today"
              value={stats.totalCalls}
              prefix={<PhoneOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="AI Handled"
              value={stats.aiHandled}
              suffix={`/ ${stats.totalCalls}`}
              prefix={<RobotOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Avg Satisfaction"
              value={stats.avgSatisfaction}
              suffix="/5"
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Avg Duration"
              value={stats.avgDuration}
              prefix={<SoundOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {/* Current Call Interface */}
      <Row gutter={16}>
        <Col span={12}>
          <Card title="Active Call Control" style={{ height: '500px' }}>
            {currentCall ? (
              <div>
                <Space direction="vertical" style={{ width: '100%' }}>
                  <Alert
                    message={`Call with ${currentCall.customerName}`}
                    description={`Phone: ${currentCall.phoneNumber}`}
                    type="info"
                    showIcon
                  />
                  
                  <div style={{ textAlign: 'center' }}>
                    <Progress 
                      type="circle" 
                      percent={isRecording ? 100 : 0} 
                      format={() => isRecording ? '🔴' : '⏸️'}
                      size={80}
                    />
                    <div style={{ marginTop: '16px' }}>
                      <Text strong>Duration: {currentCall.duration}</Text>
                    </div>
                  </div>

                  <TextArea
                    placeholder="Customer message..."
                    value={customerInput}
                    onChange={(e) => setCustomerInput(e.target.value)}
                    rows={3}
                  />
                  
                  <Button 
                    type="primary" 
                    onClick={handleCustomerMessage}
                    icon={<MessageOutlined />}
                    block
                  >
                    Process with AI
                  </Button>

                  {aiResponse && (
                    <Alert
                      message="AI Response"
                      description={aiResponse}
                      type="success"
                      showIcon
                    />
                  )}

                  <Button 
                    danger 
                    onClick={handleEndCall}
                    icon={<StopOutlined />}
                    block
                  >
                    End Call
                  </Button>
                </Space>
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: '40px' }}>
                <PlayCircleOutlined style={{ fontSize: '48px', color: '#1890ff' }} />
                <Title level={4}>No Active Call</Title>
                <Button 
                  type="primary" 
                  size="large"
                  onClick={handleStartCall}
                  icon={<PhoneOutlined />}
                >
                  Start New Call
                </Button>
              </div>
            )}
          </Card>
        </Col>

        <Col span={12}>
          <Card title="Call History" style={{ height: '500px' }}>
            <List
              dataSource={calls}
              renderItem={(call) => (
                <List.Item
                  actions={[
                    <Tag color={getStatusColor(call.status)} key="status">
                      {call.status}
                    </Tag>,
                    <Tag color={call.aiHandled ? 'green' : 'orange'} key="ai">
                      {call.aiHandled ? 'AI' : 'Human'}
                    </Tag>
                  ]}
                >
                  <List.Item.Meta
                    avatar={<Avatar icon={<PhoneOutlined />} />}
                    title={`${call.customerName} (${call.phoneNumber})`}
                    description={
                      <div>
                        <div>{call.transcript}</div>
                        <Text type="secondary" style={{ fontSize: '12px' }}>
                          {call.timestamp} • Duration: {call.duration}
                        </Text>
                      </div>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default CallCenter;
