"use client";
//In your ThemeContextProvider, {children} is a special prop that allows this component to wrap other components and pass down the theme and toggleTheme values.
import { createContext, useState, useEffect } from "react";

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggle: () => void;
}

// Initialize context with proper type
export const ThemeContext = createContext<ThemeContextType>({
  theme: 'dark',
  setTheme: () => null,
  toggle: () => null,
});

interface ThemeContextProviderProps {
  children: React.ReactNode;
}

export const ThemeContextProvider = ({ children }: ThemeContextProviderProps) => {
    //In React, the UI updates when the component re-renders. This happens only when state (useState) or props change. If you use a regular variable instead of useState, React won't know that the value changed, and the UI will not update.
    const [theme, setTheme] = useState<Theme>('light');

    useEffect(() => {
        const storedTheme = localStorage.getItem("theme") as Theme;
        if (storedTheme) setTheme(storedTheme);
    }, []);

    const toggleTheme = () => {
        const newTheme = theme === "light" ? "dark" : "light";
        setTheme(newTheme);
        localStorage.setItem("theme", newTheme);
    };

    return (
        <ThemeContext.Provider value={{ theme, setTheme, toggle: toggleTheme }}>
            {children}{/*✅ It allows all pages in the app to access theme and toggleTheme*/}
        </ThemeContext.Provider>
    );
};
