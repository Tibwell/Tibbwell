"use client";

import { useState } from "react";

const faqs = [
  {
    question: "What is Unani-Tibb?",
    answer:
      "Unani-Tibb is an ancient system of medicine based on the teachings of Hippocrates and Galen. It focuses on the four humours (blood, phlegm, yellow bile, black bile) and four qualities (heat, cold, moisture, dryness) that make up your unique temperament. TibbWell modernises this wisdom into a practical wellness programme.",
  },
  {
    question: "How does the temperament quiz work?",
    answer:
      "The quiz consists of 25 multiple-choice questions about your physical traits, emotional patterns, preferences, and tendencies. Each answer is scored against the four temperaments. Your highest and second-highest scores determine your unique temperament combination (e.g., Sanguinous-Bilious).",
  },
  {
    question: "Is the quiz really free?",
    answer:
      "Yes! The 25-question temperament quiz is completely free. You'll receive your temperament combination, description, dominant quality explanation, foods to eat/avoid, disease risks, and a seasonal tip at no cost. The premium health programme with full monthly protocols is available for R99/month.",
  },
  {
    question: "What do I get with the premium subscription?",
    answer:
      "For R99/month, you unlock your complete personalised TibbWell Health Programme including: a full food guide, monthly seasonal protocols, personalised exercise plan, sleep optimisation routine, emotional wellness practices, and disease prevention guidance — all tailored to your unique temperament combination.",
  },
  {
    question: "How often is the content updated?",
    answer:
      "Your health programme updates monthly with new seasonal protocols and health focus areas. Each month brings fresh content aligned with the changing seasons and your temperament needs, ensuring your wellness journey stays relevant throughout the year.",
  },
  {
    question: "Can I cancel my subscription?",
    answer:
      "Absolutely. You can cancel your premium subscription at any time. Your access will continue until the end of your current billing period. There are no long-term contracts or cancellation fees.",
  },
];

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <section id="faq" className="py-20 bg-white">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="section-heading">Frequently Asked Questions</h2>
          <p className="section-subheading">
            Everything you need to know about TibbWell and the temperament quiz
          </p>
        </div>

        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <div
              key={index}
              className="border border-gray-200 rounded-xl overflow-hidden"
            >
              <button
                className="accordion-trigger px-6"
                onClick={() => toggleFAQ(index)}
                aria-expanded={openIndex === index}
              >
                <span className="pr-4">{faq.question}</span>
                <svg
                  className={`w-5 h-5 text-wellness-green flex-shrink-0 transition-transform duration-300 ${
                    openIndex === index ? "rotate-180" : ""
                  }`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </button>
              <div
                className={`accordion-content ${
                  openIndex === index ? "max-h-96" : "max-h-0"
                }`}
              >
                <div className="px-6 pb-4 text-gray-600 leading-relaxed">
                  {faq.answer}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}