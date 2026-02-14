"use client";

import React from 'react';
import Header from '@/components/screening/Header';
import StepsUI from '@/components/screening/StepsUI';
import LoginScreen from '@/components/screening/LoginScreen';
import PatientForm from '@/components/screening/PatientForm';
import SpeechScreening from '@/components/screening/SpeechScreening';
import CognitiveTest from '@/components/screening/CognitiveTest';
import MRIAnalysis from '@/components/screening/MRIAnalysis';
import ResultsReport from '@/components/screening/ResultsReport';
import { useScreening } from '@/context/ScreeningContext';

export default function ScreeningPage() {
    const { currentStep } = useScreening();

    const renderScreen = () => {
        switch (currentStep) {
            case 1: return <LoginScreen />;
            case 2: return <PatientForm />;
            case 3: return <SpeechScreening />;
            case 4: return <CognitiveTest />;
            case 5: return <MRIAnalysis />;
            case 6: return <ResultsReport />;
            default: return <LoginScreen />;
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-[#F8FBFF] to-[#F4F8FF] font-sans text-gray-800">
            <div className="max-w-[1100px] mx-auto px-5 py-8">
                <Header />

                <main className="mt-6 flex flex-col gap-5">
                    <StepsUI />
                    <div className="transition-all duration-300">
                        {renderScreen()}
                    </div>
                </main>

                <footer className="mt-12 text-center text-[11px] text-muted font-medium opacity-60">
                    NEUROSCREEN AI • MULTIMODAL DEMENTIA SCREENING SYSTEM • v1.0
                </footer>
            </div>
        </div>
    );
}
