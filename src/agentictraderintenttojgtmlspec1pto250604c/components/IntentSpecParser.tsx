import React from 'react';
import { ParsedSpecOutput, JGTMLSpec } from '../types';
import FlowCard from './FlowCard';
import { FileTextIcon, LoaderIcon } from './icons/LucideIcons';

interface IntentSpecParserProps {
  specInput: JGTMLSpec | null; // The spec to be "parsed"
  parsedOutput: ParsedSpecOutput | null;
  isLoading: boolean; // This could be for a simulated parsing delay
  error: string | null;
}

const IntentSpecParser: React.FC<IntentSpecParserProps> = ({ specInput, parsedOutput, isLoading, error }) => {
  return (
    <FlowCard
      title="📜 IntentSpecParser"
      description="Reads .jgtml-spec → constructs signal package (simulated)."
      bgColorClass="bg-green-50"
      icon={<FileTextIcon className="w-6 h-6 text-green-600" />}
    >
      {isLoading && specInput && (
        <div className="flex items-center justify-center p-6 text-green-700">
          <LoaderIcon className="w-8 h-8 mr-3" />
          <span>Simulating spec parsing...</span>
        </div>
      )}
      {error && !isLoading && (
         <div className="p-4 bg-red-100 border border-red-300 text-red-700 rounded-md">
          <p className="font-semibold">Parsing Error:</p>
          <p className="text-sm">{error}</p>
        </div>
      )}
      {parsedOutput && !isLoading && !error && (
        <div className="space-y-3">
          <div>
            <h4 className="text-md font-semibold text-gray-700">Parsing Status:</h4>
            <p className={`text-sm px-3 py-1.5 rounded-md inline-block ${parsedOutput.status === 'Success' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
              {parsedOutput.status}
            </p>
          </div>
          <div>
            <h4 className="text-md font-semibold text-gray-700">Details:</h4>
            <p className="text-sm text-gray-600">{parsedOutput.message}</p>
          </div>
          {parsedOutput.signalPackagePreview && (
            <div>
              <h4 className="text-md font-semibold text-gray-700">Simulated Signal Package Preview:</h4>
              <pre className="bg-white p-3 rounded-md shadow-sm text-xs overflow-x-auto max-h-60 border border-green-200">
                {JSON.stringify(parsedOutput.signalPackagePreview, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
      {!specInput && !isLoading && !error && (
         <p className="text-sm text-gray-500 italic p-4 text-center">Waiting for a JGTML spec to parse...</p>
      )}
    </FlowCard>
  );
};

export default IntentSpecParser;
