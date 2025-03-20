'use client';

import { useState } from 'react';
import { useTheme } from '../providers/ThemeProvider';

type Message = {
  role: 'user' | 'assistant';
  content: string;
};

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const { theme, toggleTheme } = useTheme();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessage: Message = {
      role: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, newMessage]);
    setInput('');

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: Message = {
        role: 'assistant',
        content: 'This is a simulated AI response. Replace this with actual API calls to your backend.',
      };
      setMessages((prev) => [...prev, aiResponse]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-blue-50 to-white dark:from-black dark:to-gray-900">
      {/* Header */}
      <header className="border-b border-blue-100 dark:border-gray-800 p-4 bg-white/80 dark:bg-black/80 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-semibold text-blue-600 dark:text-blue-400">Law Assistant</h1>
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg hover:bg-blue-50 dark:hover:bg-gray-800 transition-colors duration-200"
          >
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
        </div>
      </header>

      {/* Chat Messages */}
      <main className="flex-1 overflow-y-auto p-4">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-4 shadow-sm ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white hover:bg-blue-600 transition-colors duration-200'
                    : 'bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 border border-blue-100 dark:border-gray-700 hover:bg-blue-50 dark:hover:bg-gray-700 transition-colors duration-200'
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}
        </div>
      </main>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="border-t border-blue-100 dark:border-gray-800 p-4 bg-white/80 dark:bg-black/80 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto flex gap-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 rounded-lg border border-blue-200 dark:border-gray-700 p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 transition-colors duration-200"
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200 font-medium"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
} 