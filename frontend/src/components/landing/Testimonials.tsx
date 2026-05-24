const testimonials = [
  {
    name: "Sarah M.",
    role: "Wellness Enthusiast",
    avatar: "SM",
    text: "The temperament quiz was eye-opening! I finally understand why certain foods work for me and others don't.",
    comingSoon: true,
  },
  {
    name: "James K.",
    role: "Health Coach",
    avatar: "JK",
    text: "TibbWell's approach to personalised health is brilliant. My clients love the practical monthly protocols.",
    comingSoon: true,
  },
  {
    name: "Amina D.",
    role: "Yoga Practitioner",
    avatar: "AD",
    text: "Knowing my Sanguinous-Phlegmatic combination has transformed my wellness journey. Highly recommend!",
    comingSoon: true,
  },
];

export default function Testimonials() {
  return (
    <section className="py-20 bg-wellness-pale">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="section-heading">What Our Users Say</h2>
          <p className="section-subheading">
            Join hundreds of people who have transformed their health with
            TibbWell
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((testimonial) => (
            <div
              key={testimonial.name}
              className="bg-white rounded-2xl p-8 shadow-md relative"
            >
              {/* Coming Soon badge */}
              <div className="absolute top-4 right-4 bg-wellness-light text-wellness-green text-xs font-semibold px-3 py-1 rounded-full">
                Coming Soon
              </div>

              {/* Avatar */}
              <div className="flex items-center gap-4 mb-6">
                <div className="w-14 h-14 rounded-full bg-gradient-to-br from-wellness-green to-wellness-accent flex items-center justify-center text-white font-bold text-lg">
                  {testimonial.avatar}
                </div>
                <div>
                  <h4 className="font-semibold text-wellness-dark">
                    {testimonial.name}
                  </h4>
                  <p className="text-sm text-gray-500">{testimonial.role}</p>
                </div>
              </div>

              {/* Quote */}
              <p className="text-gray-600 italic leading-relaxed">
                &ldquo;{testimonial.text}&rdquo;
              </p>

              {/* Stars placeholder */}
              <div className="flex gap-1 mt-4">
                {[1, 2, 3, 4, 5].map((star) => (
                  <svg
                    key={star}
                    className="w-4 h-4 text-wellness-accent"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}