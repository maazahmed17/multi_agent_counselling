import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FiHome, FiBookOpen, FiSettings, FiUser, FiSend, FiMic } from "react-icons/fi";

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || '/api';

export default function SerenityDashboard() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (messageText) => {
    if (!messageText.trim() || isLoading) return;
    
    const userMessage = messageText.trim();
    setMessage("");
    
    setChatHistory(prev => [...prev, { type: 'user', text: userMessage }]);
    setIsLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.success) {
        setChatHistory(prev => [...prev, { 
          type: 'assistant', 
          text: data.response,
          specialist: data.specialist,
          evaluation: data.evaluation
        }]);
      } else {
        setChatHistory(prev => [...prev, { 
          type: 'error', 
          text: 'Sorry, something went wrong. Please try again.' 
        }]);
      }
    } catch (error) {
      console.error('Error:', error);
      setChatHistory(prev => [...prev, { 
        type: 'error', 
        text: `Unable to connect to the server. Please try again. (${error.message})` 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSend = () => {
    sendMessage(message);
  };

  const handleCardClick = (cardMessage) => {
    sendMessage(cardMessage);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-[#E8E9FF] via-[#F5F3FF] to-[#FCF5FF] text-gray-900 relative overflow-hidden">
      {/* Decorative gradient orbs */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-purple-300/20 rounded-full blur-3xl"></div>
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-indigo-300/20 rounded-full blur-3xl"></div>
      
      {/* Sidebar */}
      <aside className="w-20 flex flex-col items-center py-8 space-y-8 bg-white/40 backdrop-blur-md shadow-sm z-10">
        <div className="w-12 h-12 flex items-center justify-center rounded-full bg-gradient-to-br from-indigo-600 to-purple-600 text-white text-xl font-bold shadow-lg">
          M
        </div>
        <nav className="flex flex-col gap-8 text-gray-500 text-2xl">
          <FiHome className="hover:text-indigo-600 cursor-pointer transition-colors" />
          <FiBookOpen className="hover:text-indigo-600 cursor-pointer transition-colors" />
          <FiUser className="hover:text-indigo-600 cursor-pointer transition-colors" />
          <FiSettings className="hover:text-indigo-600 cursor-pointer transition-colors" />
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center justify-center px-8 py-12 relative z-10">
        <div className="w-full max-w-5xl">
          {/* Header */}
          <motion.h1 
            className="text-5xl font-bold text-center mb-16"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            Hi, Ready to Start Your{" "}
            <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              Healing Journey?
            </span>
          </motion.h1>

          {/* Cards - Only show when no chat history */}
          {chatHistory.length === 0 && (
            <motion.div 
              className="grid md:grid-cols-3 gap-8 mb-20"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <motion.div 
                whileHover={{ scale: 1.05, y: -5 }} 
                whileTap={{ scale: 0.98 }}
                onClick={() => handleCardClick("I'm feeling anxious and could use some support")}
                className="bg-white/70 backdrop-blur-md rounded-3xl shadow-xl p-8 cursor-pointer border border-white/50 transition-all hover:shadow-2xl"
              >
                <div className="text-5xl mb-4">😊</div>
                <h3 className="text-2xl font-semibold mb-2 text-gray-800">I feel anxious</h3>
                <p className="text-gray-600 text-sm">Get support</p>
              </motion.div>

              <motion.div 
                whileHover={{ scale: 1.05, y: -5 }} 
                whileTap={{ scale: 0.98 }}
                onClick={() => handleCardClick("I'm doing okay, just wanted to check in and have a chat")}
                className="bg-white/70 backdrop-blur-md rounded-3xl shadow-xl p-8 cursor-pointer border border-white/50 transition-all hover:shadow-2xl"
              >
                <div className="text-5xl mb-4">🔒</div>
                <h3 className="text-2xl font-semibold mb-2 text-gray-800">I'm doing okay</h3>
                <p className="text-gray-600 text-sm">Let's have a chat</p>
              </motion.div>

              <motion.div 
                whileHover={{ scale: 1.05, y: -5 }} 
                whileTap={{ scale: 0.98 }}
                onClick={() => handleCardClick("I need help now and need to talk to someone urgently")}
                className="bg-white/70 backdrop-blur-md rounded-3xl shadow-xl p-8 cursor-pointer border border-white/50 transition-all hover:shadow-2xl"
              >
                <div className="text-5xl mb-4">⚠️</div>
                <h3 className="text-2xl font-semibold mb-2 text-gray-800">I need help now</h3>
                <p className="text-gray-600 text-sm">Access resources</p>
              </motion.div>
            </motion.div>
          )}

          {/* Chat History */}
          {chatHistory.length > 0 && (
            <div className="bg-white/70 backdrop-blur-md rounded-3xl shadow-xl p-8 mb-8 max-h-96 overflow-y-auto border border-white/50">
              {chatHistory.map((msg, index) => (
                <div key={index} className={`mb-4 ${msg.type === 'user' ? 'text-right' : 'text-left'}`}>
                  <div className={`inline-block max-w-[80%] p-4 rounded-2xl ${
                    msg.type === 'user' 
                      ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white' 
                      : msg.type === 'error'
                      ? 'bg-red-100 text-red-800'
                      : 'bg-gray-100 text-gray-900'
                  }`}>
                    <p className="whitespace-pre-wrap">{msg.text}</p>
                    {msg.specialist && (
                      <p className="text-xs mt-2 opacity-70">Specialist: {msg.specialist}</p>
                    )}
                    {msg.evaluation && msg.evaluation.approved && (
                      <p className="text-xs mt-1 opacity-70">✓ Approved (Score: {msg.evaluation.overall_score}/10)</p>
                    )}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="text-left mb-4">
                  <div className="inline-block bg-gray-100 text-gray-900 p-4 rounded-2xl">
                    <p className="animate-pulse">Thinking...</p>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Chat Input - Fixed at bottom center */}
          <motion.div 
            className="fixed bottom-8 left-1/2 transform -translate-x-1/2 w-full max-w-3xl px-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <div className="flex items-center bg-white/80 backdrop-blur-md rounded-full shadow-2xl px-6 py-4 border border-white/50">
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type your thoughts..."
                className="flex-1 bg-transparent focus:outline-none text-gray-700 placeholder-gray-400 text-base"
                disabled={isLoading}
              />
              <div className="flex items-center gap-3 ml-4">
                <button
                  className="text-gray-500 hover:text-indigo-600 transition-colors p-2"
                  aria-label="Voice input"
                >
                  <FiMic className="text-xl" />
                </button>
                <button
                  onClick={handleSend}
                  disabled={isLoading || !message.trim()}
                  className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-full p-3 hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  aria-label="Send message"
                >
                  <FiSend className="text-lg" />
                </button>
              </div>
            </div>
          </motion.div>
        </div>
      </main>

      {/* Floating Chatbot Mascot - Positioned right side */}
      <motion.div
        className="fixed top-20 right-12 flex flex-col items-center z-50"
        initial={{ opacity: 0, scale: 0, rotate: -180 }}
        animate={{ opacity: 1, scale: 1, rotate: 0 }}
        transition={{ 
          duration: 0.8,
          delay: 0.6,
          type: "spring",
          stiffness: 200
        }}
      >
        {/* Speech Bubble */}
        <AnimatePresence>
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.2 }}
            className="bg-white rounded-2xl shadow-lg px-4 py-2 mb-3 relative"
          >
            <p className="text-sm font-medium text-gray-700 whitespace-nowrap">
              Hi there! 🌈 Need a boost?
            </p>
            {/* Speech bubble tail */}
            <div className="absolute bottom-[-8px] left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-8 border-l-transparent border-r-8 border-r-transparent border-t-8 border-t-white"></div>
          </motion.div>
        </AnimatePresence>
        
        {/* Robot Mascot */}
        <motion.div
          className="w-32 h-32 bg-gradient-to-br from-indigo-500 via-purple-500 to-purple-600 rounded-full flex items-center justify-center shadow-2xl border-4 border-white"
          whileHover={{ scale: 1.1, rotate: 5 }}
          whileTap={{ scale: 0.95 }}
          animate={{ 
            y: [0, -10, 0],
          }}
          transition={{
            y: {
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }
          }}
        >
          <span className="text-6xl">🤖</span>
        </motion.div>
      </motion.div>
    </div>
  );
}
