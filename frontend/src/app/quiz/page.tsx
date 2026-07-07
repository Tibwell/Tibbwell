"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import ProgressBar from "@/components/quiz/ProgressBar";
import QuizNavigation from "@/components/quiz/QuizNavigation";
import Link from "next/link";

// Mock questions for initial development - will be fetched from API
const MOCK_QUESTIONS = [
  {
    id: 1,
    question_text: "How would you describe your body frame?",
    category: "physical",
    options: [
      { text: "Well-built and muscular", temperament: "sanguinous", points: 3 },
      { text: "Lean and wiry", temperament: "bilious", points: 3 },
      { text: "Soft and rounded", temperament: "phlegmatic", points: 3 },
      { text: "Thin and bony", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 2,
    question_text: "What is your skin texture like?",
    category: "physical",
    options: [
      { text: "Warm and moist", temperament: "sanguinous", points: 3 },
      { text: "Warm and dry", temperament: "bilious", points: 3 },
      { text: "Cool and moist", temperament: "phlegmatic", points: 3 },
      { text: "Cool and dry", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 3,
    question_text: "How would you describe your typical energy level?",
    category: "energy",
    options: [
      { text: "Consistently energetic and enthusiastic", temperament: "sanguinous", points: 3 },
      { text: "Intense bursts of energy", temperament: "bilious", points: 3 },
      { text: "Steady and relaxed", temperament: "phlegmatic", points: 3 },
      { text: "Variable, often low energy", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 4,
    question_text: "When you catch a cold, what are your symptoms like?",
    category: "health",
    options: [
      { text: "Heavy mucus, congestion, mild fever", temperament: "sanguinous", points: 3 },
      { text: "High fever, dry cough, inflammation", temperament: "bilious", points: 3 },
      { text: "Mild symptoms, lots of phlegm, slow recovery", temperament: "phlegmatic", points: 3 },
      { text: "Dry cough, low energy, lingering illness", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 5,
    question_text: "How is your appetite usually?",
    category: "digestive",
    options: [
      { text: "Good appetite, enjoy rich food", temperament: "sanguinous", points: 3 },
      { text: "Strong appetite, prefer spicy food", temperament: "bilious", points: 3 },
      { text: "Moderate appetite, comfort eater", temperament: "phlegmatic", points: 3 },
      { text: "Variable appetite, picky eater", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 6,
    question_text: "How would you describe your sleep pattern?",
    category: "sleep",
    options: [
      { text: "Deep sleeper, fall asleep easily", temperament: "sanguinous", points: 3 },
      { text: "Light sleeper, wake up early", temperament: "bilious", points: 3 },
      { text: "Heavy sleeper, need many hours", temperament: "phlegmatic", points: 3 },
      { text: "Trouble falling asleep, wake often", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 7,
    question_text: "What temperature do you prefer?",
    category: "preference",
    options: [
      { text: "Warm weather suits me best", temperament: "sanguinous", points: 3 },
      { text: "I prefer cooler environments", temperament: "bilious", points: 3 },
      { text: "I dislike both extremes", temperament: "phlegmatic", points: 3 },
      { text: "I prefer warm, cosy environments", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 8,
    question_text: "How do you react to stress?",
    category: "emotional",
    options: [
      { text: "I adapt quickly and stay optimistic", temperament: "sanguinous", points: 3 },
      { text: "I become irritable and impatient", temperament: "bilious", points: 3 },
      { text: "I withdraw and avoid confrontation", temperament: "phlegmatic", points: 3 },
      { text: "I worry and overthink situations", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 9,
    question_text: "What best describes your social style?",
    category: "social",
    options: [
      { text: "Outgoing and love being around people", temperament: "sanguinous", points: 3 },
      { text: "Assertive and like to lead", temperament: "bilious", points: 3 },
      { text: "Easy-going and peace-loving", temperament: "phlegmatic", points: 3 },
      { text: "Reserved and prefer small groups", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 10,
    question_text: "How is your digestion generally?",
    category: "digestive",
    options: [
      { text: "Strong digestion, rarely have issues", temperament: "sanguinous", points: 3 },
      { text: "Fast metabolism, prone to acidity", temperament: "bilious", points: 3 },
      { text: "Slow digestion, prone to bloating", temperament: "phlegmatic", points: 3 },
      { text: "Sensitive stomach, irregular digestion", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 11,
    question_text: "What is your hair texture?",
    category: "physical",
    options: [
      { text: "Thick and lustrous", temperament: "sanguinous", points: 3 },
      { text: "Straight and fine", temperament: "bilious", points: 3 },
      { text: "Soft and wavy", temperament: "phlegmatic", points: 3 },
      { text: "Dry and brittle", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 12,
    question_text: "How do you handle decision-making?",
    category: "mental",
    options: [
      { text: "Quick decisions based on intuition", temperament: "sanguinous", points: 3 },
      { text: "Decisive and confident", temperament: "bilious", points: 3 },
      { text: "Prefer others to decide", temperament: "phlegmatic", points: 3 },
      { text: "Careful analysis before deciding", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 13,
    question_text: "Your ideal weekend looks like:",
    category: "lifestyle",
    options: [
      { text: "Social gatherings and new experiences", temperament: "sanguinous", points: 3 },
      { text: "Productive projects and goals", temperament: "bilious", points: 3 },
      { text: "Resting at home with comfort food", temperament: "phlegmatic", points: 3 },
      { text: "Quiet time with a good book", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 14,
    question_text: "How do you typically react to change?",
    category: "emotional",
    options: [
      { text: "Embrace it with enthusiasm", temperament: "sanguinous", points: 3 },
      { text: "Take charge and adapt quickly", temperament: "bilious", points: 3 },
      { text: "Resist change and prefer routine", temperament: "phlegmatic", points: 3 },
      { text: "Anxious but eventually adjust", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 15,
    question_text: "What kind of weather affects you most?",
    category: "health",
    options: [
      { text: "Humid weather makes me sluggish", temperament: "sanguinous", points: 3 },
      { text: "Hot weather makes me irritable", temperament: "bilious", points: 3 },
      { text: "Cold and damp weather is hardest", temperament: "phlegmatic", points: 3 },
      { text: "Cold, dry weather affects me most", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 16,
    question_text: "Your speaking style is:",
    category: "social",
    options: [
      { text: "Lively and talkative", temperament: "sanguinous", points: 3 },
      { text: "Direct and persuasive", temperament: "bilious", points: 3 },
      { text: "Slow and gentle", temperament: "phlegmatic", points: 3 },
      { text: "Quiet and thoughtful", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 17,
    question_text: "What best describes your memory?",
    category: "mental",
    options: [
      { text: "Good with faces and names", temperament: "sanguinous", points: 3 },
      { text: "Good with facts and figures", temperament: "bilious", points: 3 },
      { text: "Good with routines and habits", temperament: "phlegmatic", points: 3 },
      { text: "Good with details and past events", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 18,
    question_text: "How do you react to criticism?",
    category: "emotional",
    options: [
      { text: "Brush it off easily", temperament: "sanguinous", points: 3 },
      { text: "Challenge it assertively", temperament: "bilious", points: 3 },
      { text: "Take it personally, feel hurt", temperament: "phlegmatic", points: 3 },
      { text: "Overthink and dwell on it", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 19,
    question_text: "Your exercise preference:",
    category: "lifestyle",
    options: [
      { text: "Dancing, group sports, variety", temperament: "sanguinous", points: 3 },
      { text: "Competitive sports, high intensity", temperament: "bilious", points: 3 },
      { text: "Walking, swimming, gentle movement", temperament: "phlegmatic", points: 3 },
      { text: "Yoga, pilates, solo activities", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 20,
    question_text: "How does your body respond to cold weather?",
    category: "physical",
    options: [
      { text: "I feel cold but adapt well", temperament: "sanguinous", points: 3 },
      { text: "Cold makes me feel sharp and alert", temperament: "bilious", points: 3 },
      { text: "Cold makes me very sluggish", temperament: "phlegmatic", points: 3 },
      { text: "I feel cold deeply and struggle", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 21,
    question_text: "Your typical mood throughout the day:",
    category: "emotional",
    options: [
      { text: "Cheerful and optimistic overall", temperament: "sanguinous", points: 3 },
      { text: "Driven and focused", temperament: "bilious", points: 3 },
      { text: "Calm and content", temperament: "phlegmatic", points: 3 },
      { text: "Thoughtful and introspective", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 22,
    question_text: "What foods do you naturally crave?",
    category: "digestive",
    options: [
      { text: "Sweet and rich foods", temperament: "sanguinous", points: 3 },
      { text: "Spicy and savoury foods", temperament: "bilious", points: 3 },
      { text: "Creamy and starchy foods", temperament: "phlegmatic", points: 3 },
      { text: "Simple and light foods", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 23,
    question_text: "How do you respond to conflict?",
    category: "social",
    options: [
      { text: "Seek to resolve and make peace", temperament: "sanguinous", points: 3 },
      { text: "Confront it head-on", temperament: "bilious", points: 3 },
      { text: "Avoid it at all costs", temperament: "phlegmatic", points: 3 },
      { text: "Analyse and overthink it", temperament: "melancholic", points: 3 },
    ],
  },
  {
    id: 25,
    question_text: "What motivates you most in life?",
    category: "mental",
    options: [
      { text: "Joy, connection, and new experiences", temperament: "sanguinous", points: 3 },
      { text: "Achievement, power, and goals", temperament: "bilious", points: 3 },
      { text: "Peace, comfort, and security", temperament: "phlegmatic", points: 3 },
      { text: "Meaning, truth, and understanding", temperament: "melancholic", points: 3 },
    ],
  },
];

function calculateResults(answers: Record<number, string>) {
  const scores: Record<string, number> = {
    sanguinous: 0,
    bilious: 0,
    phlegmatic: 0,
    melancholic: 0,
  };

  MOCK_QUESTIONS.forEach((q) => {
    if (answers[q.id]) {
      const selectedOption = q.options.find((opt) => opt.text === answers[q.id]);
      if (selectedOption) {
        scores[selectedOption.temperament] += selectedOption.points;
      }
    }
  });

  // Sort by score descending
  const sorted = Object.entries(scores).sort(([, a], [, b]) => b - a);
  const dominant = sorted[0][0];
  const subDominant = sorted[1][0];

  const temperamentNames: Record<string, string> = {
    sanguinous: "Sanguinous",
    bilious: "Bilious (Choleric)",
    phlegmatic: "Phlegmatic",
    melancholic: "Melancholic",
  };

  const qualities: Record<string, string> = {
    sanguinous: "Hot & Moist",
    bilious: "Hot & Dry",
    phlegmatic: "Cold & Moist",
    melancholic: "Cold & Dry",
  };

  const qualityDescriptions: Record<string, string> = {
    "Hot & Moist":
      "You have a warm and moist constitution, giving you natural vitality, sociability, and resilience. Air is your element.",
    "Hot & Dry":
      "Your constitution is hot and dry, giving you drive, ambition, and a fiery determination. Fire is your element.",
    "Cold & Moist":
      "You have a cool and moist nature, making you calm, steady, and nurturing. Water is your element.",
    "Cold & Dry":
      "Your constitution is cold and dry, giving you depth, thoughtfulness, and a grounded perspective. Earth is your element.",
  };

  const combinationData: Record<string, any> = {
    "Sanguinous-Bilious": {
      description:
        "A vibrant combination of warmth and drive. You have natural charisma and leadership abilities, blending sociability with ambition.",
      foods_to_eat: [
        "Fresh vegetables (leafy greens)",
        "Cooling fruits (cucumber, melon)",
        "Whole grains (oats, barley)",
        "Legumes and lentils",
        "Herbal teas (chamomile, mint)",
      ],
      foods_to_avoid: [
        "Spicy foods",
        "Fried and oily foods",
        "Excessive red meat",
        "Alcohol and caffeine",
        "Processed sugars",
      ],
      disease_risks: [
        "Inflammatory conditions",
        "Digestive imbalances",
        "Skin irritations",
        "High blood pressure (moderate risk)",
      ],
      seasonal_tip:
        "In summer, focus on cooling activities and lighter meals. In winter, maintain moderate exercise to keep your warmth balanced.",
    },
    "Sanguinous-Phlegmatic": {
      description:
        "A balanced and adaptable combination. You blend warmth with calm, making you approachable, steady, and naturally nurturing.",
      foods_to_eat: [
        "Light proteins (fish, chicken)",
        "Fresh seasonal fruits",
        "Steamed vegetables",
        "Warming spices (ginger, cinnamon)",
        "Warm soups and broths",
      ],
      foods_to_avoid: [
        "Heavy dairy products",
        "Excess carbohydrates",
        "Cold and raw foods in winter",
        "Fried foods",
        "Artificial sweeteners",
      ],
      disease_risks: [
        "Weight gain tendency",
        "Sluggish digestion",
        "Respiratory congestion",
        "Seasonal allergies",
      ],
      seasonal_tip:
        "Spring is your best season for detox and renewal. Incorporate more movement and lighter eating during this time.",
    },
    "Sanguinous-Melancholic": {
      description:
        "An interesting mix of optimism and depth. You have both social energy and introspective wisdom, making you creative and empathetic.",
      foods_to_eat: [
        "Warming, nourishing meals",
        "Root vegetables",
        "Healthy fats (avocado, olive oil)",
        "Nuts and seeds",
        "Dark leafy greens",
      ],
      foods_to_avoid: [
        "Excessive raw foods",
        "Caffeinated drinks late in day",
        "Highly processed foods",
        "Sugary snacks",
        "Artificial additives",
      ],
      disease_risks: [
        "Mood fluctuations",
        "Digestive sensitivity",
        "Sleep disturbances",
        "Joint discomfort",
      ],
      seasonal_tip:
        "Autumn is your season for grounding. Establish consistent routines and prioritise sleep during this time.",
    },
    "Bilious-Sanguinous": {
      description:
        "A powerful combination of fire and vitality. You are a natural leader with infectious energy and determination.",
      foods_to_eat: [
        "Cooling vegetables (cucumber, zucchini)",
        "Sweet fruits (pears, apples)",
        "Whole grains",
        "Mild legumes",
        "Aloe vera juice",
      ],
      foods_to_avoid: [
        "Very spicy foods",
        "Excessive sour foods",
        "Fermented foods",
        "Hot beverages",
        "Red meat in excess",
      ],
      disease_risks: [
        "Acidity and heartburn",
        "Inflammatory skin conditions",
        "Stress-related tension",
        "Liver heat symptoms",
      ],
      seasonal_tip:
        "Summer requires cooling practices — avoid midday heat, eat lighter meals, and practice calming activities like swimming.",
    },
    "Bilious-Phlegmatic": {
      description:
        "An uncommon but powerful mix of intensity and calm. You can switch between driven focus and relaxed contentment.",
      foods_to_eat: [
        "Bitter greens (kale, endive)",
        "Steamed vegetables",
        "Light grains (quinoa, rice)",
        "Warm lemon water",
        "Lean poultry",
      ],
      foods_to_avoid: [
        "Heavy creamy sauces",
        "Deep-fried foods",
        "Excess salt",
        "Fermented foods",
        "Cold dairy",
      ],
      disease_risks: [
        "Digestive inconsistencies",
        "Weight fluctuations",
        "Skin breakouts",
        "Seasonal fatigue",
      ],
      seasonal_tip:
        "Transitional seasons (spring and autumn) are key for you. Use these times to reset your routine and diet.",
    },
    "Bilious-Melancholic": {
      description:
        "A driven and analytical combination. You have strong determination paired with deep thinking, making you a strategic problem-solver.",
      foods_to_eat: [
        "Warming soups and stews",
        "Cooked vegetables",
        "Healthy grains (brown rice, millet)",
        "Warming herbal teas",
        "Omega-3 rich foods (salmon, flax)",
      ],
      foods_to_avoid: [
        "Caffeine and stimulants",
        "Cold foods and drinks",
        "Dry crackers and snacks",
        "Excess sugar",
        "Processed meats",
      ],
      disease_risks: [
        "Stress-related disorders",
        "Digestive issues",
        "Sleep problems",
        "Joint stiffness",
      ],
      seasonal_tip:
        "Winter is your time to slow down. Prioritise warming foods, adequate rest, and gentle indoor movement.",
    },
    "Phlegmatic-Sanguinous": {
      description:
        "A warm and easy-going combination. You bring people together with your calm presence and gentle enthusiasm for life.",
      foods_to_eat: [
        "Light, easily digestible meals",
        "Fresh fruits and vegetables",
        "Lean proteins",
        "Herbal infusions",
        "Spices in moderation (turmeric, cardamom)",
      ],
      foods_to_avoid: [
        "Heavy, creamy foods",
        "Excess carbohydrates",
        "Very cold drinks",
        "Dairy in large quantities",
        "Fried and oily food",
      ],
      disease_risks: [
        "Slow metabolism",
        "Water retention",
        "Lethargy",
        "Respiratory congestion",
      ],
      seasonal_tip:
        "Spring can bring congestion — incorporate light detox practices, dry brushing, and more movement into your routine.",
    },
    "Phlegmatic-Bilious": {
      description:
        "A unique mix of calm with hidden fire. You appear relaxed but have a strong will that emerges when needed.",
      foods_to_eat: [
        "Warm, cooked meals",
        "Root vegetables",
        "Mild spices (cumin, fennel)",
        "Whole grains",
        "Warm water with lemon",
      ],
      foods_to_avoid: [
        "Creamy sauces",
        "Deep-fried foods",
        "Excessively cold foods",
        "Heavy red meat",
        "Sugary desserts",
      ],
      disease_risks: [
        "Weight management challenges",
        "Digestive sluggishness",
        "Mood swings",
        "Skin congestion",
      ],
      seasonal_tip:
        "Summer is your best season. Use the natural warmth to stay active and maintain a lighter diet.",
    },
    "Phlegmatic-Melancholic": {
      description:
        "A gentle and reflective combination. You are kind, thoughtful, and value stability and deep connections.",
      foods_to_eat: [
        "Warming, nourishing meals",
        "Cooked vegetables",
        "Healthy grains",
        "Warming herbs (ginger, cinnamon)",
        "Comforting soups",
      ],
      foods_to_avoid: [
        "Raw, cold foods",
        "Excess dairy",
        "Processed foods",
        "Sugar-heavy items",
        "Caffeine",
      ],
      disease_risks: [
        "Low energy",
        "Seasonal depression tendency",
        "Slow circulation",
        "Weight gain",
      ],
      seasonal_tip:
        "Late autumn and winter require extra self-care. Prioritise warm meals, social connection, and gentle daily movement.",
    },
    "Melancholic-Sanguinous": {
      description:
        "A creative and thoughtful combination. You blend depth with warmth, making you both insightful and approachable.",
      foods_to_eat: [
        "Nourishing warm meals",
        "Healthy fats (nuts, seeds, avocado)",
        "Cooked greens",
        "Whole grains",
        "Warming herbal teas",
      ],
      foods_to_avoid: [
        "Dry, rough foods",
        "Excessive raw salads",
        "Cold drinks",
        "Caffeine",
        "Processed snacks",
      ],
      disease_risks: [
        "Anxiety and worry",
        "Digestive sensitivity",
        "Sleep disruption",
        "Dry skin conditions",
      ],
      seasonal_tip:
        "Spring brings renewal — use this time to establish new healthy routines and spend time in nature.",
    },
    "Melancholic-Bilious": {
      description:
        "An intense and purposeful combination. You combine analytical depth with strong determination and focus.",
      foods_to_eat: [
        "Warm, moist foods",
        "Cooked grains and vegetables",
        "Healthy oils",
        "Sweet vegetables (carrots, squash)",
        "Warming spices (cardamom, fennel)",
      ],
      foods_to_avoid: [
        "Very spicy foods",
        "Dry, hard foods",
        "Excess caffeine",
        "Alcohol",
        "Fermented foods in excess",
      ],
      disease_risks: [
        "Stress-related tension",
        "Digestive inflammation",
        "Sleep issues",
        "Headaches",
      ],
      seasonal_tip:
        "Autumn is your power season. Use the cooling energy to focus on projects while maintaining grounding practices.",
    },
    "Melancholic-Phlegmatic": {
      description:
        "A calm and thoughtful combination. You are deeply reflective with a gentle, steady nature.",
      foods_to_eat: [
        "Warm, easily digestible foods",
        "Steamed vegetables",
        "Light proteins",
        "Warm herbal teas",
        "Comforting porridges",
      ],
      foods_to_avoid: [
        "Heavy, greasy foods",
        "Excess dairy",
        "Cold foods and drinks",
        "Processed meats",
        "Sugary treats",
      ],
      disease_risks: [
        "Low energy and motivation",
        "Digestive sluggishness",
        "Seasonal mood changes",
        "Circulation issues",
      ],
      seasonal_tip:
        "Spring is your time for gentle renewal. Start with small daily habits — a short walk, fresh foods, and social connection.",
    },
  };

  const dominantName = temperamentNames[dominant];
  const subDominantName = temperamentNames[subDominant];

  // Short names match combinationData keys (e.g. "Bilious" not "Bilious (Choleric)")
  const temperamentKeyNames: Record<string, string> = {
    sanguinous: "Sanguinous",
    bilious: "Bilious",
    phlegmatic: "Phlegmatic",
    melancholic: "Melancholic",
  };
  const comboKey = `${temperamentKeyNames[dominant]}-${temperamentKeyNames[subDominant]}`;

  // Fallback if combination not found (reverse order)
  const reversedComboKey = `${temperamentKeyNames[subDominant]}-${temperamentKeyNames[dominant]}`;
  const combo = combinationData[comboKey] || combinationData[reversedComboKey];

  const dominantQuality = qualities[dominant];

  return {
    dominant_temperament: dominantName,
    sub_dominant_temperament: subDominantName,
    combination: `${dominantName}-${subDominantName}`,
    description: combo?.description || "Your unique temperament combination reflects a balanced constitution.",
    dominant_quality: dominantQuality,
    quality_explanation: qualityDescriptions[dominantQuality] || "",
    foods_to_eat: combo?.foods_to_eat || [],
    foods_to_avoid: combo?.foods_to_avoid || [],
    disease_risks: combo?.disease_risks || [],
    seasonal_tip: combo?.seasonal_tip || "Listen to your body and adjust your lifestyle with the seasons.",
  };
}

export default function QuizPage() {
  const router = useRouter();
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const question = MOCK_QUESTIONS[currentQuestion];

  const handleSelectOption = (optionText: string) => {
    setAnswers((prev) => ({
      ...prev,
      [question.id]: optionText,
    }));
  };

  const handleNext = () => {
    if (currentQuestion < MOCK_QUESTIONS.length - 1) {
      setCurrentQuestion((prev) => prev + 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handleBack = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion((prev) => prev - 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handleSubmit = () => {
    setIsSubmitting(true);
    // Calculate results locally and store in sessionStorage
    const results = calculateResults(answers);
    sessionStorage.setItem("tibbwell_results", JSON.stringify(results));
    router.push("/quiz/results");
  };

  const currentAnswer = answers[question.id] || "";
  const canGoNext = currentAnswer !== "";

  return (
    <div className="min-h-screen bg-gradient-to-b from-wellness-pale to-white">
      {/* Header */}
      <header className="bg-white border-b border-wellness-light">
        <div className="max-w-2xl mx-auto px-4 py-4 flex items-center gap-2">
          <div className="w-8 h-8 bg-wellness-green rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">TW</span>
          </div>
          <span className="text-lg font-bold text-wellness-dark">TibbWell</span>
          <span className="text-gray-400 mx-2">|</span>
          <span className="text-sm text-gray-500">Temperament Quiz</span>
        </div>
      </header>

      <div className="max-w-2xl mx-auto px-4 py-8">
        {/* Progress */}
        <ProgressBar current={currentQuestion} total={MOCK_QUESTIONS.length} />

        {/* Question Card */}
        <div className="bg-white rounded-2xl shadow-lg p-8 animate-fade-in" key={currentQuestion}>
          {/* Category badge */}
          <span className="inline-block bg-wellness-light text-wellness-green text-xs font-semibold px-3 py-1 rounded-full capitalize mb-4">
            {question.category}
          </span>

          {/* Question text */}
          <h2 className="text-xl md:text-2xl font-bold text-wellness-dark mb-6">
            {question.question_text}
          </h2>

          {/* Options */}
          <div className="space-y-3">
            {question.options.map((option) => (
              <button
                key={option.text}
                onClick={() => handleSelectOption(option.text)}
                className={`quiz-option ${
                  currentAnswer === option.text ? "selected" : ""
                }`}
              >
                <div
                  className={`w-5 h-5 rounded-full border-2 flex items-center justify-center flex-shrink-0 ${
                    currentAnswer === option.text
                      ? "border-wellness-green bg-wellness-green"
                      : "border-gray-300"
                  }`}
                >
                  {currentAnswer === option.text && (
                    <div className="w-2 h-2 rounded-full bg-white" />
                  )}
                </div>
                <span
                  className={`${
                    currentAnswer === option.text
                      ? "text-wellness-green font-medium"
                      : "text-gray-700"
                  }`}
                >
                  {option.text}
                </span>
              </button>
            ))}
          </div>

          {/* Navigation */}
          <QuizNavigation
            currentQuestion={currentQuestion}
            totalQuestions={MOCK_QUESTIONS.length}
            onNext={handleNext}
            onBack={handleBack}
            onSubmit={handleSubmit}
            canGoNext={canGoNext}
          />
        </div>
      </div>
    </div>
  );
}