import React from 'react';

const Header: React.FC = () => {
    return (
        <header className="flex justify-between items-center px-2 py-3">
            <div className="flex items-center gap-3 text-primary group transition-all">
                <div className="w-10 h-10 rounded-xl bg-primary text-white flex items-center justify-center shadow-lg transform rotate-3 group-hover:rotate-0 transition-transform">
                    <i className="fas fa-brain text-xl"></i>
                </div>
                <div>
                    <h1 className="text-xl font-black tracking-tight leading-none text-gray-800">
                        NeuroScreen <span className="text-primary italic font-extrabold">AI</span>
                    </h1>
                    <div className="text-[11px] font-bold text-sub mt-1 uppercase tracking-tighter opacity-70">
                        Multimodal Dementia Screening — Supportive & Non-Diagnostic
                    </div>
                </div>
            </div>
            <div className="hidden sm:block text-right">
                <div className="text-[10px] font-bold text-primary uppercase tracking-widest bg-soft px-3 py-1 rounded-full inline-block">
                    Soft Blue Theme • v1.0
                </div>
            </div>
        </header>
    );
};

export default Header;
