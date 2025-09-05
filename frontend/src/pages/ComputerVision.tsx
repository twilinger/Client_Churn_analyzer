import React, { useState, useRef } from 'react';
import { 
  Card, 
  Button, 
  Upload, 
  Image, 
  Row, 
  Col, 
  Typography, 
  Space, 
  Tag,
  Alert,
  Progress,
  List
} from 'antd';
import { 
  UploadOutlined, 
  EyeOutlined, 
  CameraOutlined,
  ScanOutlined,
  UserOutlined,
  CarOutlined,
  HomeOutlined
} from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;

interface VisionResult {
  type: 'face' | 'object' | 'text' | 'scene';
  confidence: number;
  description: string;
  boundingBox?: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
}

interface AnalysisResult {
  imageUrl: string;
  results: VisionResult[];
  processingTime: number;
  timestamp: string;
}

const ComputerVision: React.FC = () => {
  const [uploading, setUploading] = useState(false);
  const [analysisResults, setAnalysisResults] = useState<AnalysisResult[]>([]);
  const [currentImage, setCurrentImage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageUpload = async (file: File) => {
    setUploading(true);
    
    try {
      const formData = new FormData();
      formData.append('image', file);
      
      // Simulate API call to computer vision service
      const response = await axios.post('/api/computer-vision/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      const result: AnalysisResult = {
        imageUrl: URL.createObjectURL(file),
        results: response.data.results,
        processingTime: response.data.processingTime,
        timestamp: new Date().toLocaleString()
      };
      
      setAnalysisResults(prev => [result, ...prev]);
      setCurrentImage(result.imageUrl);
      
    } catch (error) {
      console.error('Error analyzing image:', error);
      // Mock data for demonstration
      const mockResult: AnalysisResult = {
        imageUrl: URL.createObjectURL(file),
        results: [
          {
            type: 'face',
            confidence: 0.95,
            description: 'Human face detected',
            boundingBox: { x: 100, y: 50, width: 200, height: 250 }
          },
          {
            type: 'object',
            confidence: 0.87,
            description: 'Hotel lobby furniture',
            boundingBox: { x: 300, y: 200, width: 150, height: 100 }
          },
          {
            type: 'text',
            confidence: 0.92,
            description: 'Welcome to Hotel Plaza',
            boundingBox: { x: 50, y: 400, width: 300, height: 50 }
          }
        ],
        processingTime: 1.2,
        timestamp: new Date().toLocaleString()
      };
      
      setAnalysisResults(prev => [mockResult, ...prev]);
      setCurrentImage(mockResult.imageUrl);
    }
    
    setUploading(false);
  };

  const handleCameraCapture = () => {
    // Simulate camera capture
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 640;
    canvas.height = 480;
    
    // Draw a mock image
    if (ctx) {
      ctx.fillStyle = '#f0f0f0';
      ctx.fillRect(0, 0, 640, 480);
      ctx.fillStyle = '#1890ff';
      ctx.font = '24px Arial';
      ctx.fillText('Hotel Lobby View', 200, 240);
    }
    
    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
        handleImageUpload(file);
      }
    }, 'image/jpeg');
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'face': return <UserOutlined />;
      case 'object': return <HomeOutlined />;
      case 'text': return <ScanOutlined />;
      case 'scene': return <EyeOutlined />;
      default: return <ScanOutlined />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'face': return 'blue';
      case 'object': return 'green';
      case 'text': return 'orange';
      case 'scene': return 'purple';
      default: return 'default';
    }
  };

  return (
    <div>
      <Title level={2}>👁️ Computer Vision Analysis</Title>
      <Text type="secondary">
        AI-powered image analysis for hotel security and guest services
      </Text>

      {/* Upload Controls */}
      <Card title="Image Analysis" style={{ marginTop: '24px' }}>
        <Space direction="vertical" style={{ width: '100%' }}>
          <Row gutter={16}>
            <Col span={12}>
              <Upload
                beforeUpload={(file) => {
                  handleImageUpload(file);
                  return false; // Prevent default upload
                }}
                showUploadList={false}
                accept="image/*"
              >
                <Button 
                  icon={<UploadOutlined />} 
                  size="large" 
                  loading={uploading}
                  block
                >
                  Upload Image
                </Button>
              </Upload>
            </Col>
            <Col span={12}>
              <Button 
                icon={<CameraOutlined />} 
                size="large"
                onClick={handleCameraCapture}
                block
              >
                Capture from Camera
              </Button>
            </Col>
          </Row>
          
          {uploading && (
            <Alert
              message="Analyzing image..."
              description="AI is processing your image. This may take a few seconds."
              type="info"
              showIcon
            />
          )}
        </Space>
      </Card>

      {/* Current Analysis */}
      {currentImage && analysisResults.length > 0 && (
        <Row gutter={16} style={{ marginTop: '24px' }}>
          <Col span={12}>
            <Card title="Current Image">
              <Image
                src={currentImage}
                alt="Analysis target"
                style={{ width: '100%', maxHeight: '400px', objectFit: 'contain' }}
              />
            </Card>
          </Col>
          <Col span={12}>
            <Card title="Analysis Results">
              <List
                dataSource={analysisResults[0].results}
                renderItem={(result) => (
                  <List.Item>
                    <List.Item.Meta
                      avatar={
                        <Tag color={getTypeColor(result.type)} icon={getTypeIcon(result.type)}>
                          {result.type.toUpperCase()}
                        </Tag>
                      }
                      title={result.description}
                      description={
                        <div>
                          <Progress 
                            percent={Math.round(result.confidence * 100)} 
                            size="small" 
                            format={() => `${(result.confidence * 100).toFixed(1)}%`}
                          />
                          {result.boundingBox && (
                            <Text type="secondary" style={{ fontSize: '12px' }}>
                              Position: ({result.boundingBox.x}, {result.boundingBox.y}) 
                              Size: {result.boundingBox.width}×{result.boundingBox.height}
                            </Text>
                          )}
                        </div>
                      }
                    />
                  </List.Item>
                )}
              />
              <div style={{ marginTop: '16px', padding: '12px', background: '#f5f5f5', borderRadius: '6px' }}>
                <Text type="secondary">
                  Processing time: {analysisResults[0].processingTime}s
                </Text>
              </div>
            </Card>
          </Col>
        </Row>
      )}

      {/* Analysis History */}
      {analysisResults.length > 1 && (
        <Card title="Analysis History" style={{ marginTop: '24px' }}>
          <List
            dataSource={analysisResults.slice(1)}
            renderItem={(result, index) => (
              <List.Item
                actions={[
                  <Button 
                    type="link" 
                    onClick={() => setCurrentImage(result.imageUrl)}
                  >
                    View
                  </Button>
                ]}
              >
                <List.Item.Meta
                  avatar={
                    <Image
                      src={result.imageUrl}
                      alt={`Analysis ${index + 1}`}
                      style={{ width: '60px', height: '60px', objectFit: 'cover' }}
                    />
                  }
                  title={`Analysis ${index + 1}`}
                  description={
                    <div>
                      <div>{result.results.length} objects detected</div>
                      <Text type="secondary" style={{ fontSize: '12px' }}>
                        {result.timestamp}
                      </Text>
                    </div>
                  }
                />
              </List.Item>
            )}
          />
        </Card>
      )}
    </div>
  );
};

export default ComputerVision;
