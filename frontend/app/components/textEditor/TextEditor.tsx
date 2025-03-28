"use client"
import React, { useState } from 'react';
import styles from "./textEditor.module.css";

const TextEditor = () => {
    const [text, setText] = useState("");

    return (
        <div className={styles.wrapper}>
            <div className={styles.inputWrapper}>
                <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Ask your legal question here..."
                    className={styles.textarea}
                />
            </div>
            <div className={styles.options}>
                <button className={`${styles.button} ${styles.primary}`}>
                    Send Message
                </button>

            </div>
        </div>
    );
};

export default TextEditor;
