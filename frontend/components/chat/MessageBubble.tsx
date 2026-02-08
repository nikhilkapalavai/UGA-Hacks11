"use client";

import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { motion } from "framer-motion";
import { User, Bot, Sparkles, Volume2 } from "lucide-react";
import clsx from "clsx";

interface MessageBubbleProps {
    role: "user" | "model";
    content: string;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ role, content }) => {
    const isUser = role === "user";
    const [isPlayingAudio, setIsPlayingAudio] = useState(false);

    const handleSpeak = async () => {
        if (isPlayingAudio) return;
        
        try {
            setIsPlayingAudio(true);
            const response = await fetch("http://localhost:8000/tts", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    text: content,
                    voice: "Nova",
                }),
            });

            if (!response.ok) {
                throw new Error("Failed to generate speech");
            }

            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            
            audio.onended = () => {
                setIsPlayingAudio(false);
                URL.revokeObjectURL(audioUrl);
            };
            
            audio.play();
        } catch (error) {
            console.error("Error playing audio:", error);
            setIsPlayingAudio(false);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={clsx(
                "flex w-full mb-6",
                isUser ? "justify-end" : "justify-start"
            )}
        >
            <div
                className={clsx(
                    "flex max-w-[80%] md:max-w-[70%] gap-4",
                    isUser ? "flex-row-reverse" : "flex-row"
                )}
            >
                {/* Avatar */}
                <div
                    className={clsx(
                        "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
                        isUser
                            ? "bg-primary text-primary-foreground"
                            : "bg-accent text-accent-foreground"
                    )}
                >
                    {isUser ? <User size={18} /> : <Sparkles size={18} />}
                </div>

                {/* Message Content */}
                <div
                    className={clsx(
                        "p-4 rounded-2xl shadow-sm text-sm md:text-base overflow-hidden",
                        isUser
                            ? "bg-primary text-primary-foreground rounded-tr-none"
                            : "bg-secondary text-secondary-foreground rounded-tl-none border border-white/10"
                    )}
                >
                    <div className="prose prose-invert max-w-none prose-p:leading-relaxed prose-pre:bg-black/50 prose-pre:p-0">
                        <ReactMarkdown>{content}</ReactMarkdown>
                    </div>
                    {!isUser && (
                        <button
                            onClick={handleSpeak}
                            disabled={isPlayingAudio}
                            className={clsx(
                                "mt-3 flex items-center gap-2 px-3 py-1 rounded-lg text-xs font-medium transition-colors",
                                isPlayingAudio
                                    ? "bg-white/20 text-gray-400 cursor-not-allowed"
                                    : "bg-white/10 hover:bg-white/20 text-white cursor-pointer"
                            )}
                        >
                            <Volume2 size={14} />
                            {isPlayingAudio ? "Playing..." : "Speak"}
                        </button>
                    )}
                </div>
            </div>
        </motion.div>
    );
};
