import React, { useState, useRef, useEffect } from 'react';
import { 
  Card, 
  Input, 
  Button, 
  List, 
  Avatar, 
  Typography, 
  Space,
  Tag,
  Row,
  Col,
  Statistic
} from 'antd';
import { 
  SendOutlined, 
  RobotOutlined, 
  UserOutlined,
  MessageOutlined,
  ThunderboltOutlined
} from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;
const { TextArea } = Input;

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  context?: string;
}

const AIChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI assistant for hotel operations. I can help you with customer analysis, churn prediction, and operational insights. What would you like to know?',
      timestamp: new Date().toLocaleString()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toLocaleString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/chat/message', {
        message: inputMessage,
        context: 'hotel_operations'
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date().toLocaleString(),
        context: response.data.context
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again or contact support.',
        timestamp: new Date().toLocaleString()
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    setIsLoading(false);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const quickActions = [
    'Show customer churn analysis',
    'What are the top complaints today?',
    'Analyze room occupancy trends',
    'Generate customer satisfaction report',
    'Predict next month\'s churn rate'
  ];

  const handleQuickAction = (action: string) => {
    setInputMessage(action);
  };

  const stats = {
    totalMessages: messages.length,
    aiResponses: messages.filter(m => m.role === 'assistant').length,
    avgResponseTime: '1.2s',
    satisfactionScore: '4.8/5'
  };

  return (
    <div>
      <Title level={2}>🤖 AI Assistant</Title>
      <Text type="secondary">
        Intelligent chatbot for hotel operations and customer insights
      </Text>

      {/* Statistics */}
      <Row gutter={16} style={{ marginBottom: '24px', marginTop: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Messages"
              value={stats.totalMessages}
              prefix={<MessageOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="AI Responses"
              value={stats.aiResponses}
              prefix={<RobotOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Avg Response Time"
              value={stats.avgResponseTime}
              prefix={<ThunderboltOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Satisfaction Score"
              value={stats.satisfactionScore}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={16}>
          <Card title="Chat Interface" style={{ height: '600px' }}>
            <div style={{ 
              height: '450px', 
              overflowY: 'auto', 
              border: '1px solid #f0f0f0', 
              borderRadius: '6px',
              padding: '16px',
              marginBottom: '16px'
            }}>
              <List
                dataSource={messages}
                renderItem={(message) => (
                  <List.Item style={{ border: 'none', padding: '8px 0' }}>
                    <List.Item.Meta
                      avatar={
                        <Avatar 
                          icon={message.role === 'user' ? <UserOutlined /> : <RobotOutlined />}
                          style={{ 
                            backgroundColor: message.role === 'user' ? '#1890ff' : '#52c41a' 
                          }}
                        />
                      }
                      title={
                        <Space>
                          <Text strong>
                            {message.role === 'user' ? 'You' : 'AI Assistant'}
                          </Text>
                          <Text type="secondary" style={{ fontSize: '12px' }}>
                            {message.timestamp}
                          </Text>
                        </Space>
                      }
                      description={
                        <div>
                          <div style={{ marginBottom: '8px' }}>
                            {message.content}
                          </div>
                          {message.context && (
                            <Tag color="blue" style={{ fontSize: '11px' }}>
                              Context: {message.context}
                            </Tag>
                          )}
                        </div>
                      }
                    />
                  </List.Item>
                )}
              />
              {isLoading && (
                <div style={{ textAlign: 'center', padding: '20px' }}>
                  <Text type="secondary">AI is thinking...</Text>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
            
            <Space.Compact style={{ width: '100%' }}>
              <TextArea
                placeholder="Ask me anything about hotel operations, customer analysis, or churn prediction..."
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                rows={2}
                style={{ resize: 'none' }}
              />
              <Button 
                type="primary" 
                icon={<SendOutlined />}
                onClick={handleSendMessage}
                loading={isLoading}
                style={{ height: 'auto' }}
              >
                Send
              </Button>
            </Space.Compact>
          </Card>
        </Col>

        <Col span={8}>
          <Card title="Quick Actions">
            <Space direction="vertical" style={{ width: '100%' }}>
              {quickActions.map((action, index) => (
                <Button 
                  key={index}
                  onClick={() => handleQuickAction(action)}
                  style={{ textAlign: 'left', height: 'auto', padding: '8px 12px' }}
                  block
                >
                  {action}
                </Button>
              ))}
            </Space>
          </Card>

          <Card title="AI Capabilities" style={{ marginTop: '16px' }}>
            <Space direction="vertical" style={{ width: '100%' }}>
              <Tag color="green">Customer Churn Analysis</Tag>
              <Tag color="blue">Revenue Forecasting</Tag>
              <Tag color="orange">Complaint Analysis</Tag>
              <Tag color="purple">Occupancy Predictions</Tag>
              <Tag color="cyan">Satisfaction Insights</Tag>
              <Tag color="magenta">Operational Recommendations</Tag>
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default AIChat;
