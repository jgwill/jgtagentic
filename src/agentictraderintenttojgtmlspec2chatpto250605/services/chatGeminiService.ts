

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
      return;
    }
    this.ai = new GoogleGenAI({ apiKey: API_KEY });
  }

  private formatAppMessagesToGeminiHistory(messages: ChatMessageData[]): Content[] {
    return messages
      .filter(msg => msg.sender === ChatSender.User || (msg.sender === ChatSender.AI && !msg.isError))
      .map(appMsg => {
        const parts: Part[] = [];
        if (appMsg.text) {
          parts.push({ text: appMsg.text });
        }
        // For simplicity in history, we're still focusing on text.
        // If full multimodal history context is needed, image/audio parts would be added here.
        // Example for image:
        // if (appMsg.base64ImageData && appMsg.imageMimeType) {
        //   parts.push({ inlineData: { data: appMsg.base64ImageData, mimeType: appMsg.imageMimeType } });
        // }
        return {
          role: appMsg.sender === ChatSender.User ? 'user' : 'model',
          parts: parts.length > 0 ? parts : [{text: ''}], // Ensure parts is never empty
        };
      });
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
    if (!this.chat) {
      onError(new Error("Chat is not initialized. Please call initializeChat first."), true);
      return;
    }
    if (!API_KEY) {
      onError(new Error("Gemini API Key is not configured."), true);
      return;
    }

    if (parts.length === 0) {
        onError(new Error("Cannot send an empty message."), false);
        return;
    }

    try {
      // Corrected: `message` property now holds the `parts` array.
      const result = await this.chat.sendMessageStream({ message: { parts } });
      for await (const chunk of result) {
        // text can be undefined in a chunk, e.g. if it's a non-text part or metadata
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
         isDefinitive = true; 
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