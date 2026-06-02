"use client";

import Link from "next/link";

export default function TermsOfService() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-wellness-pale to-white">
      <header className="bg-white border-b border-wellness-light">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-wellness-green rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">TW</span>
            </div>
            <span className="text-lg font-bold text-wellness-dark">TibbWell</span>
          </Link>
          <Link href="/" className="text-sm text-wellness-green hover:text-wellness-dark transition-colors font-medium">Back to Home</Link>
        </div>
      </header>
      <div className="max-w-3xl mx-auto px-4 py-12">
        <h1 className="text-3xl md:text-4xl font-bold text-wellness-dark mb-2">Terms of Service</h1>
        <p className="text-gray-500 text-sm mb-8">Effective Date: June 2026</p>

        <div className="space-y-8 text-gray-700 leading-relaxed">
          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">1. Acceptance of Terms</h2>
            <p>By accessing or using TibbWell (the &ldquo;Platform&rdquo;), you agree to be bound by these Terms of Service. If you do not agree, please do not use the Platform. These terms are governed by the laws of the Republic of South Africa.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">2. Description of Service</h2>
            <p>TibbWell provides:</p>
            <ul className="list-disc pl-6 mt-2 space-y-1">
              <li>A free 25-question Mizaaj (temperament) assessment with basic results</li>
              <li>A premium subscription (R99/month) with a full personalised health programme including food guides, seasonal protocols, exercise plans, sleep optimisation, and emotional wellness guidance</li>
              <li>An Ask TibbWell AI chatbot for health-related questions based on your temperament</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">3. User Accounts</h2>
            <ul className="list-disc pl-6 space-y-1">
              <li>You must be 18 years or older to create an account</li>
              <li>You are responsible for maintaining the confidentiality of your login credentials</li>
              <li>You must provide accurate, current, and complete registration information</li>
              <li>You may not share your account with others</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">4. Subscriptions &amp; Payments</h2>
            <ul className="list-disc pl-6 space-y-1">
              <li>Premium subscription is R99 per month, billed via PayFast</li>
              <li>Payments are processed securely by PayFast &mdash; TibbWell does not store payment card details</li>
              <li>Your subscription renews automatically each month unless cancelled</li>
              <li>You may cancel at any time; access continues until the end of the current billing period</li>
              <li>No refunds for partial months</li>
              <li>Prices may change with 30 days&apos; email notice</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">5. Medical Disclaimer</h2>
            <p><strong>IMPORTANT:</strong> TibbWell provides general wellness information based on traditional Unani-Tibb principles. The Platform does NOT provide medical advice, diagnosis, or treatment. The content is for informational purposes only and is not a substitute for professional medical advice.</p>
            <p className="mt-2">Always consult a qualified healthcare provider with any questions regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read on TibbWell.</p>
            <p className="mt-2">If you have a medical emergency, call your doctor or emergency services immediately.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">6. Mizaaj Assessment Disclaimer</h2>
            <p>Your Mizaaj (temperament) assessment result is a close estimate based on the answers you provide. The assessment is based on traditional Unani-Tibb principles and should not be considered a definitive medical or psychological diagnosis. For an accurate reading of your true temperament, an in-person consultation with a qualified Tibb practitioner is recommended.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">7. User Conduct</h2>
            <p>You agree not to:</p>
            <ul className="list-disc pl-6 mt-2 space-y-1">
              <li>Use the Platform for any unlawful purpose</li>
              <li>Attempt to gain unauthorised access to the Platform or its systems</li>
              <li>Provide false or misleading information</li>
              <li>Use the Platform to harass, abuse, or harm others</li>
              <li>Interfere with the proper functioning of the Platform</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">8. Intellectual Property</h2>
            <p>All content on TibbWell, including the Mizaaj assessment, temperament descriptions, health protocols, and platform design, is the intellectual property of TibbWell and is protected by South African and international copyright laws. You may not reproduce, distribute, or create derivative works without our written permission.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">9. Limitation of Liability</h2>
            <p>TibbWell and its operators shall not be liable for any direct, indirect, incidental, special, or consequential damages resulting from your use of the Platform. This includes, but is not limited to, reliance on any health information obtained from the Platform.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">10. Termination</h2>
            <p>We reserve the right to suspend or terminate your account if you violate these terms. You may delete your account at any time by contacting support.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">11. Governing Law</h2>
            <p>These Terms of Service are governed by and construed in accordance with the laws of the Republic of South Africa. Any disputes shall be resolved in the courts of Johannesburg, Gauteng.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">12. Contact</h2>
            <p>Email: <a href="mailto:support@tibbwell.co.za" className="text-wellness-green underline">support@tibbwell.co.za</a></p>
            <p>Website: <a href="https://www.tibbwell.co.za" className="text-wellness-green underline">www.tibbwell.co.za</a></p>
            <p>Location: Johannesburg, Gauteng, South Africa</p>
          </section>
        </div>
      </div>
    </div>
  );
}