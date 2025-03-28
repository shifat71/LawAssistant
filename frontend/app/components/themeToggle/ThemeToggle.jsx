"use client";

import React, { useContext } from "react";
import Image from "next/image";
import styles from "./themeToggle.module.css";
import { ThemeContext } from "../../contextProvider/ThemeContextProvider";
const ThemeToggle = () => {
    const { toggle, theme } = useContext(ThemeContext);

    return (
        <div
            className={styles.container}
            onClick={toggle}
            style={{
                backgroundColor: theme === "dark" ? "white" : "black",
            }}
        >
            <Image src="/moon.png" alt="Moon Icon" width={14} height={14} />
            <div
                className={styles.ball}
                style={{
                    transform: theme === "dark" ? "translateX(20px)" : "translateX(0px)",
                    backgroundColor: theme === "dark" ? "black" : "white",
                }}
            />
            <Image src="/sun.png" alt="Sun Icon" width={14} height={14} />
        </div>
    );
};

export default ThemeToggle;
