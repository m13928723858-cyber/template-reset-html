import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes for long processing
});

export interface TaskStatus {
  task_id: string;
  status: string;
  progress: {
    stage: string;
    percentage: number;
    message?: string;
    brands?: string[];
    images_count?: number;
  };
  error?: string;
  output_file?: string;
  report?: {
    images_replaced: number;
    texts_replaced: number;
    brands_used: Record<string, number>;
    errors: string[];
  };
}

export interface ProcessRequest {
  task_id: string;
  product_type: string;
  winner_name: string;
  winner_image?: string;
  image_distribution?: 'balanced' | 'primary' | 'random';
}

export interface GenerateRequest {
  winner_name: string;
  product_type: string;
  user_image_url?: string;
}

export const uploadFile = async (file: File): Promise<{ task_id: string; filename: string }> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const uploadWinnerImage = async (file: File, taskId: string): Promise<{ task_id: string; winner_image_path: string }> => {
  const formData = new FormData();
  formData.append('file', file);
  
  // 将 task_id 作为 URL 参数传递
  const response = await api.post(`/api/upload?task_id=${taskId}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const processTask = async (request: ProcessRequest): Promise<{ task_id: string; status: string }> => {
  const response = await api.post('/api/process', request);
  return response.data;
};

export const getTaskStatus = async (taskId: string): Promise<TaskStatus> => {
  const response = await api.get(`/api/status/${taskId}`);
  return response.data;
};

export const downloadResult = (taskId: string): string => {
  return `${API_BASE_URL}/api/download/${taskId}`;
};

export const deleteTask = async (taskId: string): Promise<void> => {
  await api.delete(`/api/task/${taskId}`);
};

export const uploadImageOnly = async (file: File): Promise<{ image_id: string; image_url: string }> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/api/upload-image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const generatePage = async (request: GenerateRequest): Promise<{ task_id: string; status: string }> => {
  const response = await api.post('/api/generate', request);
  return response.data;
};

export default api;
