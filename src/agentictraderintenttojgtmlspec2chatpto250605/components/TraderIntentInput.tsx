
import React, { useState, useEffect, ChangeEvent } from 'react';
import { EXAMPLE_NARRATIVES, ExampleNarrative } from '../data/exampleNarratives'; // Updated import
import FlowCard from './FlowCard';
import { MicIcon, PlayIcon, LoaderIcon, RefreshCwIcon, MessageCircleIcon } from './icons/LucideIcons';

interface TraderIntentInputProps {
  onSubmitNarrative: (narrative: string) => void;
  onReset: () => void;
  isLoading: boolean;
  initialNarrative?: string;
  onToggleChatAssistant: () => void;
  isChatAssistantVisible: boolean;
}

const TraderIntentInput: React.FC<TraderIntentInputProps> = ({ 
  onSubmitNarrative, 
  onReset, 
  isLoading, 
  initialNarrative = "",
  onToggleChatAssistant,
  isChatAssistantVisible
}) => {
  const [narrative, setNarrative] = useState<string>(initialNarrative);
  const [selectedExampleId, setSelectedExampleId] = useState<string>("");

  useEffect(() => {
    setNarrative(initialNarrative);
    // If initialNarrative matches an example, set the dropdown correctly
    const matchingExample = EXAMPLE_NARRATIVES.find(ex => ex.narrative === initialNarrative);
    setSelectedExampleId(matchingExample ? matchingExample.id : "");
  }, [initialNarrative]);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (narrative.trim()) {
      onSubmitNarrative(narrative.trim());
    }
  };
  
  const handleExampleChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const exampleId = event.target.value;
    setSelectedExampleId(exampleId);
    const selectedExample = EXAMPLE_NARRATIVES.find(ex => ex.id === exampleId);
    if (selectedExample) {
      setNarrative(selectedExample.narrative);
    } else if (exampleId === "") {
      // Potentially clear narrative or set to initial if "Select an example..." is chosen
      // For now, let's keep it simple: if "" is selected, it means user cleared selection (though typically not an option in a select without a blank option)
      // Or, set narrative to "" if we add a "Select..." option with value ""
    }
  };

  return (
    <FlowCard
      title="🎤 Trader Intent"
      description="Describe your market analysis, indicators, patterns, and overall trading intent. Use the assistant below to help refine your narrative."
      bgColorClass="bg-purple-50"
      icon={<MicIcon className="w-6 h-6 text-purple-600" />}
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          value={narrative}
          onChange={(e) => {
            setNarrative(e.target.value);
            // If user types, deselect example from dropdown
            const matchingExample = EXAMPLE_NARRATIVES.find(ex => ex.narrative === e.target.value);
            setSelectedExampleId(matchingExample ? matchingExample.id : "");
          }}
          placeholder="e.g., 'On EUR/USD H4, I see a bullish engulfing pattern near the 50 EMA. Alligator is sleeping. Expecting a breakout upwards...'"
          rows={8}
          className="w-full p-3 border border-purple-200 rounded-lg shadow-sm focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors duration-150 ease-in-out text-base bg-white text-gray-900 placeholder-gray-500"
          disabled={isLoading}
          aria-label="Trader narrative input"
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
          <div className="flex items-center gap-3 flex-wrap">
            <button
                type="button"
                onClick={onToggleChatAssistant}
                className="text-sm text-purple-600 hover:text-purple-800 underline disabled:opacity-50 flex items-center gap-1"
                disabled={isLoading}
                aria-pressed={isChatAssistantVisible}
              >
                <MessageCircleIcon className="w-4 h-4" />
                {isChatAssistantVisible ? 'Hide Assistant' : 'Refine with Assistant'}
            </button>
            <div className="flex items-center gap-1">
              <label htmlFor="example-narrative-select" className="text-sm text-purple-600">Load Example:</label>
              <select
                id="example-narrative-select"
                value={selectedExampleId}
                onChange={handleExampleChange}
                disabled={isLoading}
                className="text-sm text-purple-600 bg-purple-50 border-purple-300 rounded-md p-1 focus:ring-purple-500 focus:border-purple-500 hover:bg-purple-100 disabled:opacity-50"
              >
                <option value="">Select...</option>
                {EXAMPLE_NARRATIVES.map((ex) => (
                  <option key={ex.id} value={ex.id}>
                    {ex.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </form>
    </FlowCard>
  );
};

export default TraderIntentInput;
