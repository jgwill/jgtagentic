export interface JGTMLSignalComponent {
  [key: string]: string; // e.g., { "fractal_analysis": "jgtpy.fractal_detection" }
}

export interface JGTMLSignal {
  name: string;
  description: string;
  jgtml_components: JGTMLSignalComponent[];
  alligator_context?: string;
}

export interface JGTMLSpec {
  strategy_intent: string;
  instruments: string[];
  timeframes: string[];
  signals: JGTMLSignal[];
}

export interface TraderInput {
  narrative: string;
}

export interface ParsedSpecOutput {
  status: string;
  message: string;
  signalPackagePreview?: Record<string, any>; 
}

// Chat Assistant Types
export enum ChatSender {
  User = 'User',
  AI = 'AI',
  System = 'System',
}

export interface ChatMessageData {
  id: string;
  text: string;
  sender: ChatSender;
  timestamp: Date;
  avatar?: React.ReactNode | string; 
  isError?: boolean;
  
  // Multimodal content fields
  imagePreviewUrl?: string; // For displaying a preview (can be a blob URL)
  base64ImageData?: string; // Full image data for storage/sending
  imageMimeType?: string;
  fileName?: string; // For uploaded files

  audioDataUrl?: string; // For playing audio (can be a blob URL)
  audioMimeType?: string;
  // audioBlob?: Blob; // If Blob needs to be handled directly, not typically for JSON state
}

export interface ChatSettings {
  autoPlayTTS: boolean;
  // Add other chat-specific settings if needed
}

export interface ChatPersona {
  id: string;
  name: string;
  avatar: React.ReactNode;
  systemInstruction: string;
}