"use client"
import React, { useContext } from 'react';
import styles from './navbar.module.css';
import ThemeToggle from '../themeToggle/ThemeToggle';
import { ThemeContext } from '../../contextProvider/ThemeContextProvider';
import Image from 'next/image';
const NavBar = () => {
    return (
        <div className={styles.navbar}>
            <div className={styles.logo}>
                <Image src='/logo.png' alt ="" height={30} width={40}/>
            </div>
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
