"use client";

import { useEffect, useState } from "react";
import { fetchYouTubeVideos } from "../../utils/youtubeAPI";

interface Video {
  videoId: string;
  thumbnail: string;
  title: string;
}

interface Message {
  text: string;
  sender: "user" | "chatbot";
  videos?: Video[];
}

const ChatPage = () => {
  const [messages, setMessages] = useState<Message[]>([
    { text: "What subject would you like to learn about?", sender: "chatbot" },
  ]);
  const [query, setQuery] = useState<string>("");
  const [isPageVisible, setIsPageVisible] = useState(false);

  useEffect(() => {
    // Trigger fade-in effect
    setTimeout(() => {
      setIsPageVisible(true);
    }, 500); // Delay to sync with fade-to-black transition
  }, []);

  const handleSendMessage = async () => {
    if (query) {
      // Add user message
      setMessages((prev) => [...prev, { text: query, sender: "user" }]);

      // Fetch YouTube videos based on the query
      const videos = await fetchYouTubeVideos(query);

      // Add chatbot response with videos after a slight delay
      setTimeout(() => {
        setMessages((prev) => [
          ...prev,
          {
            text: "Here are some videos I found for you:",
            sender: "chatbot",
            videos: videos || [],
          },
        ]);
      }, 500);

      setQuery(""); // Clear the input field
    }
  };

  return (
    <div
      className={`flex flex-col h-screen bg-gradient-to-b from-white to-purple-100 transition-opacity duration-1000 ${
        isPageVisible ? "opacity-100" : "opacity-0"
      }`}
    >
      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`p-4 max-w-xs rounded-lg shadow-md transform transition-transform duration-300 ease-out ${
                message.sender === "user"
                  ? "bg-purple-500 text-white slide-in-right"
                  : "bg-gray-100 text-gray-800 slide-in-left"
              }`}
            >
              <p>{message.text}</p>
              {message.videos && message.videos.length > 0 && (
                <div className="mt-2 space-y-4">
                  {message.videos.map((video, idx) => (
                    <div
                      key={idx}
                      className="block bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300"
                    >
                      <iframe
                        width="100%"
                        height="200"
                        src={`https://www.youtube.com/embed/${video.videoId}`}
                        title={video.title}
                        frameBorder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                      ></iframe>
                      <div className="p-2">
                        <h3 className="text-sm font-medium text-gray-800">
                          {video.title}
                        </h3>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Input Box */}
      <div className="p-4 bg-white border-t border-gray-200">
        <div className="flex items-center space-x-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-900"
          />
          <button
            onClick={handleSendMessage}
            className="px-4 py-2 bg-purple-500 text-white rounded-lg shadow-md hover:bg-purple-600 transition duration-300"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;