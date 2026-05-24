import Link from "next/link";

const steps = [
  {
    number: "01",
    title: "Take the Quiz",
    description:
      "Answer 25 thoughtfully crafted questions about your physical, mental, and emotional tendencies.",
    icon: (
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
          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
    ),
  },
  {
    number: "02",
    title: "Get Your Results",
    description:
      "Receive your unique temperament combination — like Sanguinous-Bilious — with a full breakdown.",
    icon: (
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
          d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
        />
      </svg>
    ),
  },
  {
    number: "03",
    title: "Unlock Your Health Programme",
    description:
      "Subscribe to access your complete personalised plan: food guide, exercise, sleep & more — updated monthly.",
    icon: (
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
          d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"
        />
      </svg>
    ),
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="py-20 bg-wellness-pale">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="section-heading">How It Works</h2>
          <p className="section-subheading">
            Three simple steps to unlock a healthier, more balanced you
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 relative">
          {/* Connecting line (desktop) */}
          <div className="hidden md:block absolute top-1/2 left-[16%] right-[16%] h-0.5 bg-wellness-accent/50 -translate-y-1/2" />

          {steps.map((step, index) => (
            <div
              key={step.number}
              className="relative bg-white rounded-2xl p-8 shadow-md hover:shadow-lg transition-all duration-300 text-center group"
            >
              {/* Number badge */}
              <div className="w-16 h-16 rounded-2xl bg-wellness-light text-wellness-green flex items-center justify-center mx-auto mb-6 group-hover:bg-wellness-green group-hover:text-white transition-all duration-300">
                {step.icon}
              </div>

              {/* Step number */}
              <span className="text-wellness-accent font-bold text-sm tracking-widest uppercase">
                Step {step.number}
              </span>

              <h3 className="text-xl font-bold text-wellness-dark mt-2 mb-3">
                {step.title}
              </h3>

              <p className="text-gray-600">{step.description}</p>
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <Link href="/quiz" className="btn-primary text-lg inline-flex items-center gap-2">
            Start Your Journey
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
    </section>
  );
}
