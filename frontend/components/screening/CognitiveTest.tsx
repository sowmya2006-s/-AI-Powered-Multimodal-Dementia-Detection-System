import React, { useState, useEffect } from 'react';
import { useScreening } from '../../context/ScreeningContext';

const audioPool = ['Apple', 'Dog', 'Boat', 'Sun', 'Chair', 'Window', 'Phone'];
const visualPool = [
    { label: 'Apple', src: 'https://placehold.co/420x260/E8F2FF/2C6DB4?text=Apple' },
    { label: 'Dog', src: 'https://placehold.co/420x260/E8F2FF/2C6DB4?text=Dog' },
    { label: 'Boat', src: 'https://placehold.co/420x260/E8F2FF/2C6DB4?text=Boat' },
    { label: 'Car', src: 'https://placehold.co/420x260/E8F2FF/2C6DB4?text=Car' },
    { label: 'Cat', src: 'https://placehold.co/420x260/E8F2FF/2C6DB4?text=Cat' },
    { label: 'Tree', src: 'https://placehold.co/420x260/E8F2FF/2C6DB4?text=Tree' }
];

const CognitiveTest: React.FC = () => {
    const { setStep, setCognitiveScore, cognitiveScores } = useScreening();
    const [testType, setTestType] = useState<'none' | 'audio' | 'visual'>('none');
    const [phase, setPhase] = useState<'start' | 'original' | 'break' | 'options' | 'complete'>('start');
    const [currentRound, setCurrentRound] = useState(1);
    const [timeLeft, setTimeLeft] = useState(0);
    const [currentData, setCurrentData] = useState<any>(null);
    const [options, setOptions] = useState<any[]>([]);
    const [score, setScore] = useState(0);

    const shuffle = (array: any[]) => {
        const arr = [...array];
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    };

    const speak = (text: string, onEnd?: () => void) => {
        if (!window.speechSynthesis) return;
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.onend = onEnd || null;
        speechSynthesis.cancel();
        speechSynthesis.speak(utterance);
    };

    const startTest = (type: 'audio' | 'visual') => {
        setTestType(type);
        setPhase('original');
        setCurrentRound(1);
        setScore(0);
        prepareRound(type, 1);
    };

    const prepareRound = (type: 'audio' | 'visual', round: number) => {
        if (type === 'audio') {
            const word = audioPool[(round - 1) % audioPool.length];
            setCurrentData(word);
        } else {
            const item = visualPool[(round - 1) % visualPool.length];
            setCurrentData(item);
        }
    };

    const handleOriginalShown = async () => {
        if (testType === 'visual') {
            await new Promise(r => setTimeout(r, 3000));
        }
        setPhase('break');
        setTimeLeft(5); // 5 seconds for demo, instead of 30
    };

    useEffect(() => {
        let timer: any;
        if (phase === 'break' && timeLeft > 0) {
            timer = setInterval(() => setTimeLeft(prev => prev - 1), 1000);
        } else if (phase === 'break' && timeLeft === 0) {
            showOptions();
        }
        return () => clearInterval(timer);
    }, [phase, timeLeft]);

    const showOptions = () => {
        setPhase('options');
        if (testType === 'audio') {
            const distractors = shuffle(audioPool.filter(w => w !== currentData)).slice(0, 2);
            const opts = shuffle([
                { value: currentData, correct: true },
                { value: distractors[0], correct: false },
                { value: distractors[1], correct: false }
            ]);
            setOptions(opts);
        } else {
            const distractors = shuffle(visualPool.filter(v => v.label !== currentData.label)).slice(0, 2);
            const opts = shuffle([
                { value: currentData, correct: true },
                { value: distractors[0], correct: false },
                { value: distractors[1], correct: false }
            ]);
            setOptions(opts);
        }
    };

    const handleSelect = (option: any) => {
        const newScore = option.correct ? score + 1 : score;
        setScore(newScore);

        if (currentRound < 3) {
            const nextRound = currentRound + 1;
            setCurrentRound(nextRound);
            setPhase('original');
            prepareRound(testType as 'audio' | 'visual', nextRound);
        } else {
            setPhase('complete');
            setCognitiveScore(testType as 'audio' | 'visual', newScore);
        }
    };

    return (
        <section className="bg-card rounded-radius shadow-shadow p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Step 2: Cognitive Test</h2>

            {phase === 'start' && (
                <>
                    <p className="text-sub text-sm mb-6">
                        Choose one test to start. Each test repeats the sequence 3 times: original → 30s blank break → options.
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                        <div className={`p-5 rounded-xl border transition-all cursor-pointer ${cognitiveScores.audio > 0 ? 'border-green-100 bg-green-50/30' : 'border-blue-50 bg-white hover:border-primary/30'
                            }`} onClick={() => startTest('audio')}>
                            <div className="font-bold text-gray-800 mb-2">Audio Memory Test</div>
                            <div className="text-xs text-sub leading-relaxed mb-4">
                                Listen to a word, wait for a break, then select the matching clip from options.
                            </div>
                            <button className="px-4 py-2 rounded-lg bg-primary text-white text-xs font-bold hover:bg-primary-600 transition-colors">
                                {cognitiveScores.audio > 0 ? 'Retake Audio Test' : 'Start Audio Test'}
                            </button>
                        </div>

                        <div className={`p-5 rounded-xl border transition-all cursor-pointer ${cognitiveScores.visual > 0 ? 'border-green-100 bg-green-50/30' : 'border-blue-50 bg-white hover:border-primary/30'
                            }`} onClick={() => startTest('visual')}>
                            <div className="font-bold text-gray-800 mb-2">Visual Memory Test</div>
                            <div className="text-xs text-sub leading-relaxed mb-4">
                                Observe a picture, wait for a break, then identify the original from options.
                            </div>
                            <button className="px-4 py-2 rounded-lg bg-primary text-white text-xs font-bold hover:bg-primary-600 transition-colors">
                                {cognitiveScores.visual > 0 ? 'Retake Visual Test' : 'Start Visual Test'}
                            </button>
                        </div>
                    </div>
                </>
            )}

            {phase === 'original' && (
                <div className="text-center py-10">
                    <h3 className="text-lg font-bold text-gray-700 mb-6">Round {currentRound} — {testType === 'audio' ? 'Audio' : 'Visual'} Memory</h3>
                    <div className="max-w-md mx-auto p-8 rounded-2xl bg-soft border border-blue-100 shadow-sm">
                        {testType === 'audio' ? (
                            <div className="space-y-4">
                                <div className="text-sm font-medium text-blue-600 italic">Play the original word (click to play)</div>
                                <button
                                    onClick={() => speak(currentData, handleOriginalShown)}
                                    className="w-16 h-16 rounded-full bg-primary text-white text-xl flex items-center justify-center mx-auto hover:bg-primary-600 transition-transform active:scale-95 shadow-lg"
                                >
                                    <i className="fas fa-play ml-1"></i>
                                </button>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                <img src={currentData.src} alt="Original" className="rounded-xl mx-auto max-h-48 shadow-md" onLoad={handleOriginalShown} />
                                <div className="text-xs text-sub italic">Observe this image carefully.</div>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {phase === 'break' && (
                <div className="flex items-center justify-center h-64 bg-white border border-gray-50 rounded-xl mt-4 shadow-inner">
                    <div className="text-3xl font-black text-gray-300 tracking-widest uppercase">
                        Recall Break — {timeLeft}s
                    </div>
                </div>
            )}

            {phase === 'options' && (
                <div className="py-6">
                    <h3 className="text-lg font-bold text-gray-700 mb-4">Round {currentRound} — Choose the Match</h3>
                    <p className="text-sub text-sm mb-6">Which of these was the original?</p>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        {options.map((opt, i) => (
                            <div
                                key={i}
                                onClick={() => handleSelect(opt)}
                                className="group p-3 rounded-xl bg-soft border-2 border-transparent hover:border-primary hover:shadow-md transition-all cursor-pointer"
                            >
                                {testType === 'audio' ? (
                                    <div className="text-center space-y-3 p-3">
                                        <button
                                            onClick={(e) => { e.stopPropagation(); speak(opt.value); }}
                                            className="w-12 h-12 rounded-full bg-white text-primary flex items-center justify-center mx-auto shadow-sm group-hover:bg-primary group-hover:text-white transition-colors"
                                        >
                                            <i className="fas fa-play ml-0.5"></i>
                                        </button>
                                        <div className="text-xs font-bold text-sub">Clip {i + 1}</div>
                                    </div>
                                ) : (
                                    <img src={opt.value.src} alt={`Option ${i + 1}`} className="rounded-lg w-full h-32 object-cover shadow-sm group-hover:shadow-inner" />
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {phase === 'complete' && (
                <div className="text-center py-10">
                    <div className="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-3xl mx-auto mb-4 animate-bounce">
                        <i className="fas fa-check"></i>
                    </div>
                    <h3 className="text-xl font-bold text-gray-800 mb-2">
                        {testType === 'audio' ? 'Audio' : 'Visual'} Test Complete!
                    </h3>
                    <p className="text-sub text-sm mb-8">
                        Your score: <span className="font-bold text-primary">{score}/3</span>
                    </p>
                    <div className="flex gap-3 justify-center">
                        <button
                            onClick={() => { setPhase('start'); setTestType('none'); }}
                            className="px-6 py-2.5 rounded-xl border border-primary text-primary font-bold text-sm hover:bg-soft transition-colors"
                        >
                            Take Another Test
                        </button>
                        <button
                            onClick={() => setStep(5)}
                            className="px-8 py-2.5 rounded-xl bg-primary text-white font-bold text-sm hover:bg-primary-600 transition-colors shadow-sm"
                        >
                            Proceed to MRI Analysis
                        </button>
                    </div>
                </div>
            )}

            <div className="mt-8 pt-6 border-t border-gray-50">
                <button
                    onClick={() => setStep(3)}
                    className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl border border-dashed border-gray-200 text-sub font-semibold text-sm hover:bg-gray-50 transition-colors"
                >
                    Back
                </button>
            </div>
        </section>
    );
};

export default CognitiveTest;
