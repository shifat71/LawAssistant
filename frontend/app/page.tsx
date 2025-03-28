import ChatInterface from './components/ChatInterface';
import NavBar from './components/NavBar';
import SideBar from './components/SideBar';
import TextEditor from './components/TextEditor';
import styles from './home.module.css'
export default function Home() {
  return (
      <div className={styles.layout}>
        {/* {console.log()} */}
          <div className={styles.navbar}>
            <NavBar/>
          </div>
          <div className={styles.body}>

              <div className={styles.sidebar}>
                <SideBar/>
              </div>

              <div className={styles.content}>
                <TextEditor/>
              </div>
          </div>
      </div>
  );
}
