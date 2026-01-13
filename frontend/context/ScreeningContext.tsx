"use client";

import React, { createContext, useContext, useState, ReactNode } from "react";

interface ScreeningResult {
    result: string;
    confidence: number;
    recommendation: string;
}

interface ScreeningContextType {
    voiceResult: ScreeningResult | null;
    mriResult: ScreeningResult | null;
    setVoiceResult: (result: ScreeningResult) => void;
    setMriResult: (result: ScreeningResult) => void;
    resetScreening: () => void;
}

const ScreeningContext = createContext<ScreeningContextType | undefined>(undefined);

export const ScreeningProvider = ({ children }: { children: ReactNode }) => {
    const [voiceResult, setVoiceResult] = useState<ScreeningResult | null>(null);
    const [mriResult, setMriResult] = useState<ScreeningResult | null>(null);

    const resetScreening = () => {
        setVoiceResult(null);
        setMriResult(null);
    };

    return (
        <ScreeningContext.Provider
            value={{
                voiceResult,
                mriResult,
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
