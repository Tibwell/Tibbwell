"use client";

import Link from "next/link";
import { useState } from "react";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-md border-b border-wellness-light">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-wellness-green rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">TW</span>
            </div>
            <span className="text-xl font-bold text-wellness-dark">
              TibbWell
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6">
            <Link
              href="/#how-it-works"
              className="text-gray-600 hover:text-wellness-green transition-colors"
            >
              How It Works
            </Link>
            <Link
              href="/#features"
              className="text-gray-600 hover:text-wellness-green transition-colors"
            >
              Features
            </Link>
            <Link
              href="/#faq"
              className="text-gray-600 hover:text-wellness-green transition-colors"
            >
              FAQ
            </Link>
            <Link
              href="/login"
              className="text-gray-600 hover:text-wellness-green transition-colors"
            >
              Login
            </Link>
            <Link
              href="/register"
              className="text-gray-600 hover:text-wellness-green transition-colors"
            >
              Register
            </Link>
            <Link href="/quiz" className="btn-primary text-sm">
              Take the Free Quiz
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2 rounded-lg hover:bg-wellness-light transition-colors"
            onClick={() => setIsOpen(!isOpen)}
            aria-label="Toggle menu"
          >
            <svg
              className="w-6 h-6 text-wellness-dark"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {isOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <div className="md:hidden pb-4 animate-slide-down">
            <div className="flex flex-col gap-3">
              <Link
                href="/#how-it-works"
                className="text-gray-600 hover:text-wellness-green transition-colors py-2"
                onClick={() => setIsOpen(false)}
              >
                How It Works
              </Link>
              <Link
                href="/#features"
                className="text-gray-600 hover:text-wellness-green transition-colors py-2"
                onClick={() => setIsOpen(false)}
              >
                Features
              </Link>
              <Link
                href="/#faq"
                className="text-gray-600 hover:text-wellness-green transition-colors py-2"
                onClick={() => setIsOpen(false)}
              >
                FAQ
              </Link>
              <Link
                href="/login"
                className="text-gray-600 hover:text-wellness-green transition-colors py-2"
                onClick={() => setIsOpen(false)}
              >
                Login
              </Link>
              <Link
                href="/register"
                className="text-gray-600 hover:text-wellness-green transition-colors py-2"
                onClick={() => setIsOpen(false)}
              >
                Register
              </Link>
              <Link
                href="/quiz"
                className="btn-primary text-sm text-center"
                onClick={() => setIsOpen(false)}
              >
                Take the Free Quiz
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
