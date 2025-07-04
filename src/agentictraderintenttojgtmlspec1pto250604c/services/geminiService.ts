
import { GoogleGenAI, GenerateContentResponse } from "@google/genai";
import { JGTMLSpec } from '../types';
import { GEMINI_MODEL_NAME } from '../constants';

const API_KEY = process.env.API_KEY;

// Initialize GoogleGenAI instance.
// The API key's availability is handled externally as per guidelines.
// The translateNarrativeToSpec function will throw an error if API_KEY is not set.
const ai = new GoogleGenAI({ apiKey: API_KEY }); 

function constructPrompt(traderNarrative: string): string {
  return `
You are an expert trading assistant. Your task is to translate a trader's market analysis narrative into a structured JSON format representing a '.jgtml-spec'.

The JSON output MUST strictly follow this TypeScript interface:
interface JGTMLSignalComponent {
  [key: string]: string; // e.g., { "fractal_analysis": "jgtpy.fractal_detection" }
}
interface JGTMLSignal {
  name: string; // A concise name for the signal (e.g., "wave5_breakout", "alligator_pullback_entry").
  description: string; // Detailed description of the signal, incorporating trader's reasoning, price levels, indicator states.
  jgtml_components: JGTMLSignalComponent[]; // An array of objects. Each object has ONE key representing the JGTML component category and its value as the specific component or state.
  alligator_context?: string; // Optional. Specify "Regular", "Big", or "Tide" if relevant for multi-timeframe alligator analysis.
}
interface JGTMLSpec {
  strategy_intent: string; // A concise summary of the trader's overall goal.
  instruments: string[]; // An array of trading instruments (e.g., "EUR/USD", "BTC/USD").
  timeframes: string[]; // An array of timeframes mentioned (e.g., "H1", "H4", "D1").
  signals: JGTMLSignal[];
}

Trader's Narrative:
---
${traderNarrative}
---

Based on the narrative, generate ONLY the JSON object adhering to the schema described above. Do not include any other text, explanations, or markdown formatting like \`\`\`json ... \`\`\`.
Ensure all string values in the JSON are properly escaped.
If the narrative mentions specific JGTML components like 'TideAlligatorAnalysis.mouth_opening', 'jgtpy.fractal_detection', 'jgtpy.ao_acceleration', use them.
Map general indicator mentions to appropriate jgtml_components keys and values. For example:
- "Alligator is opening" -> \`{"alligator_state": "AlligatorAnalysis.mouth_opening"}\`
- "AO shows strong momentum" -> \`{"momentum": "jgtpy.ao_acceleration"}\`
- "breakout above 1.0800" -> \`{"price_level_breakout": "1.0800_above"}\`
- "completed Wave 3" -> \`{"wave_count": "manual_wave_3_complete"}\`
If the trader references different Alligator types (Regular, Big, Tide), populate the \`alligator_context\` field in the relevant signal.
`;
}

export const translateNarrativeToSpec = async (narrative: string): Promise<JGTMLSpec> => {
  if (!API_KEY) {
    // This check ensures that we don't proceed if the API key is not configured.
    console.error("API_KEY environment variable not set.");
    throw new Error("Gemini API Key is not configured. Please set the API_KEY environment variable.");
  }

  const fullPrompt = constructPrompt(narrative);

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
    // Check for common API errors, e.g., quota issues, model not found, etc.
    // The GoogleGenAI library might throw specific error types or include details in error.message or error.details
    if (error instanceof Error) {
        // Basic check for permission denied or authentication issues that might not explicitly say "API_KEY_INVALID"
        if (error.message.toLowerCase().includes("permission denied") || error.message.toLowerCase().includes("authentication failed")) {
            throw new Error("Gemini API request failed due to authentication or permission issues. Please check your API key and project setup.");
        }
         // You might want to check for specific error codes or messages from the Gemini API
        if (error.message.includes("RESOURCE_EXHAUSTED") || (error as any)?.status === 429) {
            throw new Error("Gemini API quota exceeded. Please check your usage limits or try again later.");
        }
    }
    throw new Error(`Error generating spec from LLM: ${(error as Error).message}`);
  }
};
