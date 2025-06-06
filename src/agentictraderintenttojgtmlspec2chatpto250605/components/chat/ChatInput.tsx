
import React, { useState, useEffect, FormEvent, useRef, ChangeEvent } from 'react';
import { SendHorizonalIcon, MicIcon, LoaderIcon, PaperclipIcon, CameraIcon, PlayIcon, SquareIcon, Trash2Icon } from '../icons/LucideIcons';
import useChatSpeechRecognition from '../../hooks/useChatSpeechRecognition';
import CameraModal from './CameraModal'; // Import CameraModal

interface ChatInputProps {
  onSendMessage: (data: {
    text: string;
    file?: File | null; // For image upload
    base64ImageData?: string | null; // For camera capture
    imageMimeType?: string | null;
    recordedAudio?: Blob | null; // For audio recording
    audioMimeType?: string | null;
  }) => void;
  isLoading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
  const [inputValue, setInputValue] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [filePreview, setFilePreview] = useState<string | null>(null);
  
  const [isRecording, setIsRecording] = useState(false);
  const [recordedAudio, setRecordedAudio] = useState<{ blob: Blob; url: string } | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [capturedImage, setCapturedImage] = useState<string | null>(null); // base64

  const {
    isListening: isSpeechListening,
    transcript,
    startListening: startSpeechListening,
    stopListening: stopSpeechListening,
    resetTranscript,
    browserSupportsSpeechRecognition,
    error: speechError,
  } = useChatSpeechRecognition();

  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (transcript) {
      setInputValue(transcript);
    }
  }, [transcript]);

  const clearAttachments = () => {
    setSelectedFile(null);
    setFilePreview(null);
    setRecordedAudio(null);
    setCapturedImage(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if ((inputValue.trim() || selectedFile || recordedAudio || capturedImage) && !isLoading) {
      onSendMessage({
        text: inputValue.trim(),
        file: selectedFile,
        base64ImageData: capturedImage,
        imageMimeType: capturedImage ? 'image/jpeg' : (selectedFile?.type.startsWith('image/') ? selectedFile.type : null),
        recordedAudio: recordedAudio?.blob,
        audioMimeType: recordedAudio?.blob.type
      });
      setInputValue('');
      clearAttachments();
      resetTranscript();
      if (isSpeechListening) stopSpeechListening();
    }
  };

  const toggleSpeechListening = () => {
    if (isSpeechListening) {
      stopSpeechListening();
    } else {
      clearAttachments(); // Clear other attachments when starting STT
      startSpeechListening();
    }
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type.startsWith('image/')) {
      clearAttachments();
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setFilePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    } else if (file) {
      alert("Please select an image file.");
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  const startAudioRecording = async () => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      try {
        clearAttachments();
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream);
        audioChunksRef.current = [];
        mediaRecorderRef.current.ondataavailable = (event) => {
          audioChunksRef.current.push(event.data);
        };
        mediaRecorderRef.current.onstop = () => {
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' }); // or 'audio/wav' etc.
          const audioUrl = URL.createObjectURL(audioBlob);
          setRecordedAudio({ blob: audioBlob, url: audioUrl });
          stream.getTracks().forEach(track => track.stop()); // Stop microphone access
        };
        mediaRecorderRef.current.start();
        setIsRecording(true);
      } catch (err) {
        console.error("Error starting audio recording:", err);
        alert("Could not start audio recording. Please ensure microphone permissions are granted.");
      }
    } else {
      alert("Audio recording is not supported by this browser.");
    }
  };

  const stopAudioRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };
  
  const handleToggleAudioRecord = () => {
    if (isRecording) {
      stopAudioRecording();
    } else {
      startAudioRecording();
    }
  };

  const handleOpenCamera = () => {
    clearAttachments();
    setIsCameraOpen(true);
  };

  const handleCaptureImage = (imageDataUrl: string) => {
    setCapturedImage(imageDataUrl); // This is base64
    setIsCameraOpen(false);
  };
  
  const inputDisabled = isLoading || isRecording || isSpeechListening || isCameraOpen;


  return (
    <>
      <form onSubmit={handleSubmit} className="p-3 border-t border-gray-200 bg-gray-50 rounded-b-lg">
        {(filePreview || recordedAudio || capturedImage) && (
          <div className="mb-2 p-2 border border-gray-200 rounded-md bg-white relative">
            {filePreview && <img src={filePreview} alt="Preview" className="max-h-20 rounded" />}
            {capturedImage && <img src={capturedImage} alt="Captured" className="max-h-20 rounded" />}
            {recordedAudio && (
              <div className="flex items-center gap-2">
                <audio controls src={recordedAudio.url} className="h-10 flex-grow"></audio>
                 <p className="text-xs text-gray-500">audio.webm</p>
              </div>
            )}
            <button 
              type="button" 
              onClick={clearAttachments} 
              className="absolute top-1 right-1 bg-red-500 text-white p-1 rounded-full hover:bg-red-600"
              aria-label="Remove attachment"
            >
              <Trash2Icon className="w-3 h-3" />
            </button>
          </div>
        )}

        <div className="flex items-end gap-2">
          {browserSupportsSpeechRecognition && (
            <button
              type="button"
              onClick={toggleSpeechListening}
              disabled={isLoading || isRecording || isCameraOpen}
              className={`p-2 rounded-full focus:outline-none transition-colors
                          ${isSpeechListening ? 'bg-red-500 hover:bg-red-600 text-white' : 'bg-gray-200 hover:bg-gray-300 text-gray-600'}
                          disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0`}
              aria-label={isSpeechListening ? "Stop listening" : "Start voice input"}
            >
              <MicIcon className="w-5 h-5" />
            </button>
          )}
           <button
            type="button"
            onClick={handleToggleAudioRecord}
            disabled={isLoading || isSpeechListening || isCameraOpen}
            className={`p-2 rounded-full focus:outline-none transition-colors
                        ${isRecording ? 'bg-red-500 hover:bg-red-600 text-white' : 'bg-gray-200 hover:bg-gray-300 text-gray-600'}
                        disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0`}
            aria-label={isRecording ? "Stop recording" : "Record audio message"}
          >
            {isRecording ? <SquareIcon className="w-5 h-5" /> : <MicIcon className="w-5 h-5" />}
          </button>
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileChange} 
            accept="image/*" 
            className="hidden" 
            id="chat-file-input"
          />
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={inputDisabled}
            className="p-2 rounded-full bg-gray-200 hover:bg-gray-300 text-gray-600 focus:outline-none transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
            aria-label="Attach image file"
          >
            <PaperclipIcon className="w-5 h-5" />
          </button>
           <button
            type="button"
            onClick={handleOpenCamera}
            disabled={inputDisabled}
            className="p-2 rounded-full bg-gray-200 hover:bg-gray-300 text-gray-600 focus:outline-none transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
            aria-label="Capture image with camera"
          >
            <CameraIcon className="w-5 h-5" />
          </button>
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={
              isSpeechListening ? "Listening..." : 
              isRecording ? "Recording audio..." :
              (speechError ? `Speech error: ${speechError}` : "Ask the assistant...")
            }
            rows={1}
            className="flex-grow p-2.5 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-purple-500 focus:border-purple-500 resize-none text-base text-gray-900 placeholder-gray-500 transition-colors duration-150 ease-in-out disabled:bg-gray-100"
            disabled={isLoading}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey && !isSpeechListening && !isRecording) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
          />
          <button
            type="submit"
            disabled={isLoading || (!inputValue.trim() && !selectedFile && !recordedAudio && !capturedImage)}
            className="p-2.5 bg-purple-600 text-white rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center transition-colors flex-shrink-0"
            aria-label="Send message"
          >
            {isLoading ? <LoaderIcon className="w-5 h-5" /> : <SendHorizonalIcon className="w-5 h-5" />}
          </button>
        </div>
        {speechError && <p className="text-xs text-red-500 mt-1 ml-12">{speechError}</p>}
      </form>
      <CameraModal 
        isOpen={isCameraOpen}
        onClose={() => setIsCameraOpen(false)}
        onCapture={handleCaptureImage}
      />
    </>
  );
};

export default ChatInput;