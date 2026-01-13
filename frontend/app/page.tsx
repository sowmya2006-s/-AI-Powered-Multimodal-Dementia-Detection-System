import Link from "next/link";

export default function Home() {
    return (
        <main className="min-h-screen flex items-center justify-center">
            <div className="bg-white shadow-xl rounded-2xl p-10 max-w-xl text-center">
                <h1 className="text-3xl font-bold text-blue-600 mb-4">
                    AI-Powered Dementia Screening
                </h1>

                <p className="text-gray-600 mb-8">
                    Early dementia risk screening using voice analysis and MRI-based
                    artificial intelligence.
                </p>

                <Link href="/screening">
                    <button className="px-8 py-3 bg-blue-600 text-white rounded-lg text-lg hover:bg-blue-700 transition">
                        Start Screening
                    </button>
                </Link>
            </div>
        </main>
    );
}
