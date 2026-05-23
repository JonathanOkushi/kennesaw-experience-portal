"use client";

import { useState } from "react";

export default function ChatBox() {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage() {
    if (!input.trim() || loading) return;

    const userText = input;
    setInput("");
    setLoading(true);

    setMessages((prev) => [...prev, { role: "user", text: userText }]);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userText }),
      });

      if (!res.ok) {
        throw new Error("Chat request failed");
      }

      const data = await res.json();

      setMessages((prev) => [...prev, { role: "assistant", text: data.reply }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Sorry, something went wrong. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-6 bg-slate-200 text-white rounded-2xl border border-slate-300 border-3">
      <div className="space-y-3 mb-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-3 rounded-xl break-words w-128 ${
              msg.role === "user"
                ? "bg-black ml-auto text-right"
                : "bg-yellow-500 mr-auto"
            }`}
          >
            {msg.text}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-2 w-fit rounded-xl bg-slate-100 px-4 py-3 text-slate-600 shadow-sm">
            <span className="h-3 w-3 rounded-full bg-yellow-500 animate-bounce [animation-delay:-0.2s]" />
            <span className="h-3 w-3 rounded-full bg-yellow-500 animate-bounce [animation-delay:-0.1s]" />
            <span className="h-3 w-3 rounded-full bg-yellow-500 animate-bounce" />
          </div>
        )}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 p-3 rounded-xl text-black bg-white focus:outline-none"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask a question..."
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-yellow-500 px-5 py-3 rounded-xl font-semibold"
        >
          Send
        </button>
      </div>
    </div>
  );
}
