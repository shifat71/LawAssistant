"use client"
import React, { useState } from 'react'
import Image from 'next/image'
import styles from './sideBar.module.css'
import { useChatContext } from '@/app/contextProvider/ChatContext'

const SideBar = () => {

    const [extended, setExtended] = useState(false);
    const { onSent, prevPrompts, setRecentPrompt, newChat } = useChatContext();
    
    const loadPrompt = async (prompt: string) => {
        setRecentPrompt(prompt);
        await onSent(prompt);
    }

    return (
        <div className={styles.sidebar}>
            <div className={styles.top}>
                <Image className={styles.menu} alt="" src={'/ham_burger.png'} height={20} width={20} onClick={()=>setExtended(!extended)}/>
                {extended && <div onClick={newChat} className={styles.newChat}>
                    <Image className={styles.add} alt="" src={'/add.png'} height={20} width={20} />
                    <p>New Chat</p>
                </div>}
                {extended&& <div className={styles.recent}>
                    <p className={styles.recentTitle}>Recent</p>
                    {prevPrompts.map((item, index) => {
                        return (
                            <div onClick={() => loadPrompt(item)} className={styles.recentEntry} key={index}>
                                <Image className={styles.message} alt="" src={'/message.png'} height={20} width={20} />
                                <p>{item.slice(0, 18)} ...</p>
                            </div>
                        )
                    })}
                    {/* <div className={styles.recentEntry}>
                        <Image className={styles.message} alt="" src={'/message.png'} height={20} width={20} />
                        <p>What is react ...</p>
                    </div> */}
                </div>}
            </div>
            {extended && <div className={styles.bottom}>
                <div className={`${styles.bottomItem} ${styles.recentEntry}`}>
                    <Image className={styles.message} alt="" src={'/help.png'} height={20} width={20} />
                    <p>Help</p>
                </div>
                <div className={`${styles.bottomItem} ${styles.recentEntry}`}>
                    <Image className={styles.message} alt="" src={'/activity.png'} height={20} width={20} />
                    <p>Activity</p>
                </div>
                <div className={`${styles.bottomItem} ${styles.recentEntry}`}>
                    <Image className={styles.message} alt="" src={'/settings.png'} height={20} width={20} />
                    <p>Settings</p>
                </div>
            </div>}
        </div>
    )
}

export default SideBar
