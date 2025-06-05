
import React, { useState } from 'react';
import { JGTMLSpec } from '../types';
import FlowCard from './FlowCard';
import { BrainIcon, LoaderIcon, CopyIcon, CheckIcon } from './icons/LucideIcons';

interface LLMTranslationEngineProps {
  spec: JGTMLSpec | null;
  isLoading: boolean;
  error: string | null; // Specifically for LLM translation errors
}

const LLMTranslationEngine: React.FC<LLMTranslationEngineProps> = ({ spec, isLoading, error }) => {
  const [specCopied, setSpecCopied] = useState(false);

  const handleCopySpec = () => {
    if (spec) {
      const specString = JSON.stringify(spec, null, 2);
      navigator.clipboard.writeText(specString).then(() => {
        setSpecCopied(true);
        setTimeout(() => setSpecCopied(false), 2000);
      }).catch(err => {
        console.error('Failed to copy spec: ', err);
        alert('Failed to copy spec to clipboard.');
      });
    }
  };

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
          <div className="flex justify-between items-center mb-2">
            <h3 className="text-md font-semibold text-gray-700">Generated JGTML Spec (JSON):</h3>
            <button
              onClick={handleCopySpec}
              title={specCopied ? "Copied!" : "Copy JGTML Spec"}
              className="p-1.5 rounded-md hover:bg-blue-100 text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:opacity-50"
              aria-label={specCopied ? "JGTML Spec copied to clipboard" : "Copy JGTML Spec"}
              disabled={!spec}
            >
              {specCopied ? <CheckIcon className="w-5 h-5 text-green-600" /> : <CopyIcon className="w-5 h-5" />}
            </button>
          </div>
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
