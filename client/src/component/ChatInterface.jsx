import { useState, useRef, useEffect } from 'react';
import { askQuestion } from '../utils/api';

const ChatInterface = ({ documentId, documentName }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const formatTime = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const handleSendMessage = async () => {
    if (!inputValue.trim() || !documentId) return;

    const userMessage = {
      text: inputValue,
      sender: 'user',
      time: formatTime()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await askQuestion(documentId, inputValue);
      const botMessage = {
        text: response.answer,
        sender: 'bot',
        time: formatTime()
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        text: error.message || 'Failed to get answer',
        sender: 'bot',
        time: formatTime(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b">
        <h2 className="text-lg font-semibold">Chat about: {documentName}</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`flex items-start max-w-xs md:max-w-md lg:max-w-lg ${msg.sender === 'user' ? 'flex-row-reverse' : ''}`}
            >
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${msg.sender === 'user' ? 'bg-blue-500 ml-3' : 'bg-gray-300 mr-3'}`}>
                {msg.sender === 'user' ? (
                  <span className="text-white text-sm">U</span>
                ) : (
                  <span className="text-gray-700 text-sm">B</span>
                )}
              </div>
              <div
                className={`p-3 rounded-lg ${msg.sender === 'user'
                  ? 'bg-blue-100 text-blue-900'
                  : msg.isError
                    ? 'bg-red-100 text-red-900 border border-red-600'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                <p>{msg.text}</p>
                <p className="text-xs mt-1 opacity-70">{msg.time}</p>
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex items-start">
              <div className="w-8 h-8 rounded-full bg-gray-300 mr-3 flex items-center justify-center">
                <span className="text-gray-700 text-sm">B</span>
              </div>
              <div className="p-3 rounded-lg bg-gray-100 text-gray-900">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"></div>
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t">
        <div className="flex">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask something about the document..."
            className="flex-1 p-2 border rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !inputValue.trim()}
            className="px-4 py-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 disabled:bg-blue-300 transition"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
