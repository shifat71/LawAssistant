import ChatInterface from './components/ChatInterface';
import { ThemeProvider } from './providers/ThemeProvider';

export default function Home() {
  return (
    <ThemeProvider>
      <ChatInterface />
    </ThemeProvider>
  );
}
