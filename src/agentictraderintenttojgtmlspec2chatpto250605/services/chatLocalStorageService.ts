
import { ChatMessageData, ChatSender, ChatSettings } from '../types';

const CHAT_MESSAGES_KEY = 'jgtmlTraderChatMessages';
const CHAT_SETTINGS_KEY = 'jgtmlTraderChatSettings';

type StoredChatMessage = {
  id: string;
  text: string;
  sender: ChatSender;
  timestamp: string;  // Date is stored as ISO string
  avatar?: string;     // ReactNode avatars are not stored, only string (URL) avatars
  isError?: boolean;

  // Multimodal fields
  imagePreviewUrl?: string; // Could be blob URL, might not persist well if not converted
  base64ImageData?: string;
  imageMimeType?: string;
  fileName?: string;

  audioDataUrl?: string; // Could be blob URL
  audioMimeType?: string;
  // For simplicity, audio blob itself isn't stored directly in JSON.
  // We'll rely on audioDataUrl (which might be a base64 data URI if generated that way, or blob URL)
  // If audioDataUrl is a blob URL, it won't be valid across sessions.
  // If we send base64 for audio, it should be stored here.
  // For now, let's assume audioDataUrl can be a base64 data URI for persistence.
};

export const saveChatMessages = (messages: ChatMessageData[]): void => {
  try {
    const serializableMessages: StoredChatMessage[] = messages.map(msg => {
      const storedMsg: StoredChatMessage = {
        id: msg.id,
        text: msg.text,
        sender: msg.sender,
        timestamp: msg.timestamp.toISOString(),
        isError: msg.isError,
        fileName: msg.fileName,
        base64ImageData: msg.base64ImageData,
        imageMimeType: msg.imageMimeType,
        audioDataUrl: msg.audioDataUrl, // Assumes this might be a base64 data URI for audio
        audioMimeType: msg.audioMimeType,
      };

      if (typeof msg.avatar === 'string') {
        storedMsg.avatar = msg.avatar;
      }
      // imagePreviewUrl is often a blob URL, which is temporary.
      // If base64ImageData exists, imagePreviewUrl can be reconstructed on load.
      // So, we might not need to store imagePreviewUrl if base64 is stored.
      // For simplicity, let's store it if it exists, but be aware of blob URL limitations.
      if (msg.imagePreviewUrl && !msg.base64ImageData) { 
          // Only store preview URL if there's no base64 data, assuming it might be an external URL
          storedMsg.imagePreviewUrl = msg.imagePreviewUrl;
      }


      return storedMsg;
    });
    localStorage.setItem(CHAT_MESSAGES_KEY, JSON.stringify(serializableMessages));
  } catch (error) {
    console.error('Error saving chat messages to local storage:', error);
  }
};

export const loadChatMessages = (): ChatMessageData[] => {
  try {
    const storedMessagesJson = localStorage.getItem(CHAT_MESSAGES_KEY);
    if (storedMessagesJson) {
      const parsedStoredMessages: StoredChatMessage[] = JSON.parse(storedMessagesJson);
      
      return parsedStoredMessages.map((storedMsg): ChatMessageData => {
        let imagePreviewUrl = storedMsg.imagePreviewUrl;
        if (storedMsg.base64ImageData && storedMsg.imageMimeType) {
          imagePreviewUrl = `data:${storedMsg.imageMimeType};base64,${storedMsg.base64ImageData}`;
        }
        
        const chatMessage: ChatMessageData = {
          id: storedMsg.id,
          text: storedMsg.text,
          sender: storedMsg.sender,
          timestamp: new Date(storedMsg.timestamp),
          avatar: storedMsg.avatar, 
          isError: storedMsg.isError,
          fileName: storedMsg.fileName,
          base64ImageData: storedMsg.base64ImageData,
          imageMimeType: storedMsg.imageMimeType,
          imagePreviewUrl: imagePreviewUrl, // Reconstructed if base64 was available
          audioDataUrl: storedMsg.audioDataUrl, // Assumes this was stored as base64 data URI if persistent
          audioMimeType: storedMsg.audioMimeType,
        };
        return chatMessage;
      });
    }
  } catch (error) {
    console.error('Error loading chat messages from local storage:', error);
  }
  return [];
};

export const saveChatSettings = (settings: ChatSettings): void => {
  try {
    localStorage.setItem(CHAT_SETTINGS_KEY, JSON.stringify(settings));
  } catch (error) {
    console.error('Error saving chat settings to local storage:', error);
  }
};

export const loadChatSettings = (): ChatSettings => {
  try {
    const storedSettings = localStorage.getItem(CHAT_SETTINGS_KEY);
    if (storedSettings) {
      const parsedSettings = JSON.parse(storedSettings) as ChatSettings;
      return {
        autoPlayTTS: typeof parsedSettings.autoPlayTTS === 'boolean' ? parsedSettings.autoPlayTTS : false,
      };
    }
  } catch (error) {
    console.error('Error loading chat settings from local storage:', error);
  }
  return {
    autoPlayTTS: false,
  };
};