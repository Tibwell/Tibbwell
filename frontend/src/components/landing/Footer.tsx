import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-wellness-dark text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-wellness-accent rounded-lg flex items-center justify-center">
                <span className="text-wellness-dark font-bold text-sm">TW</span>
              </div>
              <span className="text-xl font-bold">TibbWell</span>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              Discover your Unani temperament and unlock a healthier, more
              balanced life with personalised wellness guidance.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/#how-it-works"
                  className="text-gray-400 hover:text-wellness-accent transition-colors text-sm"
                >
                  How It Works
                </Link>
              </li>
              <li>
                <Link
                  href="/#features"
                  className="text-gray-400 hover:text-wellness-accent transition-colors text-sm"
                >
                  Features
                </Link>
              </li>
              <li>
                <Link
                  href="/#faq"
                  className="text-gray-400 hover:text-wellness-accent transition-colors text-sm"
                >
                  FAQ
                </Link>
              </li>
              <li>
                <Link
                  href="/quiz"
                  className="text-gray-400 hover:text-wellness-accent transition-colors text-sm"
                >
                  Take the Quiz
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact / Social */}
          <div>
            <h3 className="font-semibold mb-4">Connect With Us</h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li className="flex items-center gap-2">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                </svg>
                <span>hello@tibbwell.com</span>
              </li>
              <li className="flex items-center gap-2">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
                    clipRule="evenodd"
                  />
                </svg>
                <span>Cape Town, South Africa</span>
              </li>
            </ul>
            <div className="flex gap-3 mt-4">
              {["WhatsApp", "Facebook", "Instagram", "Twitter"].map(
                (platform) => (
                  <span
                    key={platform}
                    className="w-9 h-9 rounded-full bg-white/10 flex items-center justify-center text-gray-400 hover:bg-wellness-accent hover:text-wellness-dark transition-all cursor-pointer text-xs font-medium"
                  >
                    {platform.slice(0, 2)}
                  </span>
                )
              )}
            </div>
          </div>
        </div>

        <div className="border-t border-white/10 mt-8 pt-8 text-center text-gray-500 text-sm">
          <p>&copy; {new Date().getFullYear()} TibbWell. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}