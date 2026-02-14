import React from 'react';
import { useScreening } from '../../context/ScreeningContext';

const ResultsReport: React.FC = () => {
    const { cognitiveScores, mriProbability, voiceProbability, mriLabel, voiceLabel, patientData, resetScreening } = useScreening();

    const calculateResults = () => {
        const rounds = 3;
        const cognitivePercent = Math.round(((cognitiveScores.audio + cognitiveScores.visual) / (rounds * 2)) * 100);

        // Final Fusion Logic: 40% Voice, 40% MRI, 20% Cognitive Tests
        const combined = Math.round(
            (voiceProbability * 100 * 0.4) +
            (mriProbability * 100 * 0.4) +
            (cognitivePercent * 0.2)
        );

        let riskLabel = 'Low';
        let riskColor = 'text-green-600';
        let riskBg = 'bg-green-50';
        let riskBorder = 'border-green-100';

        if (combined >= 70) {
            riskLabel = 'High';
            riskColor = 'text-red-500';
            riskBg = 'bg-red-50';
            riskBorder = 'border-red-100';
        } else if (combined >= 35) {
            riskLabel = 'Medium';
            riskColor = 'text-orange-500';
            riskBg = 'bg-orange-50';
            riskBorder = 'border-orange-100';
        }

        return { combined, riskLabel, riskColor, riskBg, riskBorder, cognitivePercent };
    };

    const { combined, riskLabel, riskColor, riskBg, riskBorder } = calculateResults();

    const handleDownload = () => {
        const report = {
            patient: patientData,
            cognitive: cognitiveScores,
            voiceProbability: voiceProbability,
            voiceLabel: voiceLabel,
            mriProbability: mriProbability,
            mriLabel: mriLabel,
            final: { combined, riskLabel },
            generatedAt: new Date().toISOString()
        };
        const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${(patientData.name || 'patient').replace(/\s+/g, '-').toLowerCase()}-neuroscreen-report.json`;
        a.click();
        URL.revokeObjectURL(url);
    };

    return (
        <section className="bg-card rounded-radius shadow-shadow p-6">
            <div className="flex justify-between items-start mb-6">
                <div>
                    <h2 className="text-2xl font-bold text-gray-800 mb-1">Diagnostic Screening Report</h2>
                    <p className="text-sub text-sm">Comprehensive multimodal AI analysis results</p>
                </div>
                <div className={`px-4 py-2 rounded-full border ${riskBg} ${riskBorder} ${riskColor} text-xs font-bold uppercase tracking-widest`}>
                    Status: {riskLabel} Risk
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                {/* Speech Card */}
                <div className="bg-white rounded-2xl border border-blue-50 p-5 shadow-sm">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="w-10 h-10 rounded-xl bg-blue-50 text-primary flex items-center justify-center">
                            <i className="fas fa-microphone"></i>
                        </div>
                        <div>
                            <div className="text-[10px] font-bold text-sub uppercase tracking-wider">Speech Analysis</div>
                            <div className="text-sm font-bold text-gray-800">{voiceLabel || 'Voice Patterns'}</div>
                        </div>
                    </div>
                    <div className="text-2xl font-black text-primary mb-1">
                        {(voiceProbability * 100).toFixed(1)}%
                    </div>
                    <div className="text-[10px] text-muted font-medium mb-3">Dementia Probability Score</div>
                    <div className="w-full bg-soft h-1.5 rounded-full overflow-hidden">
                        <div className="bg-primary h-full transition-all duration-1000" style={{ width: `${voiceProbability * 100}%` }}></div>
                    </div>
                </div>

                {/* MRI Card */}
                <div className="bg-white rounded-2xl border border-blue-50 p-5 shadow-sm">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="w-10 h-10 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
                            <i className="fas fa-brain"></i>
                        </div>
                        <div>
                            <div className="text-[10px] font-bold text-sub uppercase tracking-wider">Brain Scan (MRI)</div>
                            <div className="text-sm font-bold text-gray-800">{mriLabel || 'Pending'}</div>
                        </div>
                    </div>
                    <div className="text-2xl font-black text-purple-600 mb-1">
                        {(mriProbability * 100).toFixed(1)}%
                    </div>
                    <div className="text-[10px] text-muted font-medium mb-3">Model Confidence Level</div>
                    <div className="w-full bg-purple-50 h-1.5 rounded-full overflow-hidden">
                        <div className="bg-purple-500 h-full transition-all duration-1000" style={{ width: `${mriProbability * 100}%` }}></div>
                    </div>
                </div>

                {/* Combined Card */}
                <div className="bg-white rounded-2xl border border-blue-50 p-5 shadow-sm relative overflow-hidden">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="w-10 h-10 rounded-xl bg-orange-50 text-orange-500 flex items-center justify-center">
                            <i className="fas fa-chart-pie"></i>
                        </div>
                        <div>
                            <div className="text-[10px] font-bold text-sub uppercase tracking-wider">Overall Index</div>
                            <div className="text-sm font-bold text-gray-800">Fused Conclusion</div>
                        </div>
                    </div>
                    <div className={`text-2xl font-black ${riskColor} mb-1`}>
                        {combined}%
                    </div>
                    <div className="text-[10px] text-muted font-medium mb-3">Weighted Multi-modal Risk</div>
                    <div className={`w-full ${riskBg} h-1.5 rounded-full overflow-hidden`}>
                        <div className={`h-full transition-all duration-1000 ${riskColor.replace('text', 'bg')}`} style={{ width: `${combined}%` }}></div>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
                <div className="bg-white rounded-xl border border-blue-50 p-5 shadow-sm">
                    <h4 className="font-bold text-gray-800 text-sm mb-3 flex items-center gap-2">
                        <i className="fas fa-stethoscope text-primary"></i> Follow-up Recommendations
                    </h4>
                    <ul className="space-y-2.5">
                        {[
                            riskLabel === 'High' ? 'CRITICAL: Consult a neurologist immediately' : 'Consult a neurologist for further evaluation',
                            'Schedule a neuropsychological assessment',
                            'Review cardiovascular health factors',
                            'Consider genetic screening (APOE-ε4)'
                        ].map((rec, i) => (
                            <li key={i} className="text-xs text-sub flex items-start gap-2">
                                <span className="w-1.5 h-1.5 rounded-full bg-primary/40 mt-1.5 shrink-0"></span>
                                {rec}
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="bg-white rounded-xl border border-blue-50 p-5 shadow-sm">
                    <h4 className="font-bold text-gray-800 text-sm mb-3 flex items-center gap-2">
                        <i className="fas fa-lightbulb text-orange-400"></i> Interpretation Note
                    </h4>
                    <div className="text-xs text-sub leading-relaxed space-y-2">
                        <p>The system utilizes a <strong>Swin Transformer Bagging Ensemble</strong> for MRI analysis and a <strong>Swin MFCC Pipeline</strong> for speech analysis.</p>
                        <p>Results are combined using a weighted fusion algorithm prioritizing objective structural data and clinical speech markers.</p>
                    </div>
                </div>
            </div>

            <div className="mt-8 p-4 bg-soft/50 border border-blue-100 rounded-xl text-xs text-primary/80 leading-relaxed font-medium italic">
                <strong>Disclaimer:</strong> This is an AI-powered screening tool for research/demonstration purposes. It does not provide medical diagnoses.
            </div>

            <div className="mt-8 flex gap-3">
                <button
                    onClick={handleDownload}
                    className="inline-flex items-center gap-2 px-8 py-3 rounded-xl bg-primary text-white font-bold text-sm hover:bg-primary-600 transition-all shadow-md"
                >
                    <i className="fas fa-download"></i> Download Report
                </button>
                <button
                    onClick={resetScreening}
                    className="inline-flex items-center gap-2 px-6 py-3 rounded-xl border border-dashed border-gray-200 text-sub font-semibold text-sm hover:bg-gray-50 transition-colors"
                >
                    New Screening
                </button>
            </div>
        </section>
    );
};

export default ResultsReport;
