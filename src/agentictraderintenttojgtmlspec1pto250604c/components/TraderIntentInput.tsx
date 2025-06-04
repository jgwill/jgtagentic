import React, { useState } from 'react';
import { EXAMPLE_NARRATIVE } from '../constants';
import FlowCard from './FlowCard';
import { MicIcon, PlayIcon, LoaderIcon, RefreshCwIcon } from './icons/LucideIcons';

interface TraderIntentInputProps {
  onSubmitNarrative: (narrative: string) => void;
  onReset: () => void;
  isLoading: boolean;
  initialNarrative?: string;
}

const TraderIntentInput: React.FC<TraderIntentInputProps> = ({ onSubmitNarrative, onReset, isLoading, initialNarrative = "" }) => {
  const [narrative, setNarrative] = useState<string>(initialNarrative);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (narrative.trim()) {
      onSubmitNarrative(narrative.trim());
    }
  };
  
  const handleUseExample = () => {
    setNarrative(EXAMPLE_NARRATIVE);
  };

  return (
    <FlowCard
      title="🎤 Trader Intent"
      description="Describe your market analysis, indicators, patterns, and overall trading intent."
      bgColorClass="bg-purple-50"
      icon={<MicIcon className="w-6 h-6 text-purple-600" />}
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          value={narrative}
          onChange={(e) => setNarrative(e.target.value)}
          placeholder="e.g., 'On EUR/USD H4, I see a bullish engulfing pattern near the 50 EMA. Alligator is sleeping. Expecting a breakout upwards...'"
          rows={8}
          className="w-full p-3 border border-purple-200 rounded-lg shadow-sm focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors duration-150 ease-in-out text-sm bg-white"
          disabled={isLoading}
        />
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div className="flex items-center gap-3">
            <button
              type="submit"
              className="px-5 py-2.5 bg-purple-600 text-white rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center transition-colors duration-150 ease-in-out text-sm font-medium"
              disabled={isLoading || !narrative.trim()}
            >
              {isLoading ? (
                <>
                  <LoaderIcon className="w-5 h-5 mr-2" />
                  Processing...
                </>
              ) : (
                <>
                  <PlayIcon className="w-5 h-5 mr-2" />
                  Generate Spec
                </>
              )}
            </button>
            <button
              type="button"
              onClick={onReset}
              className="px-5 py-2.5 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 disabled:opacity-50 flex items-center justify-center transition-colors duration-150 ease-in-out text-sm"
              disabled={isLoading}
            >
              <RefreshCwIcon className="w-5 h-5 mr-2"/> Reset
            </button>
          </div>
           <button
              type="button"
              onClick={handleUseExample}
              className="text-sm text-purple-600 hover:text-purple-800 underline disabled:opacity-50"
              disabled={isLoading}
            >
              Use Example Narrative
            </button>
        </div>
      </form>
    </FlowCard>
  );
};

export default TraderIntentInput;
