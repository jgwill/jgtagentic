
import React, { useState, useCallback, useEffect, useRef } from 'react';
import TraderIntentInput from './components/TraderIntentInput';
import LLMTranslationEngine from './components/LLMTranslationEngine';
import IntentSpecParser from './components/IntentSpecParser';
import FlowCard from './components/FlowCard';
import { JGTMLSpec, ParsedSpecOutput } from './types';
import { translateNarrativeToSpec } from './services/geminiService';
import { simulateIntentSpecParsing } from './services/parserService'; // New service
import { ArrowDownIcon, DatabaseIcon, LayersIcon, RepeatIcon, TerminalSquareIcon, FileTextIcon } from './components/icons/LucideIcons';
import { EXAMPLE_NARRATIVES } from './data/exampleNarratives'; // Updated import
import ChatAssistantContainer from './components/chat/ChatAssistantContainer';

const App: React.FC = () => {
  const defaultNarrative = EXAMPLE_NARRATIVES[0]?.narrative || "";
  const [traderNarrative, setTraderNarrative] = useState<string>(defaultNarrative);
  const [generatedSpec, setGeneratedSpec] = useState<JGTMLSpec | null>(null);
  const [parsedOutput, setParsedOutput] = useState<ParsedSpecOutput | null>(null);
  
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [llmError, setLlmError] = useState<string | null>(null);
  const [parserError, setParserError] = useState<string | null>(null);
  const [currentActiveSection, setCurrentActiveSection] = useState<string | null>(null);
  const [isChatAssistantVisible, setIsChatAssistantVisible] = useState<boolean>(false);
  const [shouldScrollToInput, setShouldScrollToInput] = useState<boolean>(false);

  const traderIntentInputRef = useRef<HTMLDivElement>(null);


  const handleReset = useCallback(() => {
    setTraderNarrative(defaultNarrative);
    setGeneratedSpec(null);
    setParsedOutput(null);
    setIsLoading(false);
    setLlmError(null);
    setParserError(null);
    setCurrentActiveSection(null);
    setIsChatAssistantVisible(false); 
    setShouldScrollToInput(false);
  }, [defaultNarrative]);

  const handleNarrativeSubmit = useCallback(async (narrative: string) => {
    setIsLoading(true);
    setLlmError(null);
    setParserError(null);
    setGeneratedSpec(null);
    setParsedOutput(null);
    setTraderNarrative(narrative); 
    setCurrentActiveSection('llm');

    try {
      const spec = await translateNarrativeToSpec(narrative);
      setGeneratedSpec(spec);
      setLlmError(null); 
      setCurrentActiveSection('parser');
      
      try {
        const parsingResult = await simulateIntentSpecParsing(spec);
        setParsedOutput(parsingResult);
        setParserError(null); 
      } catch (parseErr) {
        const parseErrorMessage = (parseErr as Error).message || 'An unknown parsing error occurred.';
        setParserError(parseErrorMessage);
        console.error("Parsing simulation error:", parseErr);
        setParsedOutput(null);
      }
      
    } catch (llmErr) {
      const llmErrorMessage = (llmErr as Error).message || 'An unknown LLM error occurred.';
      setLlmError(llmErrorMessage);
      console.error("LLM Translation error:", llmErr);
      setGeneratedSpec(null); 
      setParsedOutput(null);
    } finally {
      setIsLoading(false);
      setCurrentActiveSection(null); 
    }
  }, []);

  const toggleChatAssistant = useCallback(() => {
    setIsChatAssistantVisible(prev => !prev);
  }, []);

  const handleUpdateNarrativeFromAssistant = useCallback((newNarrative: string) => {
    setTraderNarrative(newNarrative);
    setIsChatAssistantVisible(false); // Close assistant after using summary
    setShouldScrollToInput(true); // Signal to scroll
  }, []);

  useEffect(() => {
    if (shouldScrollToInput && !isChatAssistantVisible) {
      // Timeout ensures the layout has adjusted after chat assistant closes
      setTimeout(() => {
        traderIntentInputRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setShouldScrollToInput(false); // Reset flag
      }, 100); // Adjust timeout if needed, allows CSS transitions to start
    }
  }, [shouldScrollToInput, isChatAssistantVisible]);


  const ArrowSeparator: React.FC = () => (
    <div className="flex items-center justify-center text-gray-400 my-4 sm:my-6">
      <ArrowDownIcon className="w-6 h-6 sm:w-8 sm:h-8" />
    </div>
  );

  const showLlmSection = generatedSpec || (isLoading && currentActiveSection === 'llm') || llmError;
  const showParserSection = parsedOutput || (isLoading && currentActiveSection === 'parser') || parserError || (generatedSpec && !llmError);


  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 via-gray-50 to-slate-100 py-6 sm:py-10">
      <div className="container mx-auto px-4 max-w-3xl">
        <header className="mb-8 text-center">
           <h1 className="text-3xl sm:text-4xl font-bold text-gray-800">Trader Intent to JGTML Spec</h1>
           <p className="text-sm sm:text-base text-gray-600 mt-2">Transform natural language trading ideas into structured, actionable specifications.</p>
        </header>

        <div className="space-y-6">
          <FlowCard
            title="🔁 Echo Spiral Flow"
            description="From trader narrative to execution memory and back."
            bgColorClass="bg-yellow-50 border-yellow-200"
            icon={<RepeatIcon className="w-6 h-6 text-yellow-600" />}
          />
          <div ref={traderIntentInputRef}>
            <TraderIntentInput
              onSubmitNarrative={handleNarrativeSubmit}
              onReset={handleReset}
              isLoading={isLoading && (currentActiveSection === 'llm' || currentActiveSection === 'parser')} 
              initialNarrative={traderNarrative}
              onToggleChatAssistant={toggleChatAssistant}
              isChatAssistantVisible={isChatAssistantVisible}
            />
          </div>
          
          <div
            className={`
              transition-all duration-500 ease-in-out
              overflow-hidden
              ${isChatAssistantVisible ? 'max-h-[700px] opacity-100 mt-[-1.5rem] mb-6' : 'max-h-0 opacity-0 mt-0 mb-0'}
            `}
            aria-hidden={!isChatAssistantVisible}
            role="region" 
            aria-labelledby="chat-assistant-heading" 
          >
            {isChatAssistantVisible && ( 
              <ChatAssistantContainer 
                onUpdateNarrative={handleUpdateNarrativeFromAssistant}
              />
            )}
          </div>
          
          {showLlmSection && <ArrowSeparator />}

          {showLlmSection && (
            <LLMTranslationEngine
              spec={generatedSpec}
              isLoading={isLoading && currentActiveSection === 'llm'}
              error={llmError} 
            />
          )}
          
          {showParserSection && <ArrowSeparator />}

          {/* Renamed IntentSpecParser card based on user's provided example */}
          {showParserSection && (
             <FlowCard
                title="🟩 IntentSpecParser (Interpreter)"
                description="Reads .jgtml-spec → constructs signal package"
                bgColorClass="bg-green-50"
                icon={<FileTextIcon className="w-6 h-6 text-green-600" />}
              >
                <IntentSpecParser
                  specInput={generatedSpec} 
                  parsedOutput={parsedOutput}
                  isLoading={isLoading && currentActiveSection === 'parser'}
                  error={parserError}
                />
              </FlowCard>
          )}

          {parsedOutput && !llmError && !parserError && (
            <>
              <ArrowSeparator />
              <FlowCard
                title="🟦 JGTML Execution Core"
                description="Core logic to interpret and execute strategy commands from spec"
                bgColorClass="bg-indigo-50 border-indigo-200"
                icon={<LayersIcon className="w-6 h-6 text-indigo-600" />}
              >
                <div className="pl-4 mt-2 space-y-1 text-sm text-gray-700">
                    <div>• run_spec() executor</div>
                    <div>• Indicator loader (AO, Alligator)</div>
                    <div>• Signal validator engine</div>
                    <div>• Decision node: ENTER / WAIT / EXIT</div>
                </div>
                <p className="mt-3 text-xs text-gray-500 italic">This step is typically executed on a backend server or local Python environment using the JGTML library.</p>
              </FlowCard>

              <ArrowSeparator />
              <FlowCard
                title="📦 CampaignLauncher"
                description="Materializes validated signal into an executable campaign script or API action"
                bgColorClass="bg-pink-50 border-pink-200"
                icon={<TerminalSquareIcon className="w-6 h-6 text-pink-600" />}
              >
                <p className="text-sm text-gray-600">
                  The final signal package is used to generate an executable script for trade entry,
                  potentially integrating with exchange APIs or trading platforms.
                </p>
              </FlowCard>

              <ArrowSeparator />
              <FlowCard
                title="🗃️ Trading Echo Lattice (Memory Crystallization)"
                description="Records outcome + feedback to memory crystal"
                bgColorClass="bg-gray-100 border-gray-200"
                icon={<DatabaseIcon className="w-6 h-6 text-gray-600" />}
              >
                <p className="text-sm text-gray-600">
                  Outcomes, market conditions, and any manual feedback are stored. This data refines future
                  LLM translations and strategy adaptations, completing the Echo Spiral.
                </p>
              </FlowCard>
            </>
          )}
        </div>
        <footer className="text-center mt-12 py-6 border-t border-gray-200">
            <p className="text-sm text-gray-500">&copy; {new Date().getFullYear()} Trader Tech Inc. All rights reserved.</p>
        </footer>
      </div>
    </div>
  );
};

export default App;
