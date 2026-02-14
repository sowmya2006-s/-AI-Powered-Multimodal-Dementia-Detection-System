import React from 'react';
import { useScreening } from '../../context/ScreeningContext';

const PatientForm: React.FC = () => {
    const { setStep, patientData, setPatientData } = useScreening();

    const handleStartScreening = () => {
        setStep(3);
    };

    return (
        <section className="bg-card rounded-radius shadow-shadow p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Patient Profile</h2>
            <p className="text-sub text-sm mb-6">
                Please provide patient details to personalize the screening.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div>
                    <label className="text-xs font-semibold text-sub block mb-2 uppercase tracking-wide">
                        Full Name
                    </label>
                    <input
                        type="text"
                        value={patientData.name}
                        onChange={(e) => setPatientData({ name: e.target.value })}
                        placeholder="Jane Doe"
                        className="w-full px-4 py-3 rounded-lg border border-gray-100 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
                    />
                </div>
                <div>
                    <label className="text-xs font-semibold text-sub block mb-2 uppercase tracking-wide">
                        Age
                    </label>
                    <input
                        type="number"
                        value={patientData.age}
                        onChange={(e) => setPatientData({ age: e.target.value })}
                        placeholder="65"
                        className="w-full px-4 py-3 rounded-lg border border-gray-100 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
                    />
                </div>

                <div className="md:col-span-2">
                    <label className="text-xs font-semibold text-sub block mb-2 uppercase tracking-wide">
                        Gender
                    </label>
                    <select
                        value={patientData.gender}
                        onChange={(e) => setPatientData({ gender: e.target.value })}
                        className="w-full px-4 py-3 rounded-lg border border-gray-100 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 appearance-none bg-[url('data:image/svg+xml;charset=utf-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20fill%3D%22none%22%20viewBox%3D%220%200%2020%2020%22%3E%3Cpath%20stroke%3D%22%236b7280%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%20stroke-width%3D%221.5%22%20d%3D%22m6%208%204%204%204-4%22%2F%3E%3C%2Fsvg%3E')] bg-[length:1.25em_1.25em] bg-[right_0.5rem_center] bg-no-repeat"
                    >
                        <option value="">Select</option>
                        <option value="Female">Female</option>
                        <option value="Male">Male</option>
                        <option value="Other">Other</option>
                    </select>
                </div>

                <div className="md:col-span-2">
                    <label className="text-xs font-semibold text-sub block mb-2 uppercase tracking-wide">
                        Medical History
                    </label>
                    <textarea
                        value={patientData.medicalHistory}
                        onChange={(e) => setPatientData({ medicalHistory: e.target.value })}
                        placeholder="Relevant conditions, medications, family history (optional)"
                        className="w-full px-4 py-3 rounded-lg border border-gray-100 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 min-height-[92px]"
                    />
                </div>

                <div className="md:col-span-2">
                    <label className="text-xs font-semibold text-sub block mb-2 uppercase tracking-wide">
                        Memory / Behavioral Concerns (optional)
                    </label>
                    <textarea
                        value={patientData.concerns}
                        onChange={(e) => setPatientData({ concerns: e.target.value })}
                        placeholder="Describe any memory changes or concerns"
                        className="w-full px-4 py-3 rounded-lg border border-gray-100 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 min-height-[92px]"
                    />
                </div>
            </div>

            <div className="mt-8 flex gap-3">
                <button
                    onClick={handleStartScreening}
                    className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-primary text-white font-semibold text-sm hover:bg-primary-600 transition-colors shadow-sm"
                >
                    Start Screening <i className="fas fa-arrow-right ml-1"></i>
                </button>
                <button
                    onClick={() => setStep(1)}
                    className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl border border-dashed border-gray-200 text-sub font-semibold text-sm hover:bg-gray-50 transition-colors"
                >
                    Back
                </button>
            </div>
        </section>
    );
};

export default PatientForm;
