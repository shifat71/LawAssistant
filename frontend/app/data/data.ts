export interface ThemeProviderProps {
    children: React.ReactNode;
}

export interface ChatContextType {
    input: string;
    recentPrompt: string;
    prevPrompts: string[];
    showResult: boolean;
    loading: boolean;
    resultData: string;
    setInput: (val: string) => void;
    setRecentPrompt: (val: string) => void;
    setPrevPrompts: React.Dispatch<React.SetStateAction<string[]>>;
    onSent: (prompt?: string) => Promise<void>;
    newChat: () => void;
}