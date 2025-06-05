

import { GoogleGenAI, GenerateContentResponse } from "@google/genai";
import { JGTMLSpec, ChatMessageData, ChatSender } from '../types';
import { GEMINI_MODEL_NAME } from '../constants';
import { SUMMARIZE_TRADING_NARRATIVE_CHAT_PROMPT, TRANSLATE_NARRATIVE_TO_JGTML_PROMPT_TEMPLATE } from './promptTemplates';

const API_KEY = process.env.API_KEY;

// Initialize GoogleGenAI instance.
// The API key's availability is handled externally as per guidelines.
const ai = new GoogleGenAI({ apiKey: API_KEY }); 

export const translateNarrativeToSpec = async (narrative: string): Promise<JGTMLSpec> => {
  if (!API_KEY) {
    console.error("API_KEY environment variable not set.");
    throw new Error("Gemini API Key is not configured. Please set the API_KEY environment variable.");
  }

  const fullPrompt = TRANSLATE_NARRATIVE_TO_JGTML_PROMPT_TEMPLATE.replace('{traderNarrative}', narrative);

  try {
    const response: GenerateContentResponse = await ai.models.generateContent({
      model: GEMINI_MODEL_NAME,
      contents: fullPrompt,
      config: {
        responseMimeType: "application/json",
        temperature: 0.2, // Lower temperature for more deterministic JSON output
      },
    });

    let jsonStr = response.text.trim();
    
    const fenceRegex = /^```(?:json)?\s*\n?(.*?)\n?\s*```$/s;
    const match = jsonStr.match(fenceRegex);
    if (match && match[1]) {
      jsonStr = match[1].trim();
    }

    try {
      const parsedData = JSON.parse(jsonStr) as JGTMLSpec;
      if (!parsedData.strategy_intent || !parsedData.instruments || !parsedData.timeframes || !parsedData.signals) {
        console.error("Parsed JSON is missing required JGTMLSpec fields. Raw LLM text:", response.text, "Attempted JSON string:", jsonStr);
        throw new Error("Parsed JSON is missing required JGTMLSpec fields.");
      }
      return parsedData;
    } catch (e) {
      console.error("Failed to parse JSON response from LLM:", e);
      console.error("Raw response text from LLM:", response.text);
      console.error("Cleaned JSON string for parsing:", jsonStr);
      throw new Error(`Failed to parse JGTMLSpec from LLM response. Invalid JSON: ${(e as Error).message}`);
    }
  } catch (error) {
    console.error("Error calling Gemini API:", error);
    if (error instanceof Error && error.message.includes("API_KEY_INVALID")) {
         throw new Error("The provided Gemini API Key is invalid or has expired.");
    }
    if (error instanceof Error) {
        if (error.message.toLowerCase().includes("permission denied") || error.message.toLowerCase().includes("authentication failed")) {
            throw new Error("Gemini API request failed due to authentication or permission issues. Please check your API key and project setup.");
        }
        if (error.message.includes("RESOURCE_EXHAUSTED") || (error as any)?.status === 429) {
            throw new Error("Gemini API quota exceeded. Please check your usage limits or try again later.");
        }
    }
    throw new Error(`Error generating spec from LLM: ${(error as Error).message}`);
  }
};

export const summarizeChatHistoryForNarrative = async (messages: ChatMessageData[]): Promise<string> => {
  if (!API_KEY) {
    console.error("API_KEY environment variable not set.");
    throw new Error("Gemini API Key is not configured. Please set the API_KEY environment variable.");
  }

  // Format chat history into a single string
  const chatHistoryString = messages
    .filter(msg => msg.sender === ChatSender.User || (msg.sender === ChatSender.AI && !msg.isError)) // Include user messages and non-error AI responses
    .map(msg => `${msg.sender}: ${msg.text}`)
    .join('\n');

  if (!chatHistoryString.trim()) {
    return "No relevant chat history to summarize.";
  }
  
  const prompt = SUMMARIZE_TRADING_NARRATIVE_CHAT_PROMPT.replace('{chatHistoryString}', chatHistoryString);

  try {
    const response: GenerateContentResponse = await ai.models.generateContent({
      model: GEMINI_MODEL_NAME,
      contents: prompt,
      config: {
        // Temperature can be higher for more creative summarization, but still controlled
        temperature: 0.5, 
      },
    });

    // The prompt asks for plain text, so no JSON parsing or fence removal needed here,
    // but we should still trim whitespace.
    return response.text.trim();

  } catch (error) {
    console.error("Error calling Gemini API for chat summarization:", error);
     if (error instanceof Error && error.message.includes("API_KEY_INVALID")) {
         throw new Error("The provided Gemini API Key is invalid or has expired.");
    }
    if (error instanceof Error) {
        if (error.message.toLowerCase().includes("permission denied") || error.message.toLowerCase().includes("authentication failed")) {
            throw new Error("Gemini API request failed due to authentication or permission issues for summarization.");
        }
        if (error.message.includes("RESOURCE_EXHAUSTED") || (error as any)?.status === 429) {
            throw new Error("Gemini API quota exceeded for summarization. Please check your usage limits or try again later.");
        }
    }
    throw new Error(`Error summarizing chat history: ${(error as Error).message}`);
  }
};
