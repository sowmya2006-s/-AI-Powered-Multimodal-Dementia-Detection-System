import React from 'react';
import { useScreening } from '../../context/ScreeningContext';

const steps = [
    { id: 1, label: 'Login' },
    { id: 2, label: 'Patient' },
    { id: 3, label: 'Speech' },
    { id: 4, label: 'Test' },
    { id: 5, label: 'MRI' },
    { id: 6, label: 'Results' },
];

const StepsUI: React.FC = () => {
    const { currentStep } = useScreening();

    return (
        <div className="bg-card rounded-radius shadow-shadow p-6 mb-6">
            <div className="flex justify-between items-start gap-2 overflow-x-auto pb-2 scrollbar-hide">
                {steps.map((step, idx) => (
                    <div key={step.id} className="flex flex-col items-center min-w-[70px]">
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm transition-all duration-300 ${currentStep === step.id
                                ? 'bg-primary text-white shadow-lg ring-4 ring-primary/10'
                                : currentStep > step.id
                                    ? 'bg-blue-100 text-primary'
                                    : 'bg-gray-100 text-muted'
                            }`}>
                            {currentStep > step.id ? <i className="fas fa-check"></i> : step.id}
                        </div>
                        <div className={`mt-2 text-[10px] font-bold uppercase tracking-wider ${currentStep === step.id ? 'text-primary' : 'text-sub'
                            }`}>
                            {step.label}
                        </div>
                    </div>
                ))}
            </div>

            <div className="mt-4 h-1.5 w-full bg-gray-100 rounded-full overflow-hidden">
                <div
                    className="h-full bg-gradient-to-r from-primary to-primary-600 transition-all duration-500 ease-out"
                    style={{ width: `${((currentStep - 1) / (steps.length - 1)) * 100}%` }}
                ></div>
            </div>
        </div>
    );
};

export default StepsUI;
