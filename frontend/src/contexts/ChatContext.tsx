import { createContext, useContext, useState, useCallback } from 'react';
import { SimpleChatMessage, ChatContextType } from '../types/types';
import { useAuth } from './AuthContext';

const ChatContext = createContext<ChatContextType | null>(null);

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

export const ChatProvider = ({ children }: { children: any }) => {
  const [messages, setMessages] = useState<SimpleChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentLanguage, setCurrentLanguage] = useState<'en' | 'hi' | 'raj'>('en');
  const { token } = useAuth();

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || !token) return;

    const userMessage: SimpleChatMessage = {
      id: Date.now().toString(),
      content,
      sender: 'user',
      timestamp: new Date(),
      language: currentLanguage,
    };

    setMessages((prev: any) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: content,
          language: currentLanguage,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();
      
      const botMessage: SimpleChatMessage = {
        id: (Date.now() + 1).toString(),
        content: data.response,
        sender: 'bot',
        timestamp: new Date(),
        language: currentLanguage,
      };

      setMessages((prev: any) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: SimpleChatMessage = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
        language: currentLanguage,
      };
      setMessages((prev: any) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [token, currentLanguage]);

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  const loadChatHistory = useCallback(async () => {
    if (!token) return;

    try {
      const response = await fetch('/api/chat/history', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to load chat history');
      }

      const data = await response.json();
      setMessages(data.messages || []);
    } catch (error) {
      console.error('Error loading chat history:', error);
    }
  }, [token]);

  const changeLanguage = useCallback((language: 'en' | 'hi' | 'raj') => {
    setCurrentLanguage(language);
  }, []);

  const value = {
    messages,
    isLoading,
    currentLanguage,
    sendMessage,
    clearMessages,
    loadChatHistory,
    changeLanguage,
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};