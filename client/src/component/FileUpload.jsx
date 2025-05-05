import { useState } from 'react';
import { uploadDocument } from '../utils/api';

const FileUpload = ({ onFileUpload }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);

  const handleFileChange = async (e) => {
    // Safely get the file with optional chaining
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setUploadError(null);

    try {
      // First validate the file type client-side
      if (file.type !== 'application/pdf') {
        throw new Error('Only PDF files are allowed');
      }

      const response = await uploadDocument(file);
      onFileUpload(response.id, file.name); // Changed from response.documentId to response.id
    } catch (error) {
      setUploadError(error.message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="flex items-center gap-2">
      <label className={`px-4 py-2 rounded-lg cursor-pointer transition
        ${isUploading 
          ? 'bg-blue-300 cursor-not-allowed' 
          : 'bg-blue-500 hover:bg-blue-600 text-white'}`}>
        {isUploading ? 'Uploading...' : 'Upload PDF'}
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="hidden"
          disabled={isUploading}
        />
      </label>
      {uploadError && (
        <span className="text-red-500 text-sm max-w-xs">{uploadError}</span>
      )}
    </div>
  );
};

export default FileUpload;