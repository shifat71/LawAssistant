"use client";

import React, { useContext, useEffect } from "react";
import { ThemeContext} from "../contextProvider/ThemeContextProvider";

interface ThemeProviderProps {
  children: React.ReactNode;
}

const ThemeProvider = ({ children }: ThemeProviderProps) => {
    const { theme } = useContext(ThemeContext);
    console.log(theme);
    useEffect(() => {
        document.body.className = theme; // Apply theme class to body
    }, [theme]);

    return <div>{children}</div>; // No need to redefine ThemeContext.Provider
};

export default ThemeProvider;
