"use client";

import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Send, Loader2, Cpu, Zap } from "lucide-react";
import { MessageBubble } from "./MessageBubble";
import { ReasoningPipeline } from "./ReasoningPipeline";
import { motion, AnimatePresence } from "framer-motion";

interface Message {
    role: "user" | "model";
    content: string;
    type?: "chat" | "build";
    buildData?: any;
}

export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([
        {
            role: "model",
            content: "Hi! I'm **BuildBuddy**. I use AI reasoning to build your perfect PC. What are you looking to build today?\n\n**Examples:**\n- *\"Gaming PC for $1200, 1440p 120fps\"*\n- *\"Streaming setup, $2000 budget\"*\n- *\"Workstation for 3D rendering, $3000\"*",
            type: "chat",
        },
    ]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [activeMode, setActiveMode] = useState<"chat" | "build">("build");
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage: Message = { role: "user", content: input, type: activeMode };
        setMessages((prev) => [...prev, userMessage]);
        setInput("");
        setIsLoading(true);

        try {
            if (activeMode === "build") {
                // Call the multi-agent pipeline endpoint
                const response = await axios.post(
                    "http://localhost:8000/build-pc",
                    {
                        query: input,
                        verbose: true,
                    }
                );

                const data = response.data;

                // Create stage data for visualization
                const stages = [
                    {
                        name: "Build",
                        status: "complete",
                        title: "Initial Configuration",
                        subtitle: "Creating PC build with explicit tool decisions",
                        content: data.reasoning.stage_1_build,
                        icon: Cpu,
                    },
                    {
                        name: "Critique",
                        status: "complete",
                        title: "Problem Detection",
                        subtitle: "Finding issues and risks in the build",
                        content: data.reasoning.stage_2_critique,
                        concernCount: data.reasoning.stage_2_critique?.critique?.concerns?.length || 0,
                    },
                    {
                        name: "Improve",
                        status: "complete",
                        title: "Optimization",
                        subtitle: "Revising build based on critique",
                        content: data.reasoning.stage_3_improvements,
                        changeCount: data.reasoning.stage_3_improvements?.revisions?.changes_made?.length || 0,
                    },
                    {
                        name: "Visualization",
                        status: "complete",
                        title: "Visual Presentation",
                        subtitle: "Generating photorealistic preview",
                        content: data.reasoning.stage_4_visualization,
                    },
                ];

                const aiMessage: Message = {
                    role: "model",
                    content: `I've completed my reasoning process to build your PC!`,
                    type: "build",
                    buildData: {
                        stages,
                        finalBuild: data.build,
                        summary: {
                            initialBudget: data.reasoning.stage_1_build?.build?.total_budget,
                            finalBudget: data.build?.total_budget,
                            concernsFound: stages[1].concernCount,
                            revisionsCount: stages[2].changeCount,
                        },
                    },
                };

                setMessages((prev) => [...prev, aiMessage]);
            } else {
                // Simple chat endpoint
                const response = await axios.post("http://localhost:8000/chat", {
                    message: input,
                });

                const aiMessage: Message = {
                    role: "model",
                    content: response.data.response,
                    type: "chat",
                };

                setMessages((prev) => [...prev, aiMessage]);
            }
        } catch (error: any) {
            const errorMessage: Message = {
                role: "model",
                content: `Error: ${error.response?.data?.detail || error.message}. Make sure the backend is running on port 8000.`,
                type: "chat",
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="h-full flex flex-col bg-gradient-to-br from-gray-900 to-gray-800">
            {/* Header */}
            <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-4 shadow-lg">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <Cpu className="w-8 h-8" />
                        <h1 className="text-2xl font-bold">BuildBuddy AI</h1>
                    </div>
                    <p className="text-sm text-purple-100">Reasoning-Driven PC Builder</p>
                </div>
            </div>

            {/* Mode Selector */}
            <div className="flex gap-2 px-4 py-3 bg-gray-800 border-b border-gray-700">
                <button
                    onClick={() => setActiveMode("build")}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold transition-all ${activeMode === "build"
                        ? "bg-purple-600 text-white shadow-lg"
                        : "bg-gray-700 text-gray-300 hover:bg-gray-600"
                        }`}
                >
                    <Zap className="w-4 h-4" />
                    Reasoning Mode
                </button>
                <button
                    onClick={() => setActiveMode("chat")}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold transition-all ${activeMode === "chat"
                        ? "bg-blue-600 text-white shadow-lg"
                        : "bg-gray-700 text-gray-300 hover:bg-gray-600"
                        }`}
                >
                    <Send className="w-4 h-4" />
                    Chat Mode
                </button>
            </div>

            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                <AnimatePresence mode="popLayout">
                    {messages.map((msg, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.3 }}
                            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                        >
                            {msg.role === "user" ? (
                                <div className="bg-blue-600 text-white rounded-lg p-4 max-w-md shadow-md">
                                    <p className="text-sm">{msg.content}</p>
                                </div>
                            ) : msg.type === "build" && msg.buildData ? (
                                <div className="w-full max-w-2xl">
                                    <div className="bg-gray-700 text-gray-100 rounded-lg p-4 mb-3">
                                        <p className="text-sm">{msg.content}</p>
                                    </div>
                                    <ReasoningPipeline
                                        stages={msg.buildData.stages}
                                        finalBuild={msg.buildData.finalBuild}
                                    />
                                </div>
                            ) : (
                                <MessageBubble role={msg.role} content={msg.content} />
                            )}
                        </motion.div>
                    ))}
                </AnimatePresence>

                {isLoading && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex justify-start"
                    >
                        <div className="bg-gray-700 text-gray-300 rounded-lg p-4 flex items-center gap-2">
                            <Loader2 className="w-4 h-4 animate-spin" />
                            <span className="text-sm">
                                {activeMode === "build"
                                    ? "Running reasoning pipeline..."
                                    : "Thinking..."}
                            </span>
                        </div>
                    </motion.div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input Box */}
            <div className="border-t border-gray-700 bg-gray-800 p-4">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === "Enter" && sendMessage()}
                        placeholder={
                            activeMode === "build"
                                ? "Describe your dream PC (e.g., 'Gaming PC for $1200, 1440p')..."
                                : "Ask about PC components..."
                        }
                        className="flex-1 bg-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-600 placeholder-gray-500"
                        disabled={isLoading}
                    />
                    <button
                        onClick={sendMessage}
                        disabled={isLoading || !input.trim()}
                        className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white rounded-lg px-6 py-3 font-semibold flex items-center gap-2 transition-all disabled:cursor-not-allowed"
                    >
                        {isLoading ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                            <Send className="w-4 h-4" />
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}
