import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  FiHome,
  FiBookOpen,
  FiSettings,
  FiUser,
  FiSend,
  FiMic,
} from "react-icons/fi";

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || "/api";

// Debug logging
if (typeof window !== 'undefined') {
  console.log('🔧 API_BASE_URL:', API_BASE_URL);
  console.log('🔧 VITE_BACKEND_URL:', import.meta.env.VITE_BACKEND_URL);
}

export default function SerenityDashboard() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [workflowInfo, setWorkflowInfo] = useState(null);

  const sendMessage = async (messageText) => {
    console.log("🔵 sendMessage called!", messageText);
    console.log("📍 API_BASE_URL being used:", API_BASE_URL);
    if (!messageText.trim() || isLoading) {
      console.log("❌ Blocked - empty or loading");
      return;
    }

    const userMessage = messageText.trim();
    setMessage("");

    // Add user message to UI immediately
    setChatHistory((prev) => [
      ...prev,
      {
        type: "user",
        text: userMessage,
      },
    ]);

    setIsLoading(true);

    try {
      // Call your multi-agent backend
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
          session_id: sessionId, // Pass session ID for conversation continuity
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update session ID
      if (data.session_id) {
        setSessionId(data.session_id);
      }

      // Add bot response to chat history
      setChatHistory((prev) => [
        ...prev,
        {
          type: "assistant",
          text:
            data.response ||
            data.reply ||
            "I apologize, I couldn't generate a response.",
          workflow: data.workflow || {},
          approved: data.approved !== undefined ? data.approved : true,
        },
      ]);

      // Update workflow info for sidebar/display
      if (data.workflow) {
        setWorkflowInfo({
          routing: data.workflow.routing || data.workflow.specialist || "N/A",
          judgeScore:
            data.workflow.judge_score || data.workflow.overall_score || 0,
          safetyPassed:
            data.workflow.safety_passed !== undefined
              ? data.workflow.safety_passed
              : true,
          approved: data.approved !== undefined ? data.approved : true,
        });
      }
    } catch (error) {
      console.error("Error:", error);
      setChatHistory((prev) => [
        ...prev,
        {
          type: "error",
          text: `Unable to connect to the server. Please check if the backend is running. (${error.message})`,
        },
      ]);
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
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleClearChat = () => {
    setChatHistory([]);
    setSessionId(null);
    setWorkflowInfo(null);
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
          <FiHome
            className="hover:text-indigo-600 cursor-pointer transition-colors"
            title="Home"
          />
          <FiBookOpen
            className="hover:text-indigo-600 cursor-pointer transition-colors"
            title="Library"
          />
          <FiUser
            className="hover:text-indigo-600 cursor-pointer transition-colors"
            title="Profile"
          />
          <FiSettings
            className="hover:text-indigo-600 cursor-pointer transition-colors"
            title="Settings"
            onClick={handleClearChat}
          />
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
                onClick={() =>
                  handleCardClick(
                    "I'm feeling anxious and could use some support",
                  )
                }
                className="bg-white/70 backdrop-blur-md rounded-3xl shadow-xl p-8 cursor-pointer border border-white/50 transition-all hover:shadow-2xl"
              >
                <div className="text-5xl mb-4">😊</div>
                <h3 className="text-2xl font-semibold mb-2 text-gray-800">
                  I feel anxious
                </h3>
                <p className="text-gray-600 text-sm">Get support</p>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.05, y: -5 }}
                whileTap={{ scale: 0.98 }}
                onClick={() =>
                  handleCardClick(
                    "I'm doing okay, just wanted to check in and have a chat",
                  )
                }
                className="bg-white/70 backdrop-blur-md rounded-3xl shadow-xl p-8 cursor-pointer border border-white/50 transition-all hover:shadow-2xl"
              >
                <div className="text-5xl mb-4">🔒</div>
                <h3 className="text-2xl font-semibold mb-2 text-gray-800">
                  I'm doing okay
                </h3>
                <p className="text-gray-600 text-sm">Let's have a chat</p>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.05, y: -5 }}
                whileTap={{ scale: 0.98 }}
                onClick={() =>
                  handleCardClick(
                    "I need help now and need to talk to someone urgently",
                  )
                }
                className="bg-white/70 backdrop-blur-md rounded-3xl shadow-xl p-8 cursor-pointer border border-white/50 transition-all hover:shadow-2xl"
              >
                <div className="text-5xl mb-4">⚠️</div>
                <h3 className="text-2xl font-semibold mb-2 text-gray-800">
                  I need help now
                </h3>
                <p className="text-gray-600 text-sm">Access resources</p>
              </motion.div>
            </motion.div>
          )}

          {/* Chat History */}
          {chatHistory.length > 0 && (
            <motion.div
              className="bg-white/70 backdrop-blur-md rounded-3xl shadow-xl p-8 mb-32 max-h-96 overflow-y-auto border border-white/50 scroll-smooth"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <AnimatePresence>
                {chatHistory.map((msg, index) => (
                  <motion.div
                    key={index}
                    className={`mb-4 ${msg.type === "user" ? "text-right" : "text-left"}`}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <div
                      className={`inline-block max-w-[80%] p-4 rounded-2xl ${
                        msg.type === "user"
                          ? "bg-gradient-to-r from-indigo-600 to-purple-600 text-white"
                          : msg.type === "error"
                            ? "bg-red-100 text-red-800"
                            : "bg-gray-100 text-gray-900"
                      }`}
                    >
                      <p className="whitespace-pre-wrap leading-relaxed">
                        {msg.text}
                      </p>

                      {/* Show workflow info for bot messages */}
                      {msg.workflow && msg.type === "assistant" && (
                        <div className="mt-3 pt-3 border-t border-gray-300/50">
                          <div className="flex flex-wrap gap-2 text-xs">
                            {msg.workflow.routing && (
                              <span className="bg-indigo-200 text-indigo-800 px-2 py-1 rounded-full">
                                🔀 {msg.workflow.routing}
                              </span>
                            )}
                            {msg.workflow.judgeScore !== undefined && (
                              <span className="bg-purple-200 text-purple-800 px-2 py-1 rounded-full">
                                ⚖️ {msg.workflow.judgeScore}/10
                              </span>
                            )}
                            {msg.approved && (
                              <span className="bg-green-200 text-green-800 px-2 py-1 rounded-full">
                                ✓ Approved
                              </span>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>

              {/* Typing indicator */}
              {isLoading && (
                <motion.div
                  className="text-left mb-4"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <div className="inline-block bg-gray-100 text-gray-900 p-4 rounded-2xl">
                    <div className="flex gap-2">
                      <span className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"></span>
                      <span className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce delay-75"></span>
                      <span className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce delay-150"></span>
                    </div>
                  </div>
                </motion.div>
              )}
            </motion.div>
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
                  title="Voice input (coming soon)"
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

      {/* Workflow Info Sidebar - Shows when chatting */}
      {workflowInfo && chatHistory.length > 0 && (
        <motion.div
          className="fixed right-8 top-32 bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-6 w-72 border border-white/50"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <h3 className="text-lg font-bold mb-4 text-gray-800">
            🔍 System Workflow
          </h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-indigo-50 rounded-lg">
              <span className="text-sm font-medium text-gray-700">
                🛡️ Safety
              </span>
              <span
                className={`text-sm font-bold ${workflowInfo.safetyPassed ? "text-green-600" : "text-red-600"}`}
              >
                {workflowInfo.safetyPassed ? "Passed" : "Review"}
              </span>
            </div>

            <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
              <span className="text-sm font-medium text-gray-700">
                🔀 Routed To
              </span>
              <span className="text-sm font-bold text-purple-700 capitalize">
                {workflowInfo.routing}
              </span>
            </div>

            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <span className="text-sm font-medium text-gray-700">
                ⚖️ Quality Score
              </span>
              <span className="text-sm font-bold text-blue-700">
                {workflowInfo.judgeScore}/10
              </span>
            </div>

            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <span className="text-sm font-medium text-gray-700">
                ✅ Status
              </span>
              <span className="text-sm font-bold text-green-700">
                {workflowInfo.approved ? "Approved" : "Review"}
              </span>
            </div>
          </div>

          <p className="text-xs text-gray-500 mt-4 text-center">
            Multi-Agent AI System
          </p>
        </motion.div>
      )}

      {/* Floating Chatbot Mascot - Positioned right side */}
      <motion.div
        className="fixed top-20 right-12 flex flex-col items-center z-50"
        initial={{ opacity: 0, scale: 0, rotate: -180 }}
        animate={{ opacity: 1, scale: 1, rotate: 0 }}
        transition={{
          duration: 0.8,
          delay: 0.6,
          type: "spring",
          stiffness: 200,
        }}
      >
        {/* Speech Bubble */}
        <AnimatePresence>
          {chatHistory.length === 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ delay: 1.2 }}
              className="bg-white rounded-2xl shadow-lg px-4 py-2 mb-3 relative"
            >
              <p className="text-sm font-medium text-gray-700 whitespace-nowrap">
                Hi there! 🌈 Need a boost?
              </p>
              {/* Speech bubble tail */}
              <div className="absolute bottom-[-8px] left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-8 border-l-transparent border-r-8 border-r-transparent border-t-8 border-t-white"></div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Robot Mascot */}
        <motion.div
          className="w-32 h-32 bg-gradient-to-br from-indigo-500 via-purple-500 to-purple-600 rounded-full flex items-center justify-center shadow-2xl border-4 border-white cursor-pointer"
          whileHover={{ scale: 1.1, rotate: 5 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleClearChat}
          animate={{
            y: [0, -10, 0],
          }}
          transition={{
            y: {
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut",
            },
          }}
          title="Click to reset chat"
        >
          <span className="text-6xl">🤖</span>
        </motion.div>
      </motion.div>
    </div>
  );
}
