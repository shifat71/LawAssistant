"use client"
import React, { useState } from 'react'
import Image from 'next/image'
import styles from './sideBar.module.css'
const SideBar = () => {

    const [extended, setExtended] = useState(false);

    
    return (
        <div className={styles.sidebar}>
            <div className={styles.top}>
                <Image className={styles.menu} alt="" src={'/ham_burger.png'} height={20} width={20} onClick={()=>setExtended(!extended)}/>
                {extended && <div className={styles.newChat}>
                    <Image className={styles.add} alt="" src={'/add.png'} height={20} width={20} />
                    <p>New Chat</p>
                </div>}
                {extended&& <div className={styles.recent}>
                    <p className={styles.recentTitle}>Recent</p>
                    <div className={styles.recentEntry}>
                        <Image className={styles.message} alt="" src={'/message.png'} height={20} width={20} />
                        <p>What is react ...</p>
                    </div>
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
