
import React, { useState, useEffect, useCallback } from 'react';
import { ChatMessageData, ChatSender, ChatPersona, ChatSettings } from '../../types';
import ChatWindow from './ChatWindow';
import ChatInput from './ChatInput';
import FlowCard from '../FlowCard';
import chatGeminiService from '../../services/chatGeminiService';
import { summarizeChatHistoryForNarrative } from '../../services/geminiService'; // Import the new service
import { saveChatMessages, loadChatMessages, saveChatSettings, loadChatSettings } from '../../services/chatLocalStorageService';
import { MessageCircleIcon, Settings2Icon, Trash2Icon, RefreshCwIcon, Volume2Icon, SquareIcon, UserIcon, FilePenLineIcon, LoaderIcon } from '../icons/LucideIcons'; 

const ASSISTANT_PERSONA: ChatPersona = {
  id: 'trading-assistant',
  name: 'Trading Narrative Assistant',
  avatar: <MessageCircleIcon className="w-5 h-5" />,
  systemInstruction: `You are a friendly and helpful AI assistant for traders. 
Your primary goal is to help the user formulate a clear and concise trading narrative that can be used as input for a JGTML (Juno Markets Trading Meta Language) specification.
Focus on understanding the user's market observations, their analysis of indicators, chart patterns, and their overall trading strategy ideas.
Help them articulate these thoughts clearly. You can ask clarifying questions.
Do NOT provide financial advice, predict market movements, or suggest specific trades.
You can explain trading concepts if asked.
Keep your responses helpful and focused on crafting the narrative.
If the user asks about JGTML components specifically, you can explain them conceptually but remind them the final spec generation is a separate step.
Example interaction:
User: "I'm seeing a double top on EURUSD H4."
You: "Okay, a double top on EURUSD H4. What other indicators or context are you considering with this pattern? For example, what's the current trend, or are there any MAs supporting this?"
User: "The Alligator is sleeping."
You: "Noted, the Alligator is sleeping, suggesting a ranging market or consolidation. How does this fit with your double top observation?"
User: "So, I expect a breakout to the downside if the neckline breaks."
You: "Great. So, to summarize your narrative so far for a potential JGTML spec: 'Observation of a double top pattern on EURUSD H4. The Alligator is currently sleeping, indicating market consolidation. The strategy anticipates a bearish breakout if the pattern's neckline is breached.' Does that sound right, or would you like to refine it further?"
Be concise in your responses unless asked for detail.`
};

// Helper to convert File/Blob to Base64
const toBase64 = (file: File | Blob): Promise<string> => new Promise((resolve, reject) => {
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = () => resolve((reader.result as string).split(',')[1]); // Get only base64 part
  reader.onerror = error => reject(error);
});

interface ChatAssistantContainerProps {
  onUpdateNarrative: (narrative: string) => void;
}

const ChatAssistantContainer: React.FC<ChatAssistantContainerProps> = ({ onUpdateNarrative }) => {
  const [messages, setMessages] = useState<ChatMessageData[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false); // For regular chat messages
  const [isSummarizingNarrative, setIsSummarizingNarrative] = useState<boolean>(false); // For summary generation
  const [chatError, setChatError] = useState<string | null>(null);
  const [isInitialized, setIsInitialized] = useState<boolean>(false);
  const [showSettings, setShowSettings] = useState<boolean>(false);
  const [chatSettings, setChatSettings] = useState<ChatSettings>(loadChatSettings());

  const initializeAssistant = useCallback(async () => {
    setIsLoading(true);
    setChatError(null);
    try {
      const storedMessagesWithAvatars: ChatMessageData[] = loadChatMessages().map(msg => ({
        ...msg,
         avatar: msg.sender === ChatSender.User
                  ? (typeof msg.avatar === 'string' ? msg.avatar : <UserIcon className="w-6 h-6 text-purple-600" />)
                  : (typeof msg.avatar === 'string' ? msg.avatar : ASSISTANT_PERSONA.avatar),
      }));
      
      await chatGeminiService.initializeChat(ASSISTANT_PERSONA, storedMessagesWithAvatars);
      
      if (storedMessagesWithAvatars.length > 0) {
        setMessages(storedMessagesWithAvatars);
      } else {
        const welcomeMessage: ChatMessageData = {
          id: crypto.randomUUID(),
          text: `Hello! I'm the ${ASSISTANT_PERSONA.name}. How can I help you formulate your trading narrative today?`,
          sender: ChatSender.AI,
          timestamp: new Date(),
          avatar: ASSISTANT_PERSONA.avatar,
        };
        setMessages([welcomeMessage]);
      }
      setIsInitialized(true);
    } catch (err) {
      console.error("Error initializing chat assistant:", err);
      const errorMessage = (err as Error).message || "Failed to initialize chat assistant.";
      setChatError(errorMessage);
      const systemError: ChatMessageData = {
        id: crypto.randomUUID(),
        text: `Error initializing assistant: ${errorMessage}. Please check your API key or network.`,
        sender: ChatSender.System,
        timestamp: new Date(),
        isError: true,
      };
      setMessages(prev => [...prev, systemError]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!isInitialized) {
      initializeAssistant();
    }
  }, [isInitialized, initializeAssistant]);
  
  useEffect(() => {
    saveChatMessages(messages);
  }, [messages]);

  useEffect(() => {
    saveChatSettings(chatSettings);
  }, [chatSettings]);

  const handleSendMessage = async (data: {
    text: string;
    file?: File | null; 
    base64ImageData?: string | null; 
    imageMimeType?: string | null;
    recordedAudio?: Blob | null;
    audioMimeType?: string | null;
  }) => {
    if (!data.text.trim() && !data.file && !data.base64ImageData && !data.recordedAudio) return;

    const userMessage: ChatMessageData = {
      id: crypto.randomUUID(),
      text: data.text,
      sender: ChatSender.User,
      timestamp: new Date(),
      avatar: <UserIcon className="w-6 h-6 text-purple-600" />,
      fileName: data.file?.name,
      imageMimeType: data.imageMimeType || data.file?.type,
      audioMimeType: data.audioMimeType,
    };

    if (data.file) {
      userMessage.imagePreviewUrl = URL.createObjectURL(data.file);
      userMessage.base64ImageData = await toBase64(data.file);
    } else if (data.base64ImageData && data.imageMimeType) {
      userMessage.base64ImageData = data.base64ImageData;
      userMessage.imagePreviewUrl = `data:${data.imageMimeType};base64,${data.base64ImageData}`;
    }

    if (data.recordedAudio && data.audioMimeType) {
      userMessage.audioDataUrl = URL.createObjectURL(data.recordedAudio);
    }
    
    setMessages(prevMessages => [...prevMessages, userMessage]);
    
    if (data.text.trim()) {
        setIsLoading(true);
        setChatError(null);

        let fullAiResponse = "";
        let aiMessageId = crypto.randomUUID();

        const aiPlaceholderMessage: ChatMessageData = {
            id: aiMessageId,
            text: "",
            sender: ChatSender.AI,
            timestamp: new Date(),
            avatar: ASSISTANT_PERSONA.avatar,
        };
        setMessages(prevMessages => [...prevMessages, aiPlaceholderMessage]);

        await chatGeminiService.sendMessageStream(
          data.text,
          (chunkText) => { 
            fullAiResponse += chunkText;
            setMessages(prevMessages => 
                prevMessages.map(msg => 
                    msg.id === aiMessageId ? { ...msg, text: fullAiResponse } : msg
                )
            );
          },
          (error, isDefinitive) => { 
            console.error("Chat API error:", error.message);
            const errorMessage = error.message || "Unknown error occurred.";
            setChatError(errorMessage);
            const errorText = `Sorry, I encountered an error: ${errorMessage}${isDefinitive ? " This might be a persistent issue (e.g. API Key or quota)." : ""}`;
            setMessages(prevMessages => 
                prevMessages.map(msg => 
                    msg.id === aiMessageId ? { ...msg, text: errorText, isError: true } : msg
                )
            );
            setIsLoading(false);
          },
          () => { 
            setIsLoading(false);
          }
        );
    }
  };

  const handleClearChat = async () => {
    setIsLoading(true);
    setMessages([]);
    saveChatMessages([]); 
    await chatGeminiService.initializeChat(ASSISTANT_PERSONA, []); 
    const welcomeMessage: ChatMessageData = {
      id: crypto.randomUUID(),
      text: `Chat cleared. How can I assist you now?`,
      sender: ChatSender.AI,
      timestamp: new Date(),
      avatar: ASSISTANT_PERSONA.avatar,
    };
    setMessages([welcomeMessage]);
    setIsLoading(false);
  };

  const toggleAutoPlayTTS = () => {
    setChatSettings(prev => ({ ...prev, autoPlayTTS: !prev.autoPlayTTS }));
  };

  const handleUseSummaryForNarrative = async () => {
    if (messages.filter(m => m.sender !== ChatSender.System && m.text.trim() !== "").length === 0) {
      alert("Chat history is empty or contains no relevant text to summarize.");
      return;
    }
    setIsSummarizingNarrative(true);
    setChatError(null);
    try {
      const narrativeSummary = await summarizeChatHistoryForNarrative(messages);
      onUpdateNarrative(narrativeSummary);
      // Optional: Add a toast notification for success
      // alert("Narrative updated from assistant's summary.");
    } catch (error) {
      console.error("Error summarizing narrative:", error);
      const errorMessage = (error as Error).message || "Failed to summarize narrative.";
      setChatError(errorMessage);
      alert(`Error updating narrative: ${errorMessage}`);
    } finally {
      setIsSummarizingNarrative(false);
    }
  };

  return (
    <FlowCard
      title="💬 Trading Narrative Assistant"
      description="Chat with an AI to help formulate and refine your trading intent narrative. You can attach images or record audio notes."
      icon={<MessageCircleIcon className="w-6 h-6 text-cyan-600" />}
      bgColorClass="bg-cyan-50"
      titleExtra={
        <div className="flex items-center space-x-1 sm:space-x-2">
          <button
            onClick={handleUseSummaryForNarrative}
            disabled={isLoading || isSummarizingNarrative || messages.filter(m => m.sender !== ChatSender.System && m.text.trim() !== "").length === 0}
            className="p-1.5 rounded-md hover:bg-cyan-100 text-cyan-700 focus:outline-none disabled:opacity-50 flex items-center text-xs sm:text-sm"
            title="Use Assistant's Summary for Main Narrative"
            aria-label="Use Assistant's Summary for Main Narrative"
          >
            {isSummarizingNarrative ? <LoaderIcon className="w-4 h-4 sm:w-5 sm:h-5 mr-1" /> : <FilePenLineIcon className="w-4 h-4 sm:w-5 sm:h-5 mr-1" />}
            {isSummarizingNarrative ? 'Summarizing...' : 'Use Summary'}
          </button>
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-1.5 rounded-md hover:bg-cyan-100 text-cyan-700 focus:outline-none"
            title="Chat Settings"
            aria-label="Chat Settings"
            disabled={isLoading || isSummarizingNarrative}
          >
            <Settings2Icon className="w-4 h-4 sm:w-5 sm:h-5" />
          </button>
           <button
            onClick={initializeAssistant}
            disabled={isLoading || isSummarizingNarrative}
            className="p-1.5 rounded-md hover:bg-cyan-100 text-cyan-700 focus:outline-none disabled:opacity-50"
            title="Refresh Assistant Connection"
            aria-label="Refresh Assistant Connection"
          >
            <RefreshCwIcon className="w-4 h-4 sm:w-5 sm:h-5" />
          </button>
          <button
            onClick={handleClearChat}
            disabled={isLoading || isSummarizingNarrative}
            className="p-1.5 rounded-md hover:bg-red-100 text-red-600 focus:outline-none disabled:opacity-50"
            title="Clear Chat History"
            aria-label="Clear Chat History"
          >
            <Trash2Icon className="w-4 h-4 sm:w-5 sm:h-5" />
          </button>
        </div>
      }
    >
      {showSettings && (
        <div className="p-3 mb-3 border border-cyan-200 bg-white rounded-md shadow">
          <h4 className="text-sm font-semibold text-cyan-700 mb-2">Chat Settings</h4>
          <label className="flex items-center space-x-2 cursor-pointer">
            <input
              type="checkbox"
              checked={chatSettings.autoPlayTTS}
              onChange={toggleAutoPlayTTS}
              className="form-checkbox h-4 w-4 text-cyan-600 border-gray-300 rounded focus:ring-cyan-500"
            />
            <span className="text-sm text-gray-700">Auto-play AI responses (TTS)</span>
            {chatSettings.autoPlayTTS ? <Volume2Icon className="w-4 h-4 text-cyan-600"/> : <SquareIcon className="w-4 h-4 text-gray-400"/>}
          </label>
          <p className="text-xs text-gray-500 mt-1">Enables text-to-speech for assistant's messages.</p>
        </div>
      )}

      <div className="flex flex-col h-full">
        <ChatWindow 
            messages={messages} 
            isLoading={isLoading && !isSummarizingNarrative} // Only show main typing indicator if not summarizing
            personaName={ASSISTANT_PERSONA.name}
            personaAvatar={ASSISTANT_PERSONA.avatar}
        />
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading || isSummarizingNarrative} />
        {chatError && <p className="text-xs text-red-500 p-2 text-center">{chatError}</p>}
        {!isInitialized && !isLoading && !chatError && (
            <div className="p-4 text-center text-gray-500">Initializing assistant...</div>
        )}
      </div>
    </FlowCard>
  );
};

export default ChatAssistantContainer;
