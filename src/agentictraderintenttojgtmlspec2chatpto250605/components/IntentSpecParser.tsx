
import React, { useState } from 'react';
import { ParsedSpecOutput, JGTMLSpec } from '../types';
import FlowCard from './FlowCard';
import { FileTextIcon, LoaderIcon, CopyIcon, CheckIcon } from './icons/LucideIcons';

interface IntentSpecParserProps {
  specInput: JGTMLSpec | null; 
  parsedOutput: ParsedSpecOutput | null;
  isLoading: boolean; // True when this specific component's operation is loading
  error: string | null; // Specifically for parsing errors
}

const IntentSpecParser: React.FC<IntentSpecParserProps> = ({ specInput, parsedOutput, isLoading, error }) => {
  const [previewCopied, setPreviewCopied] = useState(false);

  const handleCopyPreview = () => {
    if (parsedOutput?.signalPackagePreview) {
      const previewString = JSON.stringify(parsedOutput.signalPackagePreview, null, 2);
      navigator.clipboard.writeText(previewString).then(() => {
        setPreviewCopied(true);
        setTimeout(() => setPreviewCopied(false), 2000);
      }).catch(err => {
        console.error('Failed to copy preview: ', err);
        alert('Failed to copy preview to clipboard.');
      });
    }
  };
  
  return (
    <FlowCard
      title="📜 IntentSpecParser"
      description="Reads .jgtml-spec → constructs signal package (simulated)."
      bgColorClass="bg-green-50"
      icon={<FileTextIcon className="w-6 h-6 text-green-600" />}
    >
      {isLoading && specInput && ( // Show loading only if there's a spec input and it's its turn to load
        <div className="flex items-center justify-center p-6 text-green-700">
          <LoaderIcon className="w-8 h-8 mr-3" />
          <span>Simulating spec parsing...</span>
        </div>
      )}
      {error && !isLoading && ( // Display error only if not loading
         <div className="p-4 bg-red-100 border border-red-300 text-red-700 rounded-md">
          <p className="font-semibold">Parsing Error:</p>
          <p className="text-sm">{error}</p>
        </div>
      )}
      {parsedOutput && !isLoading && !error && ( // Display output if no error and not loading
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
              <div className="flex justify-between items-center mb-1">
                <h4 className="text-md font-semibold text-gray-700">Simulated Signal Package Preview:</h4>
                <button
                  onClick={handleCopyPreview}
                  title={previewCopied ? "Copied!" : "Copy Signal Package Preview"}
                  className="p-1.5 rounded-md hover:bg-green-100 text-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 disabled:opacity-50"
                  aria-label={previewCopied ? "Signal Package Preview copied to clipboard" : "Copy Signal Package Preview"}
                  disabled={!parsedOutput.signalPackagePreview}
                >
                  {previewCopied ? <CheckIcon className="w-5 h-5 text-green-500" /> : <CopyIcon className="w-5 h-5" />}
                </button>
              </div>
              <pre className="bg-white p-3 rounded-md shadow-sm text-xs overflow-x-auto max-h-60 border border-green-200">
                {JSON.stringify(parsedOutput.signalPackagePreview, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
      {!specInput && !isLoading && !error && ( // If no spec has been provided yet, and not loading/error state for this component
         <p className="text-sm text-gray-500 italic p-4 text-center">Waiting for a JGTML spec to parse...</p>
      )}
       {specInput && !parsedOutput && !isLoading && !error && ( // If spec is provided, but no output, not loading and no error (e.g. LLM failed, parser hasn't run)
         <p className="text-sm text-gray-500 italic p-4 text-center">Ready to parse generated JGTML spec.</p>
      )}
    </FlowCard>
  );
};

export default IntentSpecParser;
