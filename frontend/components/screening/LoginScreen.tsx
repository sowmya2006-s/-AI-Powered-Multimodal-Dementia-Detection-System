import React from 'react';
import { useScreening } from '../../context/ScreeningContext';

const LoginScreen: React.FC = () => {
    const { setStep } = useScreening();
    const [email, setEmail] = React.useState('');

    const handleSignIn = () => {
        if (!email.trim()) {
            alert('Please enter email or mobile to continue');
            return;
        }
        setStep(2);
    };

    return (
        <section className="bg-card rounded-radius shadow-shadow p-6">
            <div className="grid grid-cols-1 md:grid-cols-[1fr_380px] gap-5 items-center">
                <div>
                    <h2 className="text-2xl font-bold text-gray-800 mb-2">Login</h2>
                    <p className="text-sub text-sm mb-4">
                        Please sign in to begin the screening. Your privacy and comfort matter to us.
                    </p>

                    <div className="mt-4">
                        <label className="text-xs font-semibold text-sub block mb-2 uppercase tracking-wide">
                            Email / Mobile Number
                        </label>
                        <input
                            type="text"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="you@example.com or +91 9xxxxxxxxx"
                            className="w-full px-4 py-3 rounded-lg border border-gray-100 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
                        />
                    </div>

                    <div className="mt-4">
                        <label className="text-xs font-semibold text-sub block mb-2 uppercase tracking-wide">
                            Password
                        </label>
                        <input
                            type="password"
                            placeholder="••••••••"
                            className="w-full px-4 py-3 rounded-lg border border-gray-100 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
                        />
                    </div>

                    <div className="mt-6 flex flex-wrap gap-3">
                        <button
                            onClick={handleSignIn}
                            className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-primary text-white font-semibold text-sm hover:bg-primary-600 transition-colors shadow-sm"
                        >
                            <i className="fas fa-sign-in-alt"></i> Sign In
                        </button>
                        <button
                            onClick={() => alert('Create account flow not implemented in demo')}
                            className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl border border-primary text-primary font-semibold text-sm hover:bg-soft transition-colors"
                        >
                            New Patient? Create Account
                        </button>
                    </div>
                </div>

                <div className="bg-gradient-to-br from-soft to-[#F0F7FF] rounded-xl p-6 text-center text-primary shadow-inner">
                    <i className="fas fa-heartbeat text-5xl mb-4"></i>
                    <p className="font-bold text-lg leading-snug">
                        Early detection for better cognitive health outcomes
                    </p>
                    <p className="text-sub text-sm mt-2">
                        Friendly, fast, and supportive screening
                    </p>
                </div>
            </div>
        </section>
    );
};

export default LoginScreen;
