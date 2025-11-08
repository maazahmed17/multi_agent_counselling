import { useState } from "react";
import { motion } from "framer-motion";
import { FiHome, FiBookOpen, FiSettings, FiUser, FiSend, FiMic } from "react-icons/fi";

export default function SerenityDashboard() {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (!message.trim()) return;
    console.log("User message:", message);
    setMessage("");
  };

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-[#E0E9FF] to-[#F6F6F9] text-gray-900">
      {/* Sidebar */}
      <aside className="w-20 flex flex-col items-center py-8 space-y-6 bg-white/50 backdrop-blur-xl rounded-r-3xl shadow-md">
        <div className="w-12 h-12 flex items-center justify-center rounded-full bg-indigo-600 text-white text-2xl font-bold">M</div>
        <nav className="flex flex-col gap-6 text-gray-600 text-2xl">
          <FiHome className="hover:text-indigo-600 cursor-pointer transition" />
          <FiBookOpen className="hover:text-indigo-600 cursor-pointer transition" />
          <FiUser className="hover:text-indigo-600 cursor-pointer transition" />
          <FiSettings className="hover:text-indigo-600 cursor-pointer transition" />
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col justify-center px-16 py-10 relative">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-semibold mb-10">
            Hi, Ready to Start Your <span className="text-indigo-600">Healing Journey?</span>
          </h1>

          {/* Cards */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <motion.div whileHover={{ scale: 1.05 }} className="bg-white rounded-2xl shadow-lg p-6 cursor-pointer">
              <div className="text-4xl mb-3">😊</div>
              <h3 className="text-xl font-semibold mb-1">I feel anxious</h3>
              <p className="text-gray-500 text-sm">Get support</p>
            </motion.div>

            <motion.div whileHover={{ scale: 1.05 }} className="bg-white rounded-2xl shadow-lg p-6 cursor-pointer">
              <div className="text-4xl mb-3">🔒</div>
              <h3 className="text-xl font-semibold mb-1">I'm doing okay</h3>
              <p className="text-gray-500 text-sm">Let's have a chat</p>
            </motion.div>

            <motion.div whileHover={{ scale: 1.05 }} className="bg-white rounded-2xl shadow-lg p-6 cursor-pointer">
              <div className="text-4xl mb-3">⚠️</div>
              <h3 className="text-xl font-semibold mb-1">I need help now</h3>
              <p className="text-gray-500 text-sm">Access resources</p>
            </motion.div>
          </div>

          {/* Chat Input */}
          <div className="flex items-center bg-white rounded-full shadow-lg px-6 py-3 w-full max-w-2xl mx-auto">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type your thoughts..."
              className="flex-1 bg-transparent focus:outline-none text-gray-700"
            />
            <div className="flex items-center gap-4">
              <FiMic className="text-gray-500 text-xl cursor-pointer hover:text-indigo-600 transition" />
              <button
                onClick={handleSend}
                className="bg-indigo-600 text-white rounded-full p-2 hover:bg-indigo-700 transition"
              >
                <FiSend />
              </button>
            </div>
          </div>
        </div>

        {/* Mascot */}
        <motion.div
          className="absolute top-20 right-32 flex flex-col items-center"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          <div className="bg-white rounded-2xl shadow-md px-4 py-2 text-sm mb-2">
            Hi there! 🌈 Need a boost?
          </div>
          <div className="w-24 h-24 bg-gradient-to-br from-indigo-500 to-purple-400 rounded-full flex items-center justify-center text-white text-3xl font-bold shadow-lg">
            🤖
          </div>
        </motion.div>
      </main>
    </div>
  );
}
