
import { GoogleGenAI, GenerateContentResponse, Chat, Content, Part } from "@google/genai";
import { GEMINI_MODEL_NAME } from '../constants';
import { ChatMessageData, ChatSender, ChatPersona } from '../types';

const MIAGEM_API_KEY = process.env.MIAGEM_API_KEY;
const LEGACY_API_KEY = process.env.API_KEY; // Old key
const EFFECTIVE_API_KEY = MIAGEM_API_KEY || LEGACY_API_KEY;

const API_KEY_STATUS = ((): { configured: boolean; message: string; usingLegacyKey: boolean } => {
  if (MIAGEM_API_KEY) {
    return { configured: true, message: "MIAGEM_API_KEY configured.", usingLegacyKey: false };
  }
  if (LEGACY_API_KEY) {
    return { 
      configured: true, 
      message: "Using legacy API_KEY. Please update to MIAGEM_API_KEY for future compatibility.", 
      usingLegacyKey: true 
    };
  }
  return { 
    configured: false, 
    message: "Gemini API Key not configured. Please set MIAGEM_API_KEY (recommended) or API_KEY (legacy) environment variable.",
    usingLegacyKey: false
  };
})();

export const getApiKeyStatus = () => API_KEY_STATUS;

class ChatGeminiService {
  private ai: GoogleGenAI | null = null;
  private chat: Chat | null = null;
  private currentPersona: ChatPersona | null = null;
  private currentModel: string = GEMINI_MODEL_NAME; // Default model

  constructor() {
    // Constructor remains light, AI client initialized on demand or during initializeChat
  }

  private _getInitializedAI(): GoogleGenAI {
    if (!this.ai) {
      if (!API_KEY_STATUS.configured || !EFFECTIVE_API_KEY) {
        console.error("ChatGeminiService: Attempted to initialize AI without a configured API key.");
        throw new Error(API_KEY_STATUS.message);
      }
      this.ai = new GoogleGenAI({ apiKey: EFFECTIVE_API_KEY });
    }
    return this.ai;
  }

  private formatAppMessagesToGeminiHistory(messages: ChatMessageData[]): Content[] {
    return messages
      .filter(msg => msg.sender === ChatSender.User || (msg.sender === ChatSender.AI && !msg.isError))
      .map(appMsg => {
        const parts: Part[] = [];
        if (appMsg.text) {
          parts.push({ text: appMsg.text });
        }
        // Example for image (if full multimodal history is needed):
        if (appMsg.base64ImageData && appMsg.imageMimeType) {
           parts.push({ inlineData: { data: appMsg.base64ImageData, mimeType: appMsg.imageMimeType } });
        }
        // Example for audio (if full multimodal history is needed):
        if (appMsg.audioDataUrl && appMsg.audioMimeType && appMsg.audioDataUrl.startsWith('data:')) {
            const base64AudioData = appMsg.audioDataUrl.split(',')[1];
            if (base64AudioData) {
                 parts.push({ inlineData: { data: base64AudioData, mimeType: appMsg.audioMimeType } });
            }
        }
        return {
          role: appMsg.sender === ChatSender.User ? 'user' : 'model',
          parts: parts.length > 0 ? parts : [{text: ''}], 
        };
      });
  }

  public async initializeChat(persona: ChatPersona, history: ChatMessageData[] = []): Promise<void> {
    const ai = this._getInitializedAI(); // Ensures AI is initialized and throws if key is missing
    this.currentPersona = persona;
    this.currentModel = GEMINI_MODEL_NAME; // Or allow model to be passed in
    
    const geminiHistory = this.formatAppMessagesToGeminiHistory(history);

    this.chat = ai.chats.create({
      model: this.currentModel,
      config: {
        systemInstruction: this.currentPersona.systemInstruction,
      },
      history: geminiHistory,
    });
  }
  
  public async sendMessageStream(
    parts: Part[], 
    onChunk: (chunkText: string) => void,
    onError: (error: Error, isDefinitive: boolean) => void,
    onComplete: () => void
  ): Promise<void> {
    if (!API_KEY_STATUS.configured) {
      onError(new Error(API_KEY_STATUS.message), true);
      onComplete();
      return;
    }
    
    // Ensure AI is initialized (it would have thrown in initializeChat if key was bad, but good for direct calls)
    try {
        this._getInitializedAI();
    } catch (e) {
        onError(e as Error, true);
        onComplete();
        return;
    }

    if (!this.chat) {
      onError(new Error("Chat is not initialized. Please call initializeChat first."), true);
      onComplete();
      return;
    }

    if (parts.length === 0) {
        onError(new Error("Cannot send an empty message."), false); // Not a definitive API error
        onComplete();
        return;
    }

    try {
      const result = await this.chat.sendMessageStream({ message: parts });
      for await (const chunk of result) {
        if (chunk.text) { 
            onChunk(chunk.text);
        }
      }
      onComplete();
    } catch (e) {
      console.error("Error sending message to Gemini:", e);
      const error = e as Error;
      let isDefinitive = false;
      let UIMessage = `Sorry, an unexpected error occurred: ${error.message}. Please try again.`;

      if (error.message.includes("API_KEY_INVALID") || error.message.includes("API key not valid") || error.message.toLowerCase().includes("permission denied")) {
        isDefinitive = true;
        UIMessage = "The configured Gemini API Key is invalid, missing required permissions, or has expired. Please check your API key settings.";
      } else if (error.message.includes("RESOURCE_EXHAUSTED") || (e as any)?.status === 429) {
         isDefinitive = true; 
         UIMessage = "Gemini API quota exceeded. Please check your usage limits or try again later.";
      } else if (error.message.toLowerCase().includes("model not found")) {
         isDefinitive = true;
         UIMessage = `The AI model ('${this.currentModel}') could not be found. Please check the model name.`;
      } else if (error.message.toLowerCase().includes("request payload size exceeds the limit")) {
         UIMessage = "The image or audio file you sent might be too large. Please try a smaller file.";
         isDefinitive = false; // User can try again with smaller file
      }
      onError(new Error(UIMessage), isDefinitive);
      onComplete(); // Ensure loading state is cleared
    }
  }

  public isInitialized(): boolean {
    return !!this.chat;
  }
  
  public getCurrentPersona(): ChatPersona | null {
    return this.currentPersona;
  }
}

export default new ChatGeminiService();
