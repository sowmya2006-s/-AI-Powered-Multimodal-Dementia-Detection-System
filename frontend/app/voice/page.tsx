"use client";

import { useState } from "react";
import axios from "axios";
import { useScreening } from "@/context/ScreeningContext";
import Link from "next/link";

export default function VoiceScreening() {
    const { setVoiceResult } = useScreening();
    const [audioFile, setAudioFile] = useState<File | null>(null);
    const [audioURL, setAudioURL] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [loadingStep, setLoadingStep] = useState("");
    const [result, setResult] = useState<any>(null);

    const handleAudioUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files || e.target.files.length === 0) return;
        const file = e.target.files[0];
        setAudioFile(file);
        setAudioURL(URL.createObjectURL(file));
        setResult(null);
    };

    const analyzeVoice = async () => {
        if (!audioFile) return;

        setLoading(true);
        setResult(null);
        setLoadingStep("Extracting MFCCs...");

        const formData = new FormData();
        formData.append("audio_file", audioFile);

        try {
            // Simulate step transitions for UX while API runs
            setTimeout(() => setLoadingStep("Running Swin Transformer..."), 1000);
            setTimeout(() => setLoadingStep("Running Bagging Inference..."), 2200);

            const response = await axios.post("http://localhost:8000/api/voice/upload/", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            const { risk_level, probability } = response.data;

            setResult({
                risk: risk_level === "HIGH" ? "High Dementia Risk" : (risk_level === "MEDIUM" ? "Mild Dementia Risk" : "Normal / Low Risk"),
                confidence: `${(probability * 100).toFixed(0)}%`,
                isHigh: risk_level === "HIGH" || risk_level === "MEDIUM"
            });

            setVoiceResult({
                result: risk_level === "HIGH" ? "High Dementia Risk" : (risk_level === "MEDIUM" ? "Mild Dementia Risk" : "Normal"),
                confidence: probability,
                recommendation: risk_level === "LOW" ? "No concern" : "Further evaluation needed"
            });
        } catch (error) {
            console.error("Analysis failed", error);
            alert("Backend error. Please ensure the server is running at localhost:8000");
        } finally {
            setLoading(false);
            setLoadingStep("");
        }
    };

    return (
        <main className="min-h-screen flex items-center justify-center px-6">
            <div className="max-w-xl w-full bg-white rounded-2xl shadow-lg p-8">
                <h2 className="text-2xl font-bold text-blue-600 mb-6 text-center">
                    Phase 1: Voice Screening
                </h2>

                {/* Upload */}
                <div className="mb-6">
                    <label className="block text-sm font-medium mb-2">
                        Upload Patient Voice
                    </label>
                    <input
                        type="file"
                        accept="audio/*"
                        onChange={handleAudioUpload}
                        className="w-full border rounded-lg p-2"
                    />
                </div>

                {/* Audio Preview */}
                {audioURL && (
                    <div className="mb-6">
                        <p className="text-sm font-medium mb-2">Audio Preview</p>
                        <audio controls key={audioURL} className="w-full">
                            <source src={audioURL} />
                        </audio>
                    </div>
                )}

                {/* Analyze Button */}
                <button
                    disabled={!audioFile || loading}
                    onClick={analyzeVoice}
                    className={`w-full py-3 rounded-lg text-white text-lg transition ${loading || !audioFile
                            ? "bg-gray-400 cursor-not-allowed"
                            : "bg-blue-600 hover:bg-blue-700"
                        }`}
                >
                    {loading ? "Analyzing Voice..." : "Analyze Voice"}
                </button>

                {/* Loading */}
                {loading && (
                    <p className="text-center text-sm text-gray-500 mt-4 animate-pulse">
                        {loadingStep || "Initializing..."}
                    </p>
                )}

                {/* Result */}
                {result && (
                    <div className="mt-6 bg-slate-50 p-6 rounded-xl text-center border-t-4 border-blue-600">
                        <p className={`text-xl font-bold mb-1 ${result.isHigh ? "text-red-600" : "text-green-600"}`}>
                            {result.risk}
                        </p>
                        <p className="text-sm text-gray-600">
                            Confidence: {result.confidence}
                        </p>
                        <div className="mt-4">
                            <Link href="/summary">
                                <button className="text-blue-600 font-semibold text-sm hover:underline">
                                    View Final Summary →
                                </button>
                            </Link>
                        </div>
                    </div>
                )}
            </div>
        </main>
    );
}
