import Link from "next/link";

export default function ScreeningPage() {
    return (
        <main className="min-h-screen flex items-center justify-center px-6">
            <div className="max-w-4xl w-full">
                <h2 className="text-3xl font-bold text-center text-slate-800 mb-10">
                    Choose Screening Method
                </h2>

                <div className="grid md:grid-cols-2 gap-8">
                    {/* Voice Screening Card */}
                    <div className="bg-white rounded-2xl shadow-md p-8 text-center">
                        <h3 className="text-2xl font-semibold text-blue-600 mb-4">
                            Voice Screening
                        </h3>

                        <p className="text-gray-600 mb-6">
                            Analyze speech patterns to detect early dementia-related
                            abnormalities.
                        </p>

                        <Link href="/voice">
                            <button className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
                                Proceed to Voice Test
                            </button>
                        </Link>
                    </div>

                    {/* MRI Screening Card */}
                    <div className="bg-white rounded-2xl shadow-md p-8 text-center">
                        <h3 className="text-2xl font-semibold text-teal-600 mb-4">
                            MRI Screening
                        </h3>

                        <p className="text-gray-600 mb-6">
                            Analyze brain MRI scans to detect structural changes associated
                            with dementia.
                        </p>

                        <Link href="/mri">
                            <button className="w-full py-3 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition">
                                Proceed to MRI Test
                            </button>
                        </Link>
                    </div>
                </div>
            </div>
        </main>
    );
}
