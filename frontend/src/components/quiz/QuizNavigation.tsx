"use client";

import { useState } from "react";

interface QuizNavigationProps {
  currentQuestion: number;
  totalQuestions: number;
  onNext: () => void;
  onBack: () => void;
  onSubmit: () => void;
  canGoNext: boolean;
}

export default function QuizNavigation({
  currentQuestion,
  totalQuestions,
  onNext,
  onBack,
  onSubmit,
  canGoNext,
}: QuizNavigationProps) {
  const isLastQuestion = currentQuestion === totalQuestions - 1;

  return (
    <div className="flex justify-between items-center mt-8">
      {/* Back button */}
      {currentQuestion > 0 ? (
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 text-gray-600 hover:text-wellness-green transition-colors font-medium"
        >
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
              d="M15 19l-7-7 7-7"
            />
          </svg>
          Back
        </button>
      ) : (
        <div /> /* Spacer */
      )}

      {/* Next / Submit button */}
      {isLastQuestion ? (
        <button
          onClick={onSubmit}
          disabled={!canGoNext}
          className="btn-primary inline-flex items-center gap-2"
        >
          Submit Quiz
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
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </button>
      ) : (
        <button
          onClick={onNext}
          disabled={!canGoNext}
          className="btn-primary inline-flex items-center gap-2"
        >
          Next
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
              d="M9 5l7 7-7 7"
            />
          </svg>
        </button>
      )}
    </div>
  );
}