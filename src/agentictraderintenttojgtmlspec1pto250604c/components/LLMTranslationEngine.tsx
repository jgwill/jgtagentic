import React from 'react';
import { JGTMLSpec } from '../types';
import FlowCard from './FlowCard';
import { BrainIcon, LoaderIcon } from './icons/LucideIcons';

interface LLMTranslationEngineProps {
  spec: JGTMLSpec | null;
  isLoading: boolean;
  error: string | null; // Specifically for LLM translation errors
}

const LLMTranslationEngine: React.FC<LLMTranslationEngineProps> = ({ spec, isLoading, error }) => {
  return (
    <FlowCard
      title="🧠 LLM Translation Engine"
      description="Parses narrative → .jgtml-spec (JSON format) using pattern rules and LLM understanding."
      bgColorClass="bg-blue-50"
      icon={<BrainIcon className="w-6 h-6 text-blue-600" />}
    >
      {isLoading && (
        <div className="flex items-center justify-center p-6 text-blue-700">
          <LoaderIcon className="w-8 h-8 mr-3" />
          <span>Translating narrative to spec...</span>
        </div>
      )}
      {error && !isLoading && ( // Display error only if not loading
        <div className="p-4 bg-red-100 border border-red-300 text-red-700 rounded-md">
          <p className="font-semibold">LLM Translation Error:</p>
          <p className="text-sm break-all">{error}</p>
        </div>
      )}
      {spec && !isLoading && !error && ( // Display spec only if no error and not loading
        <div>
          <h3 className="text-md font-semibold text-gray-700 mb-2">Generated JGTML Spec (JSON):</h3>
          <pre className="bg-white p-4 rounded-md shadow-sm text-xs overflow-x-auto max-h-96 border border-blue-200">
            {JSON.stringify(spec, null, 2)}
          </pre>
        </div>
      )}
      {!spec && !isLoading && !error && ( // Placeholder if no spec, not loading, and no error
         <p className="text-sm text-gray-500 italic p-4 text-center">Submit a trader narrative to generate the JGTML spec.</p>
      )}
    </FlowCard>
  );
};

export default LLMTranslationEngine;