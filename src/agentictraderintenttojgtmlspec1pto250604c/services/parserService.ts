import { JGTMLSpec, ParsedSpecOutput } from '../types';

// Simulate an asynchronous parsing operation
export const simulateIntentSpecParsing = (spec: JGTMLSpec): Promise<ParsedSpecOutput> => {
  return new Promise((resolve, reject) => {
    // Simulate a delay for parsing
    setTimeout(() => {
      if (!spec || !spec.signals || !spec.strategy_intent) {
        // Simulate a basic validation error
        reject(new Error("Invalid JGTML spec provided for parsing. Core fields missing."));
        return;
      }
      
      // Simulate a successful parsing outcome
      const parsedOutput: ParsedSpecOutput = {
        status: 'Success',
        message: 'JGTML spec successfully received and validated (simulation). Ready for signal processing.',
        signalPackagePreview: {
          strategy: spec.strategy_intent,
          instruments: spec.instruments,
          timeframes: spec.timeframes,
          signalCount: spec.signals.length,
          firstSignalName: spec.signals.length > 0 ? spec.signals[0].name : 'N/A',
          // You could add more derived or structured data here
          // For example, a count of unique JGTML components:
          uniqueComponents: [
            ...new Set(
              spec.signals.flatMap(s => 
                s.jgtml_components.flatMap(c => Object.keys(c))
              )
            )
          ].join(', ') || 'None'
        }
      };
      resolve(parsedOutput);
    }, 1000); // 1 second delay to simulate work
  });
};