"use client";
import Link from "next/link";

interface ErrorPageProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ErrorPage({ error, reset }: ErrorPageProps) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-wellness-pale to-white flex items-center justify-center">
      <div className="text-center max-w-md mx-auto px-4">
        <div className="w-20 h-20 bg-amber-500 rounded-2xl flex items-center justify-center mx-auto mb-6"><span className="text-white font-bold text-2xl">!</span></div>
        <h1 className="text-3xl font-bold text-wellness-dark mb-3">Something Went Wrong</h1>
        <p className="text-gray-600 mb-8">An unexpected error occurred. Please try again.</p>
        <div className="flex gap-4 justify-center">
          <button onClick={reset} className="bg-wellness-green text-white px-8 py-3 rounded-xl font-bold hover:bg-wellness-dark transition-all">Try Again</button>
          <Link href="/" className="border-2 border-gray-300 text-gray-700 px-8 py-3 rounded-xl font-bold hover:bg-gray-50 transition-all">Go Home</Link>
        </div>
      </div>
    </div>
  );
}