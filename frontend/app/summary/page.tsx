"use client";

import { useScreening } from "@/context/ScreeningContext";
import Link from "next/link";

export default function SummaryPage() {
    const { voiceResult, mriResult, resetScreening } = useScreening();

    const getCombinedAssessment = () => {
        if (!voiceResult && !mriResult) return "No tests performed yet.";

        const vRisk = voiceResult?.result.toLowerCase().includes("risk");
        const mRisk = mriResult?.result.toLowerCase().includes("demented");

        if (vRisk && mRisk) return "Likely Early-Stage Dementia";
        if (vRisk || mRisk) return "Further Clinical Evaluation Required";
        return "Low Risk Detected";
    };

    return (
        <main className="min-h-screen flex items-center justify-center px-6">
            <div className="max-w-2xl w-full bg-white rounded-2xl shadow-xl p-10">
                <h2 className="text-3xl font-bold text-center text-slate-800 mb-10 border-b pb-6">
                    Final Screening Summary
                </h2>

                <div className="space-y-8 mb-10">
                    {/* Voice Result */}
                    <div className="flex justify-between items-center bg-slate-50 p-6 rounded-xl">
                        <div>
                            <p className="text-sm font-bold text-gray-500 uppercase tracking-widest">Voice Analysis</p>
                            <p className={`text-xl font-bold ${voiceResult?.result.toLowerCase().includes("risk") ? "text-red-600" : "text-green-600"}`}>
                                {voiceResult ? voiceResult.result : "Not Performed"}
                            </p>
                        </div>
                        {voiceResult && (
                            <div className="text-right">
                                <p className="text-sm text-gray-400">Confidence</p>
                                <p className="text-lg font-bold text-slate-700">{(voiceResult.confidence * 100).toFixed(0)}%</p>
                            </div>
                        )}
                    </div>

                    {/* MRI Result */}
                    <div className="flex justify-between items-center bg-slate-50 p-6 rounded-xl">
                        <div>
                            <p className="text-sm font-bold text-gray-500 uppercase tracking-widest">MRI Analysis</p>
                            <p className={`text-xl font-bold ${mriResult?.result.toLowerCase().includes("demented") ? "text-red-600" : "text-green-600"}`}>
                                {mriResult ? mriResult.result : "Not Performed"}
                            </p>
                        </div>
                        {mriResult && (
                            <div className="text-right">
                                <p className="text-sm text-gray-400">Confidence</p>
                                <p className="text-lg font-bold text-slate-700">{(mriResult.confidence * 100).toFixed(0)}%</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Final Assessment */}
                <div className="bg-blue-50 border-2 border-blue-100 p-8 rounded-2xl text-center mb-10">
                    <p className="text-sm font-bold text-blue-600 uppercase tracking-widest mb-2">Final AI Assessment</p>
                    <p className="text-2xl font-black text-slate-900 mb-2">
                        {getCombinedAssessment()}
                    </p>
                    <p className="text-sm text-red-500 font-medium">
                        ⚠ Not a medical diagnosis. Please consult a specialist.
                    </p>
                </div>

                <div className="flex gap-4">
                    <Link href="/" className="flex-1">
                        <button
                            onClick={resetScreening}
                            className="w-full py-4 border-2 border-slate-200 text-slate-600 font-bold rounded-xl hover:bg-slate-50 transition"
                        >
                            Start New Session
                        </button>
                    </Link>
                    <button
                        onClick={() => window.print()}
                        className="flex-1 py-4 bg-slate-900 text-white font-bold rounded-xl hover:bg-black transition"
                    >
                        Save PDF Report
                    </button>
                </div>
            </div>
        </main>
    );
}
