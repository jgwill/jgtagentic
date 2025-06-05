import React, { useRef, useEffect, useState, useCallback } from 'react';
import { CameraIcon, RefreshCwIcon, CheckIcon } from '../icons/LucideIcons';

interface CameraModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCapture: (imageDataUrl: string) => void;
}

const CameraModal: React.FC<CameraModalProps> = ({ isOpen, onClose, onCapture }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);

  const startCamera = useCallback(async () => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
        setStream(mediaStream);
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
        setError(null);
        setCapturedImage(null); // Reset captured image when camera starts
      } catch (err) {
        console.error("Error accessing camera:", err);
        setError("Could not access camera. Please ensure permissions are granted.");
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            setStream(null);
        }
      }
    } else {
      setError("Camera access is not supported by this browser.");
    }
  }, [stream]); // Added stream to dependency array

  const stopCamera = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    if (videoRef.current) {
        videoRef.current.srcObject = null;
    }
  }, [stream]);

  useEffect(() => {
    if (isOpen) {
      startCamera();
    } else {
      stopCamera();
      setCapturedImage(null); // Clear image when modal closes
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen]); // startCamera/stopCamera have their own dependencies

   useEffect(() => {
    // Cleanup stream on component unmount
    return () => {
      stopCamera();
    };
  }, [stopCamera]);


  const handleCapture = () => {
    if (videoRef.current && canvasRef.current && stream) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const context = canvas.getContext('2d');
      if (context) {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageDataUrl = canvas.toDataURL('image/jpeg'); // Use jpeg for smaller size
        setCapturedImage(imageDataUrl);
        stopCamera(); // Stop camera after capture to show preview
      }
    }
  };

  const handleRetake = () => {
    setCapturedImage(null);
    startCamera();
  };

  const handleConfirmCapture = () => {
    if (capturedImage) {
      onCapture(capturedImage);
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div 
        className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75 p-4"
        role="dialog"
        aria-modal="true"
        aria-labelledby="camera-modal-title"
    >
      <div className="bg-white rounded-lg shadow-xl p-4 sm:p-6 w-full max-w-md transform transition-all">
        <h2 id="camera-modal-title" className="text-lg font-semibold text-gray-800 mb-4">Capture Image</h2>
        
        {error && <p className="text-red-500 text-sm mb-3 p-2 bg-red-50 rounded-md">{error}</p>}

        <div className="relative aspect-video bg-gray-200 rounded overflow-hidden mb-4">
          {capturedImage ? (
            <img src={capturedImage} alt="Captured" className="w-full h-full object-contain" />
          ) : (
            <video ref={videoRef} autoPlay playsInline className="w-full h-full object-contain" aria-label="Camera feed"></video>
          )}
          <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>
        </div>

        <div className="flex flex-col sm:flex-row justify-center items-center gap-3">
          {!capturedImage && stream && (
            <button
              onClick={handleCapture}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 flex items-center justify-center gap-2 w-full sm:w-auto"
            >
              <CameraIcon className="w-5 h-5" /> Capture
            </button>
          )}
          {capturedImage && (
            <>
              <button
                onClick={handleRetake}
                className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 flex items-center justify-center gap-2 w-full sm:w-auto"
              >
                <RefreshCwIcon className="w-5 h-5" /> Retake
              </button>
              <button
                onClick={handleConfirmCapture}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 flex items-center justify-center gap-2 w-full sm:w-auto"
              >
                <CheckIcon className="w-5 h-5" /> Confirm
              </button>
            </>
          )}
        </div>
         <button
            onClick={onClose}
            className="mt-4 w-full px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 sm:w-auto sm:mt-0 sm:absolute sm:top-4 sm:right-4"
            aria-label="Close camera modal"
          >
            Close
          </button>
      </div>
    </div>
  );
};

export default CameraModal;