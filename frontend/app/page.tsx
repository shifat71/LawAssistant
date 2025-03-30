import ChatInterface from './components/chatInterface/ChatInterface';
import SideBar from './components/sideBar/SideBar';
import styles from "./home.module.css"
export default function Home() {
  return (
      <div className={styles.main}>
        <SideBar/>
        <ChatInterface/>
      </div>
  );
}
