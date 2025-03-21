const API_BASE_URL = 'http://localhost:8000';  

export type Message = {
  role: 'user' | 'assistant';
  content: string;
};

export async function sendMessage(message: string): Promise<Message> {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error('Failed to send message');
    }

    const data = await response.json();
    return {
      role: 'assistant',
      content: data.response,
    };
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
} 