"use client";

import React, { useContext, useEffect } from "react";
import { ThemeContext} from "../contextProvider/ThemeContextProvider";
import { ThemeProviderProps } from "../data/data";


const ThemeProvider = ({ children }: ThemeProviderProps) => {
    const { theme } = useContext(ThemeContext);
    useEffect(() => {
        document.body.className = theme; // Apply theme class to body
    }, [theme]);

    return <div>{children}</div>; // No need to redefine ThemeContext.Provider
};

export default ThemeProvider;
