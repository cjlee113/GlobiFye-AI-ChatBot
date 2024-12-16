"use client";

import { useState } from "react";

export default function HomePage() {
  const [isExiting, setIsExiting] = useState(false);

  const handleExit = () => {
    setIsExiting(true);
    setTimeout(() => {
      window.location.href = "/chatpage";
    }, 500); // Match animation duration
  };

  return (
    <div
      className={`flex flex-col items-center justify-center h-screen bg-gradient-to-b from-purple-400 to-white transition-opacity duration-500 ${
        isExiting ? "opacity-0" : "opacity-100"
      }`}
    >
      <h1 className="text-4xl font-bold text-gray-800 mb-4">
        Welcome to GlobiFYE's Chatbot!
      </h1>
      <p className="text-lg text-gray-700 mb-8">How may I help you today?</p>
      <button
        onClick={handleExit}
        className="px-6 py-3 bg-purple-500 text-white font-medium rounded-lg shadow-md hover:bg-purple-600 transition duration-300"
      >
        Prepare me for an interview
      </button>
    </div>
  );
}