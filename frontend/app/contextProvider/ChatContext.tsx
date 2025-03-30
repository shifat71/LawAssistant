"use client";

import { createContext, ReactNode, useContext, useState } from "react";
import runChat from "../config/gemini";
import { ChatContextType } from "../data/data";



// Create context with default undefined value
export const ChatContext = createContext<ChatContextType | undefined>(undefined);

interface Props {
    children: ReactNode;
}

// Create the actual provider component
export const ChatContextProvider = ({ children }: Props) => {
    const [input, setInput] = useState<string>("");
    const [recentPrompt, setRecentPrompt] = useState<string>("");
    const [prevPrompts, setPrevPrompts] = useState<string[]>([]);
    const [showResult, setShowResult] = useState(false);
    const [loading, setLoading] = useState(false);
    const [resultData, setResultData] = useState<string>("");

    // Format markdown-like syntax into HTML
    // const applyFormatting = (text: string): string => {
    //     return text
    // };

    const delayPara = (index: number, nextWord: string) => {
        setTimeout(function () {
            setResultData(prev => prev + nextWord + " ");
        }, 150 * index);
        // Optional for future animation
    };

    const newChat =()=>{
        setLoading(false);
        setShowResult(false);
    }
    const onSent = async (prompt?: string) => {
        setResultData("");
        setLoading(true);
        setShowResult(true);
        let response;
        
        if (prompt !== undefined) {
            response = await runChat(prompt);
            setRecentPrompt(prompt);
        } else {
            setPrevPrompts(prev => [...prev, input]);
            setRecentPrompt(input);
            response = await runChat(input);
        }

        let newResponeArray = response.split(" ");
        for (let i = 0; i < newResponeArray.length; i++) {
            const nextWord = newResponeArray[i];
            delayPara(i, nextWord);
        }
        setLoading(false);
        setInput("");
    };

    return (
        <ChatContext.Provider value={{
            input,
            recentPrompt,
            prevPrompts,
            showResult,
            loading,
            resultData,
            setInput,
            setRecentPrompt,
            setPrevPrompts,
            onSent,
            newChat
        }}>
            {children}
        </ChatContext.Provider>
    );
};

export default ChatContextProvider;

// Optional: Custom hook for easier usage
export const useChatContext = () => {
    const context = useContext(ChatContext);
    if (!context) {
        throw new Error("useChatContext must be used within ChatContextProvider");
    }
    return context;
};
