import { useState } from 'react';
import Navbar from './component/Navbar';
import ChatInterface from './component/ChatInterface';

function App() {
  const [documentInfo, setDocumentInfo] = useState({
    id: null,
    name: '',
    isLoading: false,
    error: null
  });

  const handleFileUpload = async (file) => {
    setDocumentInfo(prev => ({
      ...prev,
      isLoading: true,
      error: null
    }));

    try {
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setDocumentInfo({
        id: 'simulated-doc-id', // response.documentId in real app
        name: file.name,
        isLoading: false,
        error: null
      });
    } catch (error) {
      setDocumentInfo(prev => ({
        ...prev,
        isLoading: false,
        error: error.message || 'Failed to upload document'
      }));
    }
  };

  const resetDocument = () => {
    setDocumentInfo({
      id: null,
      name: '',
      isLoading: false,
      error: null
    });
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <Navbar 
        onFileUpload={handleFileUpload} 
        documentName={documentInfo.name}
        isLoading={documentInfo.isLoading}
      />
      
      <main className="flex-1 overflow-hidden">
        {documentInfo.error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4">
            <p>{documentInfo.error}</p>
          </div>
        )}

        {documentInfo.id ? (
          <ChatInterface 
            documentId={documentInfo.id} 
            documentName={documentInfo.name}
            onReset={resetDocument}
          />
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center p-6 max-w-md">
              <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-blue-100 flex items-center justify-center">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  className="h-10 w-10 text-blue-500" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
                  />
                </svg>
              </div>
              <h2 className="text-2xl font-bold mb-4 text-gray-800">Document QA Assistant</h2>
              <p className="mb-6 text-gray-600">
                Upload a PDF document to start asking questions about its content.
                Get instant answers powered by AI.
              </p>
              
              {documentInfo.isLoading ? (
                <div className="flex justify-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                </div>
              ) : (
                <div className="mt-4">
                  <p className="text-sm text-gray-500 mb-2">
                    Supported formats: PDF
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;