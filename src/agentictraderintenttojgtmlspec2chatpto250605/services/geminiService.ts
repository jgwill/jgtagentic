
import { GoogleGenAI, GenerateContentResponse } from "@google/genai";
import { JGTMLSpec, ChatMessageData, ChatSender } from '../types';
import { GEMINI_MODEL_NAME } from '../constants';
import { SUMMARIZE_TRADING_NARRATIVE_CHAT_PROMPT, TRANSLATE_NARRATIVE_TO_JGTML_PROMPT_TEMPLATE } from './promptTemplates';

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

let ai: GoogleGenAI | null = null;
if (API_KEY_STATUS.configured && EFFECTIVE_API_KEY) {
  ai = new GoogleGenAI({ apiKey: EFFECTIVE_API_KEY });
} else {
  console.warn(`geminiService: ${API_KEY_STATUS.message}`);
}

const checkApiKeyAndThrow = () => {
  if (!API_KEY_STATUS.configured || !ai) {
    throw new Error(API_KEY_STATUS.message + " (geminiService)");
  }
};

const getApiKeyRelatedErrorMessage = (error: Error): string => {
    let keyDisplayName = "API Key";
    if (API_KEY_STATUS.usingLegacyKey) {
        keyDisplayName = "legacy API_KEY";
    } else if (MIAGEM_API_KEY) {
        keyDisplayName = "MIAGEM_API_KEY";
    }

    if (error.message.includes("API_KEY_INVALID") || error.message.toLowerCase().includes("api key not valid")) {
        return `The provided Gemini ${keyDisplayName} is invalid or has expired.`;
    }
    if (error.message.toLowerCase().includes("permission denied") || error.message.toLowerCase().includes("authentication failed")) {
        return `Gemini API request failed due to authentication or permission issues with ${keyDisplayName}. Please check your API key and project setup.`;
    }
    if (error.message.includes("RESOURCE_EXHAUSTED") || (error as any)?.status === 429) {
        return `Gemini API quota exceeded. Please check your usage limits or try again later. (Using ${keyDisplayName})`;
    }
    return `Error from Gemini API (using ${keyDisplayName}): ${error.message}`;
};


export const translateNarrativeToSpec = async (narrative: string): Promise<JGTMLSpec> => {
  checkApiKeyAndThrow(); // Will throw if API key is not configured

  const fullPrompt = TRANSLATE_NARRATIVE_TO_JGTML_PROMPT_TEMPLATE.replace('{traderNarrative}', narrative);

  try {
    // ai is guaranteed to be non-null here due to checkApiKeyAndThrow()
    const response: GenerateContentResponse = await ai!.models.generateContent({
      model: GEMINI_MODEL_NAME,
      contents: fullPrompt,
      config: {
        responseMimeType: "application/json",
        temperature: 0.2, 
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
    console.error("Error calling Gemini API for spec translation:", error);
    throw new Error(getApiKeyRelatedErrorMessage(error as Error));
  }
};

export const summarizeChatHistoryForNarrative = async (messages: ChatMessageData[]): Promise<string> => {
  checkApiKeyAndThrow(); // Will throw if API key is not configured

  const chatHistoryString = messages
    .filter(msg => msg.sender === ChatSender.User || (msg.sender === ChatSender.AI && !msg.isError))
    .map(msg => `${msg.sender}: ${msg.text}`)
    .join('\n');

  if (!chatHistoryString.trim()) {
    return "No relevant chat history to summarize.";
  }
  
  const prompt = SUMMARIZE_TRADING_NARRATIVE_CHAT_PROMPT.replace('{chatHistoryString}', chatHistoryString);

  try {
    // ai is guaranteed to be non-null here
    const response: GenerateContentResponse = await ai!.models.generateContent({
      model: GEMINI_MODEL_NAME,
      contents: prompt,
      config: {
        temperature: 0.5, 
      },
    });

    return response.text.trim();

  } catch (error) {
    console.error("Error calling Gemini API for chat summarization:", error);
    throw new Error(getApiKeyRelatedErrorMessage(error as Error));
  }
};
