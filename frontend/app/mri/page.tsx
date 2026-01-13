"use client";

import { useState } from "react";
import axios from "axios";
import { useScreening } from "@/context/ScreeningContext";
import Link from "next/link";

export default function MRIScreening() {
    const { setMriResult } = useScreening();
    const [file, setFile] = useState<File | null>(null);
    const [previewURL, setPreviewURL] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files || e.target.files.length === 0) return;
        const uploadedFile = e.target.files[0];
        setFile(uploadedFile);
        setPreviewURL(URL.createObjectURL(uploadedFile));
        setResult(null);
    };

    const analyzeMRI = async () => {
        if (!file) return;

        setLoading(true);
        setResult(null);

        const formData = new FormData();
        formData.append("mri_image", file);

        try {
            const response = await axios.post("http://localhost:8000/api/reports/mri-upload/", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            const { mri_result, confidence } = response.data;

            setResult({
                classification: mri_result,
                confidence: `${(confidence * 100).toFixed(0)}%`,
                isDemented: mri_result === "Demented"
            });

            setMriResult({
                result: mri_result,
                confidence: confidence,
                recommendation: mri_result === "Demented" ? "Consult Neurologist" : "Routine Checkup"
            });
        } catch (error) {
            console.error("MRI Analysis failed", error);
            alert("Error connecting to MRI analysis service. Please ensure backend is running.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="min-h-screen flex items-center justify-center px-6">
            <div className="max-w-xl w-full bg-white rounded-2xl shadow-lg p-8">
                <h2 className="text-2xl font-bold text-teal-600 mb-6 text-center">
                    Phase 3: MRI Analysis
                </h2>

                {/* Upload Section */}
                <div className="mb-6">
                    <label className="block text-sm font-medium mb-2">
                        Upload MRI Scan
                    </label>
                    <div className="border-2 border-dashed border-gray-200 rounded-xl p-6 flex flex-col items-center justify-center hover:bg-slate-50 transition cursor-pointer relative">
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleFileUpload}
                            className="absolute inset-0 opacity-0 cursor-pointer"
                        />
                        <p className="text-gray-500 text-sm">
                            {file ? file.name : "Drag & Drop or Click to Upload MRI Image"}
                        </p>
                    </div>
                </div>

                {/* MRI Preview */}
                {previewURL && (
                    <div className="mb-6">
                        <p className="text-sm font-medium mb-2">MRI Preview</p>
                        <div className="w-full h-48 bg-slate-100 rounded-lg overflow-hidden flex items-center justify-center">
                            <img
                                src={previewURL}
                                alt="MRI Preview"
                                className="max-h-full max-w-full object-contain"
                            />
                        </div>
                    </div>
                )}

                {/* Analyze Button */}
                <button
                    disabled={!file || loading}
                    onClick={analyzeMRI}
                    className={`w-full py-3 rounded-lg text-white text-lg font-semibold transition ${loading || !file
                            ? "bg-gray-400 cursor-not-allowed"
                            : "bg-teal-600 hover:bg-teal-700"
                        }`}
                >
                    {loading ? "Running Swin Transformer..." : "Analyze MRI"}
                </button>

                {/* Result Card */}
                {result && (
                    <div className="mt-8 bg-slate-50 p-6 rounded-xl text-center border-t-4 border-teal-600">
                        <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-2">
                            MRI Result
                        </h3>
                        <p className={`text-xl font-bold ${result.isDemented ? "text-red-600" : "text-green-600"}`}>
                            {result.classification}
                        </p>
                        <p className="text-sm text-gray-600">
                            Confidence: {result.confidence}
                        </p>
                        <div className="mt-4">
                            <Link href="/summary">
                                <button className="text-teal-600 font-semibold text-sm hover:underline">
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
