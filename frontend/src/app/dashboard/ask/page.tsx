"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

// Pre-written responses for demo
const MOCK_RESPONSES: Record<string, string> = {
  default:
    "That's a great question! Based on your Sanguinous-Phlegmatic temperament, I'd recommend focusing on balance. For your specific concern, try incorporating cooling foods like cucumber and melon, and practice moderate exercise like brisk walking. Would you like me to elaborate on any particular aspect?",
  food: "For your Sanguinous-Phlegmatic temperament, focus on light, easily digestible meals. Include fresh seasonal fruits, leafy greens, and lean proteins. Avoid heavy, creamy foods and excessive carbohydrates. Warming spices like ginger and cinnamon in moderation can help balance your system.",
  exercise:
    "Your temperament benefits from consistent, moderate exercise. Aim for 30-45 minutes, 5-6 days per week. Brisk walking, swimming, yoga, and cycling are excellent choices. Morning or evening workouts are ideal — avoid intense midday exertion, especially in warm weather.",
  sleep: "To optimise your sleep, establish a consistent routine: wind down by 9:30pm, avoid screens 30 minutes before bed, and keep your bedroom cool (18-20°C). Herbal teas like chamomile or lavender can help. Aim for 7-8 hours of quality rest.",
  stress:
    "When stress arises, try the 5-4-3-2-1 grounding technique: name 5 things you see, 4 you can touch, 3 you hear, 2 you can smell, and 1 you can taste. Also, a 10-minute mindful walk in nature can work wonders for your temperament.",
  seasonal:
    "In early summer, focus on cooling and hydration. Morning walks before 9am, swimming 2-3 times per week, and infused water with cucumber and mint will help balance your warm constitution.",
};

const suggestedQuestions = [
  "What foods should I eat for my temperament?",
  "What exercise routine do you recommend?",
  "How can I improve my sleep quality?",
  "Tips for managing stress?",
  "What's my seasonal protocol for this month?",
];

export default function AskPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "👋 Welcome! I'm your TibbWell AI health assistant. I'm here to help you with personalised wellness advice based on your Sanguinous-Phlegmatic temperament. What would you like to know?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const getResponse = (userMessage: string): string => {
    const lower = userMessage.toLowerCase();
    if (lower.includes("food") || lower.includes("eat") || lower.includes("diet")) {
      return MOCK_RESPONSES.food;
    }
    if (lower.includes("exercise") || lower.includes("workout") || lower.includes("gym") || lower.includes("run")) {
      return MOCK_RESPONSES.exercise;
    }
    if (lower.includes("sleep") || lower.includes("bed") || lower.includes("insomnia") || lower.includes("rest")) {
      return MOCK_RESPONSES.sleep;
    }
    if (lower.includes("stress") || lower.includes("anxiety") || lower.includes("worry") || lower.includes("calm")) {
      return MOCK_RESPONSES.stress;
    }
    if (lower.includes("season") || lower.includes("summer") || lower.includes("winter") || lower.includes("weather")) {
      return MOCK_RESPONSES.seasonal;
    }
    return MOCK_RESPONSES.default;
  };

  const handleSend = async () => {
    if (!input.trim() || isTyping) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    // Simulate AI response delay
    setTimeout(() => {
      const response: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: getResponse(userMessage.content),
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, response]);
      setIsTyping(false);
    }, 1500);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      {/* Chat Header */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-4 mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-wellness-green to-wellness-accent flex items-center justify-center">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <div>
            <h2 className="font-bold text-wellness-dark">TibbWell AI</h2>
            <p className="text-xs text-gray-500">Powered by Unani wisdom • Premium feature</p>
          </div>
          <Link
            href="/dashboard"
            className="ml-auto text-sm text-wellness-green hover:text-wellness-dark transition-colors font-medium"
          >
            Back to Dashboard
          </Link>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4 px-1">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[85%] md:max-w-[70%] rounded-2xl p-4 ${
                msg.role === "user"
                  ? "bg-wellness-green text-white rounded-br-md"
                  : "bg-white border border-gray-100 shadow-sm rounded-bl-md"
              }`}
            >
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
              <p
                className={`text-xs mt-2 ${
                  msg.role === "user" ? "text-white/60" : "text-gray-400"
                }`}
              >
                {msg.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
              </p>
            </div>
          </div>
        ))}

        {/* Typing indicator */}
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-100 shadow-sm rounded-2xl rounded-bl-md p-4">
              <div className="flex gap-1.5">
                <span className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Questions (when no user messages yet) */}
      {messages.length === 1 && (
        <div className="mb-4">
          <p className="text-xs text-gray-500 mb-2">Suggested questions:</p>
          <div className="flex flex-wrap gap-2">
            {suggestedQuestions.map((q) => (
              <button
                key={q}
                onClick={() => {
                  setInput(q);
                }}
                className="text-xs bg-gray-100 hover:bg-wellness-light hover:text-wellness-green text-gray-600 px-3 py-2 rounded-full transition-colors"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-3">
        <div className="flex gap-3">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about your health, diet, exercise, or anything wellness-related..."
            className="flex-1 resize-none border-0 outline-none text-sm text-gray-700 placeholder-gray-400 py-2 max-h-32"
            rows={1}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isTyping}
            className="btn-primary !px-4 !py-2 self-end flex items-center gap-2"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
            <span className="hidden sm:inline">Send</span>
          </button>
        </div>
        <p className="text-[10px] text-gray-400 mt-2">
          TibbWell AI provides general wellness guidance based on Unani-Tibb principles. Always consult a healthcare professional for medical advice.
        </p>
      </div>
    </div>
  );
}