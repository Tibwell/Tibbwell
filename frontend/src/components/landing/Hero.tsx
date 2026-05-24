import Link from "next/link";

export default function Hero() {
  return (
    <section className="relative min-h-[90vh] flex items-center bg-gradient-to-br from-wellness-green via-[#1b5e3a] to-wellness-dark overflow-hidden">
      {/* Decorative circles */}
      <div className="absolute top-20 left-10 w-64 h-64 bg-white/5 rounded-full blur-3xl" />
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-white/5 rounded-full blur-3xl" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-wellness-light/10 rounded-full blur-3xl" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="max-w-3xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm text-white/90 px-4 py-2 rounded-full text-sm mb-8 animate-fade-in">
            <span className="w-2 h-2 bg-wellness-accent rounded-full animate-pulse" />
            Free Unani-Tibb Assessment
          </div>

          {/* Headline */}
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold text-white leading-tight mb-6 animate-slide-up">
            Discover Your
            <span className="block text-wellness-accent">
              Unani Temperament
            </span>
          </h1>

          {/* Subheadline */}
          <p className="text-lg sm:text-xl text-white/80 max-w-2xl mx-auto mb-10 animate-slide-up animate-delay-200">
            Take our free 25-question quiz to unlock your unique mind-body
            constitution. Get personalised health insights based on the ancient
            wisdom of Unani-Tibb.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up animate-delay-300">
            <Link
              href="/quiz"
              className="inline-flex items-center justify-center gap-2 bg-white text-wellness-green px-8 py-4 rounded-xl font-bold text-lg hover:bg-wellness-light transition-all duration-200 shadow-xl hover:shadow-2xl"
            >
              Take the Free Quiz
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
            <Link
              href="/#how-it-works"
              className="inline-flex items-center justify-center gap-2 border-2 border-white/40 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white/10 transition-all duration-200"
            >
              Learn More
            </Link>
          </div>

          {/* Social proof */}
          <div className="mt-16 flex flex-col items-center gap-4 animate-fade-in animate-delay-500">
            <div className="flex -space-x-2">
              {[1, 2, 3, 4].map((i) => (
                <div
                  key={i}
                  className="w-10 h-10 rounded-full border-2 border-white bg-wellness-accent/30 flex items-center justify-center text-white text-xs font-bold"
                >
                  {String.fromCharCode(64 + i)}
                </div>
              ))}
            </div>
            <p className="text-white/60 text-sm">
              Join{" "}
              <span className="text-white font-semibold">500+</span> people who
              discovered their temperament
            </p>
          </div>
        </div>
      </div>

      {/* Wave divider */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1440 60" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M0 60V30C240 0 480 0 720 30C960 60 1200 60 1440 30V60H0Z"
            fill="white"
          />
        </svg>
      </div>
    </section>
  );
}
