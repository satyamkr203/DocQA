import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

// Configure axios instance with default settings
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Accept': 'application/json',
  }
});

// Add response interceptor to handle errors consistently
apiClient.interceptors.response.use(
  response => response,
  error => {
    const errorMessage = error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'Request failed';
    return Promise.reject(new Error(errorMessage));
  }
);

export const uploadDocument = async (file) => {
  // Validation
  if (!file) {
    throw new Error('No file selected');
  }
  if (!(file instanceof File) && !(file instanceof Blob)) {
    throw new Error('Invalid file object');
  }
  if (file.type !== 'application/pdf') {
    throw new Error('Only PDF files are allowed');
  }
  if (file.size > 10 * 1024 * 1024) { // 10MB limit
    throw new Error('File size exceeds 10MB');
  }

  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await apiClient.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw error; // Error already processed by interceptor
  }
};

export const askQuestion = async (documentId, question) => {
  // Validation
  if (!documentId || typeof documentId !== 'number') {
    throw new Error('Valid document ID is required');
  }
  if (!question?.trim()) {
    throw new Error('Question is required');
  }

  try {
    const response = await apiClient.post('/question', {
      document_id: documentId,
      question: question.trim(),
    }, {
      headers: {
        'Content-Type': 'application/json',
      }
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const uploadAndAskQuestion = async (file, question) => {
  try {
    const { id: documentId } = await uploadDocument(file);
    return await askQuestion(documentId, question);
  } catch (error) {
    throw error;
  }
};