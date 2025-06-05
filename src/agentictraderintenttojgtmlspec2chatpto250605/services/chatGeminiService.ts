import { GoogleGenAI, GenerateContentResponse, Chat, Content, Part } from "@google/genai";
import { GEMINI_MODEL_NAME } from '../constants';
import { ChatMessageData, ChatSender, ChatPersona } from '../types';

const API_KEY = process.env.API_KEY;

class ChatGeminiService {
  private ai: GoogleGenAI | null = null;
  private chat: Chat | null = null;
  private currentPersona: ChatPersona | null = null;
  private currentModel: string = GEMINI_MODEL_NAME; // Default model

  constructor() {
    if (!API_KEY) {
      console.error("API_KEY environment variable not set for ChatGeminiService.");
      // Throwing an error here might be too disruptive for app load.
      // Instead, methods that use `ai` will check and throw.
      return;
    }
    this.ai = new GoogleGenAI({ apiKey: API_KEY });
  }

  private formatAppMessagesToGeminiHistory(messages: ChatMessageData[]): Content[] {
    return messages
      .filter(msg => msg.sender === ChatSender.User || (msg.sender === ChatSender.AI && !msg.isError)) // Only user messages and successful AI messages for history
      .map(appMsg => ({
        role: appMsg.sender === ChatSender.User ? 'user' : 'model',
        parts: [{ text: appMsg.text }] as Part[], // Assuming text-only history for now
      }));
  }

  public async initializeChat(persona: ChatPersona, history: ChatMessageData[] = []): Promise<void> {
    if (!this.ai) {
      throw new Error("ChatGeminiService AI not initialized. API_KEY might be missing.");
    }
    this.currentPersona = persona;
    
    const geminiHistory = this.formatAppMessagesToGeminiHistory(history);

    this.chat = this.ai.chats.create({
      model: this.currentModel,
      config: {
        systemInstruction: this.currentPersona.systemInstruction,
        // Add other relevant config like temperature if needed for chat
        // temperature: 0.7, 
      },
      history: geminiHistory,
    });
  }
  
  public async sendMessageStream(
    messageText: string,
    onChunk: (chunkText: string) => void,
    onError: (error: Error, isDefinitive: boolean) => void,
    onComplete: () => void
  ): Promise<void> {
    if (!this.chat) {
      onError(new Error("Chat is not initialized. Please call initializeChat first."), true);
      return;
    }
    if (!API_KEY) {
      onError(new Error("Gemini API Key is not configured."), true);
      return;
    }

    try {
      const result = await this.chat.sendMessageStream({ message: messageText });
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
      if (error.message.includes("API_KEY_INVALID") || error.message.includes("API key not valid")) {
        isDefinitive = true;
        onError(new Error("The Gemini API Key is invalid or missing."), isDefinitive);
      } else if (error.message.includes("RESOURCE_EXHAUSTED") || (e as any)?.status === 429) {
         isDefinitive = true; // Quota issues are often persistent for a while
         onError(new Error("Gemini API quota exceeded. Please check your usage limits or try again later."), isDefinitive);
      }
      else {
        onError(error, isDefinitive);
      }
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
