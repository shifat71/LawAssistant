"use client"
import React, { useContext } from 'react';
import styles from './navbar.module.css';
import ThemeToggle from '../themeToggle/ThemeToggle';
import { ThemeContext } from '../../contextProvider/ThemeContextProvider';
const NavBar = () => {
    return (
        <div className={styles.navbar}>
            <div className={styles.logo}>Logo</div>
            <div className={styles.buttons}>
                <ThemeToggle/>
                <button className={`${styles.login} ${styles.button}`}>
                    Login
                </button>
                <button className={`${styles.signup} ${styles.button}`}>
                    Signup
                </button>
            </div>
        </div>
    );
};

export default NavBar;
