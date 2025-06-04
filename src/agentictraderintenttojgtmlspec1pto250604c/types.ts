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

// Enum for FlowStep can be added if needed for more complex state management,
// but for this app, conditional rendering based on data presence might be simpler.
