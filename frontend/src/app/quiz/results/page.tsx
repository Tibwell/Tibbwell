"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

interface QuizResult {
  dominant_temperament: string;
  sub_dominant_temperament: string;
  combination: string;
  description: string;
  dominant_quality: string;
  quality_explanation: string;
  foods_to_eat: string[];
  foods_to_avoid: string[];
  disease_risks: string[];
  seasonal_tip: string;
}

export default function ResultsPage() {
  const router = useRouter();
  const [result, setResult] = useState<QuizResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = sessionStorage.getItem("tibbwell_results");
    if (stored) {
      setResult(JSON.parse(stored));
      setLoading(false);
    } else {
      // No results found — redirect to quiz
      router.push("/quiz");
    }
  }, [router]);

  const handleShare = (platform: string) => {
    const text = `I discovered my Unani temperament: ${result?.combination}! Take the free quiz at TibbWell 🌿`;
    const url = "https://tibbwell.com/quiz";

    switch (platform) {
      case "whatsapp":
        window.open(
          `https://wa.me/?text=${encodeURIComponent(text + " " + url)}`,
          "_blank"
        );
        break;
      case "facebook":
        window.open(
          `https://www.facebook.com/sharer/sharer.php?quote=${encodeURIComponent(
            text
          )}&u=${encodeURIComponent(url)}`,
          "_blank"
        );
        break;
      case "twitter":
        window.open(
          `https://twitter.com/intent/tweet?text=${encodeURIComponent(
            text + " " + url
          )}`,
          "_blank"
        );
        break;
    }
  };

  if (loading || !result) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-wellness-pale to-white flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-wellness-light border-t-wellness-green rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading your results...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-wellness-pale to-white">
      {/* Header */}
      <header className="bg-white border-b border-wellness-light">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-wellness-green rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">TW</span>
            </div>
            <span className="text-lg font-bold text-wellness-dark">
              TibbWell
            </span>
          </Link>
          <Link
            href="/quiz"
            className="text-sm text-wellness-green hover:text-wellness-dark transition-colors font-medium"
          >
            Retake Quiz
          </Link>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Hero Result */}
        <div className="text-center mb-12 animate-fade-in">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 bg-wellness-light text-wellness-green px-4 py-2 rounded-full text-sm font-semibold mb-6">
            <span className="w-2 h-2 bg-wellness-green rounded-full" />
            Your Temperament Result
          </div>

          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-wellness-dark mb-4">
            {result.combination}
          </h1>

          <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
            {result.description}
          </p>
        </div>

        {/* Quality Section */}
        <div className="bg-white rounded-2xl shadow-md p-8 mb-8 animate-slide-up">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-xl bg-wellness-light text-wellness-green flex items-center justify-center">
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <div>
              <h2 className="text-xl font-bold text-wellness-dark">
                Dominant Quality
              </h2>
              <p className="text-sm text-gray-500">
                What governs your constitution
              </p>
            </div>
          </div>
          <div className="bg-wellness-pale rounded-xl p-6">
            <span className="inline-block bg-wellness-green text-white font-bold px-4 py-1 rounded-full text-sm mb-3">
              {result.dominant_quality}
            </span>
            <p className="text-gray-700 leading-relaxed">
              {result.quality_explanation}
            </p>
          </div>
        </div>

        {/* Two Column Layout */}
        <div className="grid md:grid-cols-2 gap-8 mb-8">
          {/* Foods to Eat */}
          <div className="bg-white rounded-2xl shadow-md p-8 animate-slide-up">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-xl bg-green-100 text-green-600 flex items-center justify-center">
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h2 className="text-xl font-bold text-wellness-dark">
                Foods to Eat
              </h2>
            </div>
            <ul className="space-y-3">
              {result.foods_to_eat.map((food, index) => (
                <li
                  key={index}
                  className="flex items-start gap-3 text-gray-700"
                >
                  <span className="w-6 h-6 rounded-full bg-green-100 text-green-600 flex items-center justify-center flex-shrink-0 text-sm font-bold">
                    {index + 1}
                  </span>
                  {food}
                </li>
              ))}
            </ul>
          </div>

          {/* Foods to Avoid */}
          <div className="bg-white rounded-2xl shadow-md p-8 animate-slide-up">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-xl bg-red-100 text-red-600 flex items-center justify-center">
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h2 className="text-xl font-bold text-wellness-dark">
                Foods to Avoid
              </h2>
            </div>
            <ul className="space-y-3">
              {result.foods_to_avoid.map((food, index) => (
                <li
                  key={index}
                  className="flex items-start gap-3 text-gray-700"
                >
                  <span className="w-6 h-6 rounded-full bg-red-100 text-red-600 flex items-center justify-center flex-shrink-0 text-sm font-bold">
                    {index + 1}
                  </span>
                  {food}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Disease Risks */}
        <div className="bg-white rounded-2xl shadow-md p-8 mb-8 animate-slide-up">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 rounded-xl bg-yellow-100 text-yellow-600 flex items-center justify-center">
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
                />
              </svg>
            </div>
            <h2 className="text-xl font-bold text-wellness-dark">
              Health Awareness
            </h2>
          </div>
          <p className="text-gray-500 text-sm mb-4">
            Based on your temperament, here are areas to be mindful of:
          </p>
          <ul className="grid sm:grid-cols-2 gap-3">
            {result.disease_risks.map((risk, index) => (
              <li
                key={index}
                className="flex items-start gap-3 text-gray-700 bg-gray-50 rounded-xl p-4"
              >
                <span className="w-2 h-2 bg-yellow-500 rounded-full mt-2 flex-shrink-0" />
                {risk}
              </li>
            ))}
          </ul>
        </div>

        {/* Seasonal Tip */}
        <div className="bg-gradient-to-r from-wellness-green to-wellness-dark rounded-2xl p-8 mb-8 text-white animate-slide-up">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center">
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
                />
              </svg>
            </div>
            <div>
              <h2 className="text-xl font-bold">Seasonal Tip</h2>
              <p className="text-white/70 text-sm">
                Advice for the current season
              </p>
            </div>
          </div>
          <p className="text-white/90 leading-relaxed">{result.seasonal_tip}</p>
        </div>

        {/* Share Section */}
        <div className="bg-white rounded-2xl shadow-md p-8 mb-8">
          <div className="text-center mb-6">
            <h2 className="text-xl font-bold text-wellness-dark mb-2">
              Share Your Result
            </h2>
            <p className="text-gray-500 text-sm">
              Let your friends discover their temperament too!
            </p>
          </div>
          <div className="flex justify-center gap-4">
            <button
              onClick={() => handleShare("whatsapp")}
              className="flex items-center gap-2 bg-green-500 text-white px-6 py-3 rounded-xl font-medium hover:bg-green-600 transition-all"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
              </svg>
              WhatsApp
            </button>
            <button
              onClick={() => handleShare("facebook")}
              className="flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-xl font-medium hover:bg-blue-700 transition-all"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
              </svg>
              Facebook
            </button>
            <button
              onClick={() => handleShare("twitter")}
              className="flex items-center gap-2 bg-gray-900 text-white px-6 py-3 rounded-xl font-medium hover:bg-gray-800 transition-all"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
              </svg>
              X
            </button>
          </div>
        </div>

        {/* Premium Preview Card */}
        <div className="bg-gradient-to-br from-wellness-green to-wellness-dark rounded-2xl p-8 md:p-12 text-white text-center animate-slide-up relative overflow-hidden">
          {/* Decorative */}
          <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2" />

          <div className="relative">
            <div className="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <svg
                className="w-8 h-8"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                />
              </svg>
            </div>
            <h3 className="text-2xl md:text-3xl font-bold mb-3">
              Unlock Your Complete Health Programme
            </h3>
            <p className="text-white/80 mb-2 max-w-lg mx-auto">
              Get your full personalised plan including monthly food guides,
              exercise protocols, sleep optimisation, and more.
            </p>
            <p className="text-wellness-accent font-bold text-xl mb-6">
              R99/month
            </p>
            <Link
              href="/#features"
              className="inline-flex items-center gap-2 bg-white text-wellness-green px-8 py-4 rounded-xl font-bold text-lg hover:bg-wellness-light transition-all"
            >
              Learn More About Premium
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 7l5 5m0 0l-5 5m5-5H6"
                />
              </svg>
            </Link>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8">
          <p className="text-gray-400 text-sm">
            Based on the ancient wisdom of Unani-Tibb medicine
          </p>
        </div>
      </div>
    </div>
  );
}