import React, { useState } from 'react';
import { ChatMessageData, ChatSender } from '../../types';
import { BotIcon, UserIcon, CopyIcon, Volume2Icon, SquareIcon, CheckIcon, CircleAlertIcon } from '../icons/LucideIcons';
import useChatSpeechSynthesis from '../../hooks/useChatSpeechSynthesis';
import MarkdownRenderer from './MarkdownRenderer';

interface ChatMessageProps {
  message: ChatMessageData;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const [copied, setCopied] = useState(false);
  const { speak, cancel, isSpeaking, browserSupportsSpeechSynthesis } = useChatSpeechSynthesis();

  const handleCopy = () => {
    navigator.clipboard.writeText(message.text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }).catch(err => console.error('Failed to copy text: ', err));
  };

  const handleToggleTTS = () => {
    if (isSpeaking) {
      cancel();
    } else {
      speak(message.text);
    }
  };
  
  const avatar = message.sender === ChatSender.User 
    ? message.avatar || <UserIcon className="w-6 h-6 text-purple-600" /> 
    : message.avatar || <BotIcon className="w-6 h-6 text-teal-600" />;

  const bubbleBgClass = message.sender === ChatSender.User
    ? 'bg-purple-100 text-purple-800'
    : message.isError ? 'bg-red-100 text-red-700' : 'bg-teal-50 text-teal-800';

  const alignmentClass = message.sender === ChatSender.User ? 'items-end' : 'items-start';
  const messageFlowClass = message.sender === ChatSender.User ? 'flex-row-reverse' : 'flex-row';

  return (
    <div className={`flex ${messageFlowClass} gap-2.5 my-3`}>
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${message.sender === ChatSender.User ? 'bg-purple-500' : 'bg-teal-500'} text-white mt-auto mb-auto`}>
        {avatar}
      </div>
      <div className={`flex flex-col w-full max-w-xs sm:max-w-md md:max-w-lg ${alignmentClass}`}>
        <div className={`flex ${message.sender === ChatSender.User ? 'flex-row-reverse' : ''} items-center space-x-1 ${message.sender === ChatSender.User ? 'space-x-reverse' : ''}`}>
           <span className="text-xs text-gray-500">{message.sender === ChatSender.AI ? (message.avatar && typeof message.avatar !== 'string' && (message.avatar as any).props?.personaName || message.sender) : message.sender}</span>
           <span className="text-xs text-gray-400">{message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
        </div>
        <div className={`relative p-3 rounded-lg shadow-sm ${bubbleBgClass}`}>
          {message.isError && <CircleAlertIcon className="w-5 h-5 inline-block mr-2 mb-0.5 text-red-500" />}
          
          {message.imagePreviewUrl && (
            <div className="my-2">
              <img 
                src={message.imagePreviewUrl} 
                alt={message.fileName || "Attached image"} 
                className="max-w-full h-auto max-h-60 rounded-md border border-gray-300" 
              />
              {message.fileName && <p className="text-xs text-gray-600 mt-1">{message.fileName}</p>}
            </div>
          )}

          {message.audioDataUrl && (
            <div className="my-2">
              <audio controls src={message.audioDataUrl} className="w-full h-10">
                Your browser does not support the audio element.
              </audio>
              {message.fileName && <p className="text-xs text-gray-600 mt-1">{message.fileName}</p>}
            </div>
          )}
          
          {message.text && <MarkdownRenderer content={message.text} />}

          {(message.text || (message.sender === ChatSender.AI && !message.isError && browserSupportsSpeechSynthesis)) && (
            <div className={`absolute -bottom-2 ${message.sender === ChatSender.User ? 'left-2' : 'right-2'} flex space-x-1 opacity-70 hover:opacity-100 transition-opacity`}>
              {message.text && (
                <button
                  onClick={handleCopy}
                  title={copied ? "Copied!" : "Copy text"}
                  className="p-1 rounded-full hover:bg-gray-300/50 focus:outline-none"
                  aria-label={copied ? "Copied text to clipboard" : "Copy message text"}
                >
                  {copied ? <CheckIcon className="w-3 h-3 text-green-600" /> : <CopyIcon className="w-3 h-3 text-gray-500" />}
                </button>
              )}
              {message.sender === ChatSender.AI && !message.isError && message.text && browserSupportsSpeechSynthesis && (
                <button
                  onClick={handleToggleTTS}
                  title={isSpeaking ? "Stop speaking" : "Speak text"}
                  className="p-1 rounded-full hover:bg-gray-300/50 focus:outline-none"
                  aria-label={isSpeaking ? "Stop text-to-speech" : "Start text-to-speech"}
                >
                  {isSpeaking ? <SquareIcon className="w-3 h-3 text-red-500" /> : <Volume2Icon className="w-3 h-3 text-gray-500" />}
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;