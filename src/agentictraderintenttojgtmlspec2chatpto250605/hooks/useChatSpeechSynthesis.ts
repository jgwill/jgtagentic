import { useState, useEffect, useCallback, useRef } from 'react';

interface SpeechSynthesisHook {
  isSpeaking: boolean;
  speak: (text: string) => void;
  cancel: () => void;
  browserSupportsSpeechSynthesis: boolean;
  error: string | null;
}

const useChatSpeechSynthesis = (): SpeechSynthesisHook => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);

  const browserSupportsSpeechSynthesis =
    typeof window !== 'undefined' && 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;

  useEffect(() => {
    if (!browserSupportsSpeechSynthesis) {
      setError('Speech synthesis is not supported in this browser.');
      return;
    }

    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance();
    utterance.lang = 'en-US';
    utterance.pitch = 1;
    utterance.rate = 1;
    utterance.volume = 1;
    utteranceRef.current = utterance;

    utterance.onstart = () => {
      setIsSpeaking(true);
      setError(null);
    };

    utterance.onend = () => {
      setIsSpeaking(false);
    };

    utterance.onerror = (event: SpeechSynthesisErrorEvent) => {
      console.error('Speech synthesis error:', event.error);
      setError(`Speech synthesis error: ${event.error}`);
      setIsSpeaking(false);
    };

    return () => {
      if (synth.speaking) {
        synth.cancel();
      }
      if (utteranceRef.current) {
        utteranceRef.current.onstart = null;
        utteranceRef.current.onend = null;
        utteranceRef.current.onerror = null;
      }
    };
  }, [browserSupportsSpeechSynthesis]);

  const speak = useCallback((text: string) => {
    if (!browserSupportsSpeechSynthesis || !utteranceRef.current) {
      setError('Speech synthesis is not available or not initialized.');
      return;
    }
    const synth = window.speechSynthesis;
    if (synth.speaking) {
      synth.cancel(); // Cancel current speech before starting new one
    }
    utteranceRef.current.text = text;
    synth.speak(utteranceRef.current);
    // setIsSpeaking(true) will be handled by onstart event
  }, [browserSupportsSpeechSynthesis]);

  const cancel = useCallback(() => {
    if (!browserSupportsSpeechSynthesis) return;
    const synth = window.speechSynthesis;
    if (synth.speaking) {
      synth.cancel();
    }
    setIsSpeaking(false); // Explicitly set speaking to false on cancel
  }, [browserSupportsSpeechSynthesis]);

  return {
    isSpeaking,
    speak,
    cancel,
    browserSupportsSpeechSynthesis,
    error,
  };
};

export default useChatSpeechSynthesis;