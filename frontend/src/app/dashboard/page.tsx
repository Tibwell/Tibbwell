"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { MOCK_DASHBOARD_DATA, PremiumDashboardData, FoodItem } from "@/lib/dashboard";
import { authApi } from "@/lib/api";

function SectionCard({
  id,
  title,
  icon,
  children,
}: {
  id?: string;
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <section
      id={id}
      className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden scroll-mt-24"
    >
      <div className="flex items-center gap-3 px-6 py-5 border-b border-gray-100 bg-gray-50/50">
        <div className="w-10 h-10 rounded-xl bg-wellness-light text-wellness-green flex items-center justify-center">
          {icon}
        </div>
        <h2 className="text-lg font-bold text-wellness-dark">{title}</h2>
      </div>
      <div className="p-6">{children}</div>
    </section>
  );
}

function FoodList({ items, color }: { items: FoodItem[]; color: "green" | "red" }) {
  const borderColors = { green: "border-l-green-500 bg-green-50/50", red: "border-l-red-500 bg-red-50/50" };
  const dotColors = { green: "bg-green-500", red: "bg-red-500" };
  const labelColors = { green: "text-green-700", red: "text-red-600" };

  return (
    <ul className="space-y-4">
      {items.map((item, i) => (
        <li
          key={i}
          className={`border-l-4 ${borderColors[color]} rounded-r-xl p-4`}
        >
          <p className={`font-medium text-sm ${labelColors[color]} mb-1`}>
            <span className={`w-2 h-2 rounded-full inline-block mr-2 ${dotColors[color]}`} />
            {item.name}
          </p>
          <p className="text-xs text-gray-500 ml-4 leading-relaxed">{item.why}</p>
        </li>
      ))}
    </ul>
  );
}

function SeasonTab({
  season,
  data,
}: {
  season: string;
  data: { description: string; recommendations: string[] };
}) {
  return (
    <div className="space-y-3">
      <p className="text-sm text-gray-700 leading-relaxed">{data.description}</p>
      <ul className="space-y-1.5">
        {data.recommendations.map((rec, i) => (
          <li key={i} className="flex items-start gap-2 text-sm text-gray-600">
            <span className="w-1.5 h-1.5 bg-wellness-green rounded-full mt-1.5 flex-shrink-0" />
            {rec}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function DashboardPage() {
  const [data, setData] = useState<PremiumDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [hasToken, setHasToken] = useState(false);
  // Determine Southern Hemisphere season from current month
  // Dec/Jan/Feb = Summer, Mar/Apr/May = Autumn, Jun/Jul/Aug = Winter, Sep/Oct/Nov = Spring
  const getCurrentSeason = () => {
    const month = new Date().getMonth();
    if (month >= 8 && month <= 10) return "spring";
    if (month >= 2 && month <= 4) return "autumn";
    if (month >= 5 && month <= 7) return "winter";
    return "summer"; // months 11, 0, 1
  };
  const [activeSeason, setActiveSeason] = useState(getCurrentSeason);

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("tibbwell_token") : null;
    setHasToken(!!token);

    const timer = setTimeout(() => {
      setData(MOCK_DASHBOARD_DATA);
      setLoading(false);
    }, 500);
    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-wellness-light border-t-wellness-green rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-500 text-sm">Loading your health programme...</p>
        </div>
      </div>
    );
  }

  if (!hasToken) {
    return (
      <div className="text-center py-20 max-w-md mx-auto">
        <div className="w-16 h-16 bg-wellness-light rounded-2xl flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8 text-wellness-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <h2 className="text-xl font-bold text-wellness-dark mb-2">Premium Dashboard</h2>
        <p className="text-gray-500 text-sm mb-6">Please log in or register to access your personalised health programme.</p>
        <div className="flex gap-3 justify-center">
          <Link href="/quiz" className="btn-secondary text-sm">Take the Quiz First</Link>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-20">
        <p className="text-gray-500">Unable to load dashboard data.</p>
      </div>
    );
  }

  const seasons = [
    { key: "summer", label: "Summer" },
    { key: "autumn", label: "Autumn" },
    { key: "winter", label: "Winter" },
    { key: "spring", label: "Spring" },
  ] as const;

  const seasonData = {
    summer: data.seasonal_protocol.summer,
    autumn: data.seasonal_protocol.autumn,
    winter: data.seasonal_protocol.winter,
    spring: data.seasonal_protocol.spring,
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-br from-wellness-green to-wellness-dark rounded-2xl p-6 md:p-8 text-white relative overflow-hidden">
        <div className="absolute top-0 right-0 w-48 h-48 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-32 h-32 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2" />

        <div className="relative">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-bold">Welcome back, {data.user.name}</h1>
              <p className="text-white/70 text-sm">Your personalised health programme is ready</p>
            </div>
            <span className="ml-auto inline-flex items-center gap-1.5 bg-white/20 text-white text-xs font-semibold px-3 py-1.5 rounded-full backdrop-blur-sm">
              <span className="w-1.5 h-1.5 bg-green-300 rounded-full" />
              Premium Active
            </span>
          </div>

          <div className="flex flex-wrap gap-3 mt-4">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl px-4 py-2.5">
              <p className="text-[10px] text-white/60 uppercase tracking-wider">Temperament</p>
              <p className="font-semibold text-sm">{data.temperament.combination}</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl px-4 py-2.5">
              <p className="text-[10px] text-white/60 uppercase tracking-wider">Quality</p>
              <p className="font-semibold text-sm">{data.temperament.quality}</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl px-4 py-2.5">
              <p className="text-[10px] text-white/60 uppercase tracking-wider">Current Focus</p>
              <p className="font-semibold text-sm">{data.monthly_focus.month} {data.monthly_focus.year}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Monthly Focus */}
      <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-2xl p-6">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-xl bg-amber-100 text-amber-600 flex items-center justify-center flex-shrink-0">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-semibold text-amber-600 bg-amber-100 px-2 py-0.5 rounded-full">Monthly Focus</span>
              <span className="text-xs text-gray-400">{data.monthly_focus.month} {data.monthly_focus.year}</span>
            </div>
            <h3 className="text-lg font-bold text-gray-800 mb-1">{data.monthly_focus.title}</h3>
            <p className="text-gray-600 text-sm leading-relaxed">{data.monthly_focus.content}</p>
            {data.monthly_focus.tip && (
              <div className="mt-3 bg-amber-100/70 rounded-lg p-3">
                <p className="text-xs font-semibold text-amber-700 mb-0.5">💡 Tip of the Month</p>
                <p className="text-sm text-amber-800">{data.monthly_focus.tip}</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <Link href="/dashboard/ask" className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 hover:shadow-md hover:border-wellness-light transition-all text-center group">
          <div className="w-10 h-10 rounded-xl bg-wellness-light text-wellness-green flex items-center justify-center mx-auto mb-2 group-hover:bg-wellness-green group-hover:text-white transition-all">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <span className="text-xs font-medium text-gray-600">Ask TibbWell AI</span>
        </Link>

        <button onClick={() => document.getElementById("food-guide")?.scrollIntoView({ behavior: "smooth" })}
          className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 hover:shadow-md hover:border-wellness-light transition-all text-center group">
          <div className="w-10 h-10 rounded-xl bg-green-50 text-green-600 flex items-center justify-center mx-auto mb-2 group-hover:bg-green-600 group-hover:text-white transition-all">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </div>
          <span className="text-xs font-medium text-gray-600">Food Guide</span>
        </button>

        <button onClick={() => window.print()} className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 hover:shadow-md hover:border-wellness-light transition-all text-center group">
          <div className="w-10 h-10 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center mx-auto mb-2 group-hover:bg-purple-600 group-hover:text-white transition-all">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
          </div>
          <span className="text-xs font-medium text-gray-600">Download PDF</span>
        </button>

        <a href={data.full_programme_url || "#"} className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 hover:shadow-md hover:border-wellness-light transition-all text-center group">
          <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center mx-auto mb-2 group-hover:bg-blue-600 group-hover:text-white transition-all">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </div>
          <span className="text-xs font-medium text-gray-600">Full Programme</span>
        </a>
      </div>

      {/* Food Guide */}
      <SectionCard id="food-guide" title="Personalised Food & Drink Guide" icon={
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
      }>
        <div className="grid md:grid-cols-2 gap-8 mb-6">
          <div>
            <h3 className="font-semibold text-green-700 mb-4 flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Foods to Eat
            </h3>
            <FoodList items={data.food_guide.foods_to_eat} color="green" />
          </div>
          <div>
            <h3 className="font-semibold text-red-600 mb-4 flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Foods to Avoid
            </h3>
            <FoodList items={data.food_guide.foods_to_avoid} color="red" />
          </div>
        </div>

        <div className="grid sm:grid-cols-3 gap-4 mb-4">
          <div className="bg-wellness-pale rounded-xl p-4">
            <h4 className="font-semibold text-wellness-dark text-sm mb-2">🍳 Best Cooking Methods</h4>
            <ul className="space-y-1">
              {data.food_guide.cooking_methods.map((m, i) => (
                <li key={i} className="text-xs text-gray-600 flex items-start gap-1.5">
                  <span className="text-wellness-green mt-0.5">•</span> {m}
                </li>
              ))}
            </ul>
          </div>
          <div className="bg-wellness-pale rounded-xl p-4">
            <h4 className="font-semibold text-wellness-dark text-sm mb-2">⏰ Meal Timing</h4>
            <p className="text-xs text-gray-600 leading-relaxed">{data.food_guide.meal_timing}</p>
          </div>
          <div className="bg-wellness-pale rounded-xl p-4">
            <h4 className="font-semibold text-wellness-dark text-sm mb-2">💧 Water Intake</h4>
            <p className="text-xs text-gray-600 leading-relaxed">{data.food_guide.water_intake}</p>
          </div>
        </div>

        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
          <h4 className="font-semibold text-amber-700 text-sm mb-2">💡 Pro Tips</h4>
          <ul className="space-y-1">
            {data.food_guide.tips.map((tip, i) => (
              <li key={i} className="text-xs text-amber-800 flex items-start gap-1.5">
                <span className="mt-0.5">•</span> {tip}
              </li>
            ))}
          </ul>
        </div>
      </SectionCard>

      {/* Seasonal Protocol */}
      <SectionCard id="seasonal" title="Full Seasonal Protocol" icon={
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      }>
        {/* Season Tabs */}
        <div className="flex gap-1 mb-6 bg-gray-100 rounded-xl p-1 overflow-x-auto">
          {seasons.map((s) => (
            <button
              key={s.key}
              onClick={() => setActiveSeason(s.key)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${
                activeSeason === s.key
                  ? "bg-white text-wellness-green shadow-sm"
                  : "text-gray-500 hover:text-wellness-green"
              }`}
            >
              {s.label}
            </button>
          ))}
        </div>

        <SeasonTab season={activeSeason} data={seasonData[activeSeason as keyof typeof seasonData]} />
      </SectionCard>

      {/* Exercise Plan */}
      <SectionCard id="exercise" title="Complete Exercise Programme" icon={
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      }>
        <div className="grid md:grid-cols-2 gap-6 mb-4">
          <div>
            <h3 className="font-semibold text-green-700 text-sm mb-3">✅ Recommended Activities</h3>
            <ul className="space-y-2">
              {data.exercise_plan.recommended.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                  <span className="w-1.5 h-1.5 bg-green-500 rounded-full mt-1.5 flex-shrink-0" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="font-semibold text-red-600 text-sm mb-3">❌ What to Avoid</h3>
            <ul className="space-y-2">
              {data.exercise_plan.avoid.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                  <span className="w-1.5 h-1.5 bg-red-500 rounded-full mt-1.5 flex-shrink-0" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="grid sm:grid-cols-3 gap-3">
          <div className="bg-wellness-pale rounded-xl p-4">
            <p className="text-xs text-gray-500 mb-0.5">Best Time of Day</p>
            <p className="text-sm font-medium text-wellness-dark">{data.exercise_plan.best_time}</p>
          </div>
          <div className="bg-wellness-pale rounded-xl p-4">
            <p className="text-xs text-gray-500 mb-0.5">Duration</p>
            <p className="text-sm font-medium text-wellness-dark">{data.exercise_plan.duration}</p>
          </div>
          <div className="bg-wellness-pale rounded-xl p-4">
            <p className="text-xs text-gray-500 mb-0.5">Frequency</p>
            <p className="text-sm font-medium text-wellness-dark">{data.exercise_plan.frequency}</p>
          </div>
        </div>

        {data.exercise_plan.notes && (
          <div className="mt-4 bg-blue-50 rounded-xl p-4">
            <p className="text-sm text-gray-700 italic">{data.exercise_plan.notes}</p>
          </div>
        )}
      </SectionCard>

      {/* Sleep Plan */}
      <SectionCard id="sleep" title="Sleep Optimisation Plan" icon={
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      }>
        <div className="grid sm:grid-cols-2 gap-3 mb-6">
          <div className="bg-indigo-50 rounded-xl p-4">
            <p className="text-xs text-indigo-500 mb-0.5">Ideal Sleep Hours</p>
            <p className="text-sm font-medium text-indigo-700">{data.sleep_plan.ideal_hours}</p>
          </div>
          <div className="bg-indigo-50 rounded-xl p-4">
            <p className="text-xs text-indigo-500 mb-0.5">Best Sleeping Position</p>
            <p className="text-sm font-medium text-indigo-700">{data.sleep_plan.best_position}</p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold text-indigo-600 text-sm mb-3">🌙 Bedtime Routine</h3>
            <ul className="space-y-2">
              {data.sleep_plan.routine.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                  <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full mt-1.5 flex-shrink-0" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="font-semibold text-indigo-600 text-sm mb-3">✨ Best Practices</h3>
            <ul className="space-y-2">
              {data.sleep_plan.best_practices.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                  <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full mt-1.5 flex-shrink-0" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
        {data.sleep_plan.notes && (
          <div className="mt-4 bg-indigo-50 rounded-xl p-4">
            <p className="text-sm text-gray-700 italic">{data.sleep_plan.notes}</p>
          </div>
        )}
      </SectionCard>

      {/* Emotional Wellness */}
      <SectionCard id="emotional" title="Emotional Wellness Guide" icon={
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
      }>
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <div className="bg-green-50 rounded-xl p-4">
            <h3 className="font-semibold text-green-700 text-sm mb-3">💪 Strengths</h3>
            <ul className="space-y-1.5">
              {data.emotional_wellness.strengths.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-gray-700">
                  <span className="w-1.5 h-1.5 bg-green-500 rounded-full mt-1 flex-shrink-0" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div className="bg-amber-50 rounded-xl p-4">
            <h3 className="font-semibold text-amber-700 text-sm mb-3">🌱 Areas to Nurture</h3>
            <ul className="space-y-1.5">
              {data.emotional_wellness.weaknesses.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-gray-700">
                  <span className="w-1.5 h-1.5 bg-amber-500 rounded-full mt-1 flex-shrink-0" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <div>
            <h3 className="font-semibold text-pink-600 text-sm mb-3">🧘 Stress Management</h3>
            <ul className="space-y-1.5">
              {data.emotional_wellness.stress_management.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-gray-700">
                  <span className="w-1.5 h-1.5 bg-pink-400 rounded-full mt-1 flex-shrink-0" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="font-semibold text-blue-600 text-sm mb-3">🌬️ Breathing Techniques</h3>
            <ul className="space-y-1.5">
              {data.emotional_wellness.breathing_techniques.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-gray-700">
                  <span className="w-1.5 h-1.5 bg-blue-400 rounded-full mt-1 flex-shrink-0" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="bg-purple-50 rounded-xl p-4 mb-4">
          <h3 className="font-semibold text-purple-700 text-sm mb-2">🧠 Meditation Tips</h3>
          <ul className="space-y-1">
            {data.emotional_wellness.meditation_tips.map((item, i) => (
              <li key={i} className="flex items-start gap-2 text-xs text-gray-700">
                <span className="w-1.5 h-1.5 bg-purple-400 rounded-full mt-1 flex-shrink-0" />
                {item}
              </li>
            ))}
          </ul>
        </div>

        {data.emotional_wellness.notes && (
          <div className="bg-pink-50 rounded-xl p-4">
            <p className="text-sm text-gray-700 italic">{data.emotional_wellness.notes}</p>
          </div>
        )}
      </SectionCard>

      {/* Disease Prevention */}
      <SectionCard id="prevention" title="Full Disease Risk Profile" icon={
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
      }>
        <div className="space-y-4 mb-6">
          {data.disease_risks.conditions.map((condition, i) => {
            const riskColors: Record<string, string> = {
              High: "bg-red-100 text-red-700",
              Moderate: "bg-amber-100 text-amber-700",
              "Low-Moderate": "bg-green-100 text-green-700",
            };
            return (
              <div key={i} className="border border-gray-200 rounded-xl p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-gray-800 text-sm">{condition.name}</h4>
                  <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${riskColors[condition.risk_level] || "bg-gray-100 text-gray-600"}`}>
                    {condition.risk_level} Risk
                  </span>
                </div>
                <p className="text-xs text-gray-500 mb-1.5">Early Warning Signs:</p>
                <ul className="space-y-1">
                  {condition.early_warning_signs.map((sign, j) => (
                    <li key={j} className="flex items-start gap-1.5 text-xs text-gray-600">
                      <span className="w-1 h-1 bg-gray-400 rounded-full mt-1.5 flex-shrink-0" />
                      {sign}
                    </li>
                  ))}
                </ul>
              </div>
            );
          })}
        </div>

        <div className="bg-green-50 border border-green-200 rounded-xl p-4">
          <h3 className="font-semibold text-green-700 text-sm mb-2">🛡️ Prevention Tips</h3>
          <ul className="grid sm:grid-cols-2 gap-x-6 gap-y-1.5">
            {data.disease_risks.prevention_tips.map((tip, i) => (
              <li key={i} className="flex items-start gap-1.5 text-xs text-gray-700">
                <span className="w-1.5 h-1.5 bg-green-500 rounded-full mt-1 flex-shrink-0" />
                {tip}
              </li>
            ))}
          </ul>
        </div>
      </SectionCard>

      {/* Ask TibbWell CTA */}
      <div className="bg-gradient-to-br from-wellness-green to-wellness-dark rounded-2xl p-6 md:p-8 text-white text-center relative overflow-hidden">
        <div className="absolute top-0 right-0 w-40 h-40 bg-white/5 rounded-full" />
        <div className="absolute bottom-0 left-0 w-56 h-56 bg-white/5 rounded-full" />
        <div className="relative">
          <div className="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <h3 className="text-xl md:text-2xl font-bold mb-2">Have Questions About Your Health?</h3>
          <p className="text-white/80 mb-6 max-w-md mx-auto">Ask TibbWell AI — your personal health assistant powered by Unani wisdom</p>
          <Link href="/dashboard/ask" className="inline-flex items-center gap-2 bg-white text-wellness-green px-6 py-3 rounded-xl font-semibold hover:bg-wellness-light transition-all">
            Ask TibbWell AI
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </Link>
        </div>
      </div>
    </div>
  );
}