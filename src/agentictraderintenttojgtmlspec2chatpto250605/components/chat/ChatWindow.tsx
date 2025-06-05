import React, { useEffect, useRef } from 'react';
import { ChatMessageData, ChatSender } from '../../types';
import ChatMessage from './ChatMessage';
import { LoaderIcon, BotIcon } from '../icons/LucideIcons'; // Assuming BotIcon is available

interface ChatWindowProps {
  messages: ChatMessageData[];
  isLoading: boolean;
  personaName?: string; // Optional, for loading message
  personaAvatar?: React.ReactNode; // Optional, for loading message
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages, isLoading, personaName, personaAvatar }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const aiAvatar = personaAvatar || <BotIcon className="w-6 h-6 text-teal-600" />;

  return (
    <div className="flex-grow p-4 space-y-2 overflow-y-auto bg-white rounded-t-lg border border-gray-200 h-[400px] max-h-[400px]">
      {messages.map((msg) => (
        <ChatMessage key={msg.id} message={msg} />
      ))}
      {isLoading && (
        <div className="flex flex-row gap-2.5 my-3 items-end">
            <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-teal-500 text-white mt-auto">
                {aiAvatar}
            </div>
            <div className="flex flex-col items-start">
                 <span className="text-xs text-gray-500">{personaName || ChatSender.AI}</span>
                <div className="p-3 rounded-lg shadow-sm bg-teal-50 text-teal-800">
                    <div className="flex items-center space-x-1">
                        <LoaderIcon className="w-4 h-4 text-teal-600" />
                        <span className="text-sm italic">typing...</span>
                    </div>
                </div>
            </div>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatWindow;
