import React from 'react'
import styles from "./chatInterface.module.css"
import Image from 'next/image'
import NavBar from '../components/navBar/NavBar'
const ChatInterface = () => {
    return (
        <div className={styles.chatInterface}>
            <div className={styles.nav}>
                <NavBar />
            </div>
            <div className={styles.mainContent}>
                <div className={styles.greet}>
                    <p><span>Hello, Shifat.</span></p>
                    <p>How can I help you today?</p>
                </div>
                <div className={styles.cards}>
                    <div className={styles.card}>
                        <p className={styles.cardText}>Suggest beautful places to see on the upcoming road trip</p>
                        <Image src='/help.png' alt="" height={20} width={20} className={styles.image}/>
                    </div>
                    <div className={styles.card}>
                        <p className={styles.cardText}>Briefly summarize this concept: urban planning</p>
                        <Image src='/message.png' alt="" height={20} width={20} className={styles.image} />
                    </div>
                    <div className={styles.card}>
                        <p className={styles.cardText}>Brainstorm team bonding activities for our work retreat</p>
                        <Image src='/gallery.png' alt="" height={20} width={20} className={styles.image} />
                    </div>
                    <div className={styles.card}>
                        <p className={styles.cardText}>Improve the readabilit of the following code.</p>
                        <Image src='/settings.png' alt="" height={20} width={20} className={styles.image} />
                    </div>
                    <div className={`${styles.mainBottom}`}>
                        <div className={styles.searchBox}>
                            <input className={styles.input} type="text" placeholder='Enter a prompt here'/>
                            <div className={styles.serchBoxDiv}>
                                <Image src='/gallery.png' alt="" height={20} width={20} className={styles.serchImage}/>
                                <Image src='/mic.png' alt="" height={20} width={20} className={styles.serchImage}/>
                                <Image src='/send.png' alt="" height={20} width={20} className={styles.serchImage}/>
                            </div>
                        </div>
                        <p className={styles.bottomInfo}>
                            Google Terms Opens in a new window and the Gemini Apps Privacy Notice Opens in a new window apply. Chats are reviewed and used to improve Google AI. Learn about your choices Opens in a new window . Gemini can make mistakes, so double-check it. Info about your location Opens in a new window is also stored with your Gemini Apps activity. 
                        </p>
                    </div>
                </div>
            </div>

        </div>
    )
}

export default ChatInterface
