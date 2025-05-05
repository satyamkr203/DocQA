import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

// Function to upload the document
export const uploadDocument = async (file) => {
  if (!file) {
    throw new Error('No file selected');
  }

  if (!(file instanceof File) && !(file instanceof Blob)) {
    throw new Error('Invalid file object');
  }

  if (file.type !== 'application/pdf') {
    throw new Error('Only PDF files are allowed');
  }

  // File size validation (max 10MB)
  if (file.size > 10 * 1024 * 1024) {
    throw new Error('File size exceeds 10MB');
  }

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post(`${API_BASE}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 30000,
    });
    return response.data; // This includes the "id" field you need
  } catch (error) {
    const errorMessage =
      error.response?.data?.detail ||
      error.message ||
      'File upload failed';
    throw new Error(errorMessage);
  }
};

// Function to ask a question about the uploaded document
export const askQuestion = async (documentId, question) => {
  if (!documentId) throw new Error('Document ID is required');
  if (!question?.trim()) throw new Error('Question is required');

  try {
    const response = await axios.post(`${API_BASE}/question`, {
      document_id: documentId,
      question: question.trim(),
    });
    return response.data;
  } catch (error) {
    const errorMessage =
      error.response?.data?.detail ||
      error.message ||
      'Failed to get answer';
    throw new Error(errorMessage);
  }
};

// Combined function: Upload the file and ask a question
export const uploadAndAskQuestion = async (file, question) => {
  try {
    const uploadResponse = await uploadDocument(file);
    const documentId = uploadResponse.id;

    const questionResponse = await askQuestion(documentId, question);
    return questionResponse;
  } catch (err) {
    throw err;
  }
};
