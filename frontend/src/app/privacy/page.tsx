"use client";

import Link from "next/link";

export default function PrivacyPolicy() {
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
        <h1 className="text-3xl md:text-4xl font-bold text-wellness-dark mb-2">Privacy Policy</h1>
        <p className="text-gray-500 text-sm mb-8">Effective Date: June 2026 &mdash; POPIA Compliant</p>

        <div className="space-y-8 text-gray-700 leading-relaxed">
          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">1. Who We Are</h2>
            <p>TibbWell is a digital health and wellness platform based on Unani-Tibb (Islamic medicine) principles, owned and operated by Moulana Suhail, Johannesburg, South Africa. TibbWell provides Mizaaj (temperament) assessments and personalised wellness guidance based on traditional Tibb knowledge.</p>
            <p className="mt-2">For all privacy-related matters, contact us at: <a href="mailto:support@tibbwell.co.za" className="text-wellness-green underline">support@tibbwell.co.za</a></p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">2. What Personal Information We Collect</h2>
            <p>We collect the following categories of personal information:</p>
            <ul className="list-disc pl-6 mt-2 space-y-1">
              <li><strong>Account information:</strong> name, email address, password (encrypted)</li>
              <li><strong>Quiz responses:</strong> your answers to the 25-question Mizaaj assessment</li>
              <li><strong>Health-related data:</strong> temperament result, disease risk profile, lifestyle information derived from quiz answers</li>
              <li><strong>Payment information:</strong> subscription status (Note: actual card/banking details are processed by PayFast — we do not store payment card details)</li>
              <li><strong>Usage data:</strong> login times, chatbot interactions, pages visited</li>
            </ul>
            <p className="mt-2">In terms of the Protection of Personal Information Act 4 of 2013 (POPIA), health-related information is classified as Special Personal Information and is handled with the highest level of care and protection.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">3. Why We Collect Your Information</h2>
            <ul className="list-disc pl-6 space-y-1">
              <li>To provide your personalised Mizaaj assessment and wellness recommendations</li>
              <li>To operate and manage your TibbWell subscription</li>
              <li>To power the Ask TibbWell AI chatbot with your specific temperament profile</li>
              <li>To send transactional emails (registration confirmation, subscription confirmation, password reset)</li>
              <li>To improve the platform and content based on aggregated, anonymised usage data</li>
              <li>To comply with legal and regulatory obligations</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">4. Your Rights Under POPIA</h2>
            <p>As a data subject under POPIA, you have the following rights:</p>
            <ul className="list-disc pl-6 mt-2 space-y-1">
              <li><strong>Right to access:</strong> you may request a copy of all personal information we hold about you</li>
              <li><strong>Right to correction:</strong> you may request correction of inaccurate information</li>
              <li><strong>Right to deletion:</strong> you may request deletion of your account and personal data</li>
              <li><strong>Right to object:</strong> you may object to the processing of your personal information</li>
              <li><strong>Right to complain:</strong> you may lodge a complaint with the Information Regulator of South Africa at www.justice.gov.za/inforeg/</li>
            </ul>
            <p className="mt-2">To exercise any of these rights, email us at: <a href="mailto:support@tibbwell.co.za" className="text-wellness-green underline">support@tibbwell.co.za</a></p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">5. How We Store and Protect Your Data</h2>
            <ul className="list-disc pl-6 space-y-1">
              <li>All data is stored on secure servers hosted by Railway (backend database) and Vercel (frontend)</li>
              <li>Passwords are encrypted using industry-standard hashing and are never stored in plain text</li>
              <li>All communication between your device and TibbWell is encrypted via SSL/TLS (HTTPS)</li>
              <li>We do not sell, rent, or share your personal information with any third party for marketing purposes</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">6. Third-Party Services</h2>
            <p>TibbWell uses the following third-party services that may process your data:</p>
            <ul className="list-disc pl-6 mt-2 space-y-1">
              <li><strong>PayFast</strong> (payfast.co.za): payment processing for R99/month subscriptions — governed by PayFast&apos;s own privacy policy</li>
              <li><strong>Anthropic Claude API:</strong> powers the Ask TibbWell chatbot — your temperament profile and questions are processed to generate responses</li>
              <li><strong>Resend:</strong> transactional email delivery</li>
              <li><strong>Railway and Vercel:</strong> cloud hosting and infrastructure</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">7. Health Information Disclaimer</h2>
            <p>The information provided by TibbWell is based on traditional Unani-Tibb principles and is intended for general wellness guidance only. It does not constitute medical advice, medical diagnosis, or treatment. Always consult a qualified healthcare professional for medical concerns.</p>
            <p className="mt-2">Your Mizaaj assessment is a close estimate based on your quiz answers. For an accurate reading of your true temperament, an in-person consultation with a qualified Tibb practitioner is recommended.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">8. Data Retention</h2>
            <p>We retain your personal information for as long as your account remains active. If you delete your account, your personal data will be removed from our systems within 30 days, except where we are required by law to retain it.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">9. Children</h2>
            <p>TibbWell is not intended for use by persons under the age of 18. We do not knowingly collect personal information from children.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">10. Changes to This Policy</h2>
            <p>We may update this Privacy Policy from time to time. We will notify registered users by email of any material changes. Continued use of the platform after changes constitutes acceptance of the updated policy.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-wellness-dark mb-3">11. Contact Us</h2>
            <p>Email: <a href="mailto:support@tibbwell.co.za" className="text-wellness-green underline">support@tibbwell.co.za</a></p>
            <p>Website: <a href="https://www.tibbwell.co.za" className="text-wellness-green underline">www.tibbwell.co.za</a></p>
            <p>Location: Johannesburg, Gauteng, South Africa</p>
          </section>
        </div>
      </div>
    </div>
  );
}