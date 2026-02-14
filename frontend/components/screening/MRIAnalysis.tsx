import React, { useState } from 'react';
import { useScreening } from '../../context/ScreeningContext';

const MRIAnalysis: React.FC = () => {
    const { setStep, mriProbability, setMriProbability, setMriLabel, setMriResult } = useScreening();
    const [preview, setPreview] = useState<string | null>(null);
    const [analyzing, setAnalyzing] = useState(false);

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const url = URL.createObjectURL(file);
            setPreview(url);
            setAnalyzing(true);

            try {
                const formData = new FormData();
                formData.append('mri_image', file);

                const response = await fetch('http://localhost:8000/api/reports/mri-upload/', {
                    method: 'POST',
                    body: formData,
                });

                if (!response.ok) throw new Error('MRI analysis failed');

                const data = await response.json();
                setMriProbability(data.confidence);
                setMriLabel(data.mri_result);
                setMriResult(data);
            } catch (err) {
                console.error("MRI fetch error:", err);
                // Fallback for demo if unreachable
                setMriProbability(0.72);
                setMriLabel("Demented (Simulated)");
            } finally {
                setAnalyzing(false);
            }
        }
    };

    const useSample = () => {
        setPreview('https://placehold.co/420x260/E8F2FF/2C6DB4?text=Sample+MRI');
        setMriProbability(0.68);
        setMriLabel("VeryMildDemented");
    };

    return (
        <section className="bg-card rounded-radius shadow-shadow p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Step 3: Brain Scan Analysis</h2>
            <p className="text-sub text-sm mb-6">
                Upload an MRI report image (or use sample). This demo shows a structural change probability (illustrative).
            </p>

            <div className="flex flex-wrap gap-3 items-center mb-6">
                <input
                    type="file"
                    onChange={handleFileUpload}
                    accept="image/*"
                    className="text-sm text-sub file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-soft file:text-primary hover:file:bg-blue-100 cursor-pointer"
                />
                <button
                    onClick={useSample}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-soft text-primary font-semibold text-xs hover:bg-blue-100 transition-colors"
                >
                    <i className="fas fa-image"></i> Use Sample MRI
                </button>
            </div>

            <div className="flex flex-wrap lg:flex-nowrap gap-6 items-start">
                <div className="w-full max-w-[420px] aspect-video rounded-xl bg-gradient-to-br from-soft to-[#F0F7FF] flex items-center justify-center relative overflow-hidden shadow-inner border border-blue-50">
                    {preview ? (
                        <img src={preview} alt="MRI" className="w-full h-full object-cover" />
                    ) : (
                        <div className="text-center text-muted font-medium italic">
                            No MRI uploaded
                        </div>
                    )}
                    {analyzing && (
                        <div className="absolute inset-0 bg-white/60 backdrop-blur-[2px] flex flex-col items-center justify-center gap-3">
                            <i className="fas fa-circle-notch fa-spin text-3xl text-primary"></i>
                            <span className="text-xs font-bold text-primary uppercase tracking-widest">Analyzing Structure...</span>
                        </div>
                    )}
                    <div className="absolute left-[46%] top-[40%] w-16 h-10 bg-red-400/60 rounded-[50%] animate-pulse-slow"></div>
                </div>

                <div className="flex-1 min-w-[280px]">
                    <div className="bg-white rounded-xl border border-blue-50 p-5 shadow-sm">
                        <div className="text-xs font-bold text-sub uppercase tracking-wider mb-2">
                            Detected Classification
                        </div>
                        <div className="text-3xl font-black text-primary mb-1">
                            {useScreening().mriLabel || 'N/A'}
                        </div>
                        <div className="text-xs font-bold text-primary opacity-60 mb-2">
                            Confidence: {(mriProbability * 100).toFixed(1)}%
                        </div>
                        <div className="text-[11px] text-muted leading-relaxed">
                            Hippocampal volume variation is visualized for illustrative screening purposes only.
                        </div>
                    </div>

                    <div className="mt-8 flex gap-3">
                        <button
                            onClick={() => setStep(6)}
                            className="inline-flex items-center gap-2 px-8 py-3 rounded-xl bg-primary text-white font-bold text-sm hover:bg-primary-600 transition-all shadow-md active:translate-y-0.5"
                        >
                            View Full Results
                        </button>
                        <button
                            onClick={() => setStep(4)}
                            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl border border-dashed border-gray-200 text-sub font-semibold text-sm hover:bg-gray-50 transition-colors"
                        >
                            Back
                        </button>
                    </div>
                </div>
            </div>

            <style jsx>{`
        @keyframes pulse-slow {
          0% { opacity: 0.3; transform: scale(1); }
          100% { opacity: 0.8; transform: scale(1.1); }
        }
        .animate-pulse-slow {
          animation: pulse-slow 1.8s infinite alternate ease-in-out;
        }
      `}</style>
        </section>
    );
};

export default MRIAnalysis;
