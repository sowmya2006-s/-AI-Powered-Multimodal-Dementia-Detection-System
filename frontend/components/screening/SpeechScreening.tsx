import React, { useState, useRef } from 'react';
import { useScreening } from '../../context/ScreeningContext';

const SpeechScreening: React.FC = () => {
    const { setStep, setVoiceResult, setVoiceProbability, setVoiceLabel } = useScreening();
    const [recording, setRecording] = useState(false);
    const [status, setStatus] = useState('Click the microphone to start a short recording');
    const [isFinished, setIsFinished] = useState(false);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const chunksRef = useRef<Blob[]>([]);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorderRef.current = mediaRecorder;
            chunksRef.current = [];

            mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0) chunksRef.current.push(e.data);
            };

            mediaRecorder.onstop = async () => {
                const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
                setStatus('Analyzing speech patterns...');

                try {
                    const formData = new FormData();
                    formData.append('audio_file', blob, 'recording.webm');

                    const response = await fetch('http://localhost:8000/api/voice/upload/', {
                        method: 'POST',
                        body: formData,
                    });

                    if (!response.ok) throw new Error('Backend analysis failed');

                    const data = await response.json();
                    setVoiceProbability(data.probability);
                    setVoiceLabel(data.risk_level);
                    setVoiceResult(data);
                    setStatus('Recording complete — analysis finished');
                    setIsFinished(true);
                } catch (err) {
                    console.error("Inference fetch error:", err);
                    setVoiceResult({ result: 'Simulated', probability: 0.65, recommendation: 'Proceed' });
                    setVoiceProbability(0.65);
                    setVoiceLabel("MEDIUM");
                    setStatus('Simulated result (backend unreachable)');
                    setIsFinished(true);
                }
            };

            mediaRecorder.start();
            setRecording(true);
            setStatus('Recording — please speak');

            // Automatically stop after 4 seconds
            setTimeout(() => {
                if (mediaRecorder.state === 'recording') {
                    mediaRecorder.stop();
                    setRecording(false);
                    stream.getTracks().forEach(track => track.stop());
                }
            }, 4000);

        } catch (err) {
            console.error("Recording error:", err);
            setStatus('Mic error');
        }
    };

    const handleMicClick = () => {
        if (recording) {
            if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
                mediaRecorderRef.current.stop();
            }
            setRecording(false);
        } else {
            startRecording();
        }
    };

    return (
        <section className="bg-card rounded-radius shadow-shadow p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Step 1: Speech Screening</h2>
            <p className="text-sub text-sm mb-6">
                This short test captures voice patterns that may indicate cognitive changes. Please speak clearly.
            </p>

            <div className="flex flex-wrap gap-8 items-center mt-6">
                <div className="text-center">
                    <div
                        onClick={handleMicClick}
                        className={`w-28 h-28 rounded-full flex items-center justify-center text-4xl cursor-pointer transition-all duration-200 shadow-lg ${recording
                            ? 'bg-primary text-white scale-105 animate-pulse'
                            : 'bg-soft text-primary hover:bg-blue-100'
                            }`}
                        title="Click to record"
                    >
                        <i className={`fas ${recording ? 'fa-stop' : 'fa-microphone'}`}></i>
                    </div>

                    <div className="flex gap-1.5 justify-center mt-4 h-8 items-end">
                        {[1, 2, 3, 4, 5].map((i) => (
                            <div
                                key={i}
                                className={`w-1.5 bg-primary rounded-full transition-all duration-300 ${recording ? 'animate-wave' : 'h-2 opacity-30'
                                    }`}
                                style={{
                                    animationDelay: `${i * 0.1}s`,
                                    height: recording ? '100%' : '8px'
                                }}
                            ></div>
                        ))}
                    </div>

                    <div className={`mt-4 text-xs font-semibold ${isFinished ? 'text-green-600' : 'text-sub'}`}>
                        {status}
                    </div>
                </div>

                <div className="flex-1 min-w-[260px]">
                    <label className="text-xs font-semibold text-sub block mb-2 uppercase tracking-wide">
                        Sentence to speak
                    </label>
                    <div className="bg-soft rounded-xl p-5 border border-blue-50">
                        <strong className="text-primary text-lg leading-relaxed italic">
                            "The quick brown fox jumps over the lazy dog."
                        </strong>
                    </div>

                    <div className="mt-8 flex gap-3">
                        <button
                            disabled={!isFinished}
                            onClick={() => setStep(4)}
                            className={`inline-flex items-center gap-2 px-6 py-2.5 rounded-xl font-semibold text-sm transition-all shadow-sm ${isFinished
                                ? 'bg-primary text-white hover:bg-primary-600'
                                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                                }`}
                        >
                            Continue to Cognitive Test
                        </button>
                        <button
                            onClick={() => setStep(2)}
                            className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl border border-primary text-primary font-semibold text-sm hover:bg-soft transition-colors"
                        >
                            Back
                        </button>
                    </div>
                </div>
            </div>

            <style jsx>{`
        @keyframes wave {
          0% { opacity: 0.6; transform: scaleY(0.6); height: 8px; }
          50% { opacity: 1; transform: scaleY(1.4); height: 24px; }
          100% { opacity: 0.6; transform: scaleY(0.75); height: 10px; }
        }
        .animate-wave {
          animation: wave 1.2s infinite ease-in-out;
        }
      `}</style>
        </section>
    );
};

export default SpeechScreening;
