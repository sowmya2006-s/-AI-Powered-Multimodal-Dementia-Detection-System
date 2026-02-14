"use client";

import React, { createContext, useContext, useState, ReactNode } from "react";

export interface PatientData {
    name: string;
    age: string;
    gender: string;
    medicalHistory: string;
    concerns: string;
}

export interface CognitiveScores {
    audio: number;
    visual: number;
}

interface ScreeningContextType {
    currentStep: number;
    patientData: PatientData;
    cognitiveScores: CognitiveScores;
    mriProbability: number;
    voiceResult: any | null;
    mriResult: any | null;
    voiceProbability: number;
    mriLabel: string;
    voiceLabel: string;
    setStep: (step: number) => void;
    setPatientData: (data: Partial<PatientData>) => void;
    setCognitiveScore: (type: 'audio' | 'visual', score: number) => void;
    setMriProbability: (prob: number) => void;
    setVoiceProbability: (prob: number) => void;
    setMriLabel: (label: string) => void;
    setVoiceLabel: (label: string) => void;
    setVoiceResult: (result: any) => void;
    setMriResult: (result: any) => void;
    resetScreening: () => void;
}

const defaultPatientData: PatientData = {
    name: "",
    age: "",
    gender: "",
    medicalHistory: "",
    concerns: ""
};

const defaultCognitiveScores: CognitiveScores = {
    audio: 0,
    visual: 0
};

const ScreeningContext = createContext<ScreeningContextType | undefined>(undefined);

export const ScreeningProvider = ({ children }: { children: ReactNode }) => {
    const [currentStep, setCurrentStep] = useState(1);
    const [patientData, setPatientDataState] = useState<PatientData>(defaultPatientData);
    const [cognitiveScores, setCognitiveScores] = useState<CognitiveScores>(defaultCognitiveScores);
    const [mriProbability, setMriProbability] = useState(0.0);
    const [voiceProbability, setVoiceProbability] = useState(0.0);
    const [mriLabel, setMriLabel] = useState("");
    const [voiceLabel, setVoiceLabel] = useState("");
    const [voiceResult, setVoiceResult] = useState<any | null>(null);
    const [mriResult, setMriResult] = useState<any | null>(null);

    const setStep = (step: number) => setCurrentStep(step);

    const setPatientData = (data: Partial<PatientData>) => {
        setPatientDataState(prev => ({ ...prev, ...data }));
    };

    const setCognitiveScore = (type: 'audio' | 'visual', score: number) => {
        setCognitiveScores(prev => ({ ...prev, [type]: score }));
    };

    const resetScreening = () => {
        setCurrentStep(1);
        setPatientDataState(defaultPatientData);
        setCognitiveScores(defaultCognitiveScores);
        setMriProbability(0.0);
        setVoiceProbability(0.0);
        setMriLabel("");
        setVoiceLabel("");
        setVoiceResult(null);
        setMriResult(null);
    };

    return (
        <ScreeningContext.Provider
            value={{
                currentStep,
                patientData,
                cognitiveScores,
                mriProbability,
                voiceProbability,
                mriLabel,
                voiceLabel,
                voiceResult,
                mriResult,
                setStep,
                setPatientData,
                setCognitiveScore,
                setMriProbability,
                setVoiceProbability,
                setMriLabel,
                setVoiceLabel,
                setVoiceResult,
                setMriResult,
                resetScreening,
            }}
        >
            {children}
        </ScreeningContext.Provider>
    );
};

export const useScreening = () => {
    const context = useContext(ScreeningContext);
    if (context === undefined) {
        throw new Error("useScreening must be used within a ScreeningProvider");
    }
    return context;
};

