// ─── Premium Dashboard API Types ────────────────────────────

export interface FoodItem {
  name: string;
  why: string;
}

export interface PremiumDashboardData {
  user: {
    name: string;
    email: string;
    is_premium: boolean;
    subscription_status: string;
  };
  temperament: {
    dominant: string;
    sub_dominant: string;
    combination: string;
    quality: string;
  };
  monthly_focus: {
    month: string;
    year: number;
    title: string;
    content: string;
    tip: string;
  };
  food_guide: {
    foods_to_eat: FoodItem[];
    foods_to_avoid: FoodItem[];
    cooking_methods: string[];
    meal_timing: string;
    water_intake: string;
    tips: string[];
  };
  seasonal_protocol: {
    summer: { description: string; recommendations: string[] };
    autumn: { description: string; recommendations: string[] };
    winter: { description: string; recommendations: string[] };
    spring: { description: string; recommendations: string[] };
    current_season: string;
  };
  exercise_plan: {
    recommended: string[];
    avoid: string[];
    best_time: string;
    duration: string;
    frequency: string;
    notes: string;
  };
  sleep_plan: {
    ideal_hours: string;
    best_position: string;
    routine: string[];
    best_practices: string[];
    notes: string;
  };
  emotional_wellness: {
    strengths: string[];
    weaknesses: string[];
    stress_management: string[];
    breathing_techniques: string[];
    meditation_tips: string[];
    notes: string;
  };
  disease_risks: {
    conditions: Array<{ name: string; risk_level: string; early_warning_signs: string[] }>;
    prevention_tips: string[];
  };
  full_programme_url?: string;
}

// ─── MOCK DATA ─────────────────────────────────────────────

const summerProtocol = {
  description:
    "Summer brings heat and expansion. For your Sanguinous-Phlegmatic temperament, the focus is on cooling, hydration, and gentle movement. The heat can aggravate warmth, so prioritise cooling foods and activities.",
  recommendations: [
    "Exercise before 9am or after 6pm to avoid peak heat",
    "Swim or practice water-based activities 2-3 times weekly",
    "Hydrate with cucumber-mint infused water throughout the day",
    "Eat cooling foods: watermelon, cucumber, coconut water, leafy greens",
    "Take a short midday rest (20-min siesta) to recharge",
    "Wear light, breathable fabrics — cotton and linen",
    "Use peppermint or eucalyptus essential oils for cooling",
    "Avoid prolonged sun exposure between 11am-3pm",
  ],
};

const autumnProtocol = {
  description:
    "Autumn is a transitional season of cooling and drying. This is the ideal time to establish grounding routines. For your temperament, focus on warming foods and consistent habits to prepare for winter.",
  recommendations: [
    "Gradually shift to warmer, cooked meals as the weather cools",
    "Incorporate root vegetables: sweet potatoes, carrots, beets",
    "Establish a consistent sleep schedule before winter",
    "Practice dry brushing to stimulate circulation and lymph",
    "Enjoy moderate sun exposure in the milder mornings",
    "Begin wearing layers to protect against temperature shifts",
    "Reduce raw food intake as the season progresses",
    "Focus on immune-supporting herbs: echinacea, elderberry",
  ],
};

const winterProtocol = {
  description:
    "Winter is a time of conservation and rest. Cold and moisture dominate, which can affect your phlegmatic tendency. Prioritise warmth, gentle movement, and nourishing foods to maintain balance.",
  recommendations: [
    "Eat warm, cooked meals — soups, stews, and broths",
    "Include warming spices: ginger, cinnamon, turmeric, black pepper",
    "Maintain gentle daily movement — indoor yoga or stretching",
    "Get morning sunlight exposure for vitamin D and mood",
    "Keep your living space warm and well-humidified",
    "Practice self-massage with warm sesame oil (Abhyanga)",
    "Socialise regularly to counter the tendency to hibernate",
    "Prioritise 7-8 hours of sleep — winter is a time for rest",
  ],
};

const springProtocol = {
  description:
    "Spring is a season of renewal, lightness, and shedding stagnation. For your temperament, it's the perfect time for gentle detoxification, increased movement, and embracing fresh, light foods.",
  recommendations: [
    "Incorporate more raw greens and fresh vegetables",
    "Start a gentle detox: warm lemon water, reduce heavy foods",
    "Increase physical activity gradually — walk, jog, cycle",
    "Practice deep breathing to clear respiratory passages",
    "Spring cleaning — declutter your living and mental space",
    "Eat bitter greens to support liver function: dandelion, rocket",
    "Spend time in nature as the weather warms",
    "Set new health intentions for the coming months",
  ],
};

export const MOCK_DASHBOARD_DATA: PremiumDashboardData = {
  user: {
    name: "Sarah",
    email: "sarah@example.com",
    is_premium: true,
    subscription_status: "active",
  },
  temperament: {
    dominant: "Sanguinous",
    sub_dominant: "Phlegmatic",
    combination: "Sanguinous-Phlegmatic",
    quality: "Hot & Moist",
  },
  monthly_focus: (() => {
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const now = new Date();
    return {
    month: monthNames[now.getMonth()],
    year: now.getFullYear(),
    title: "Summer Harmony: Cooling & Grounding",
    content:
      "As summer arrives, focus on cooling practices that balance your warm temperament. Incorporate lighter meals, spend time near water, and practice gentle movement in the early morning or evening when temperatures are lower.",
    tip: "Start each morning with a glass of warm water with lemon and a 10-minute mindful breathing session to set a calm tone for the day ahead.",
    };
  })(),
  food_guide: {
    foods_to_eat: [
      {
        name: "Fresh seasonal fruits (watermelon, berries, peaches, pears)",
        why: "These cooling, hydrating fruits balance your Hot & Moist temperament. Watermelon is especially beneficial — its high water content cools the body while its natural sugars provide steady energy without inflammation.",
      },
      {
        name: "Leafy greens and cooling vegetables (cucumber, zucchini, celery, lettuce)",
        why: "Greens are naturally cooling and alkalising. Cucumber and celery have a high water content that helps regulate body temperature and support kidney function, preventing fluid retention (a phlegmatic tendency).",
      },
      {
        name: "Light proteins (fish, skinless chicken, tofu, legumes)",
        why: "Light proteins are easier to digest than red meat, reducing metabolic heat. Fish like salmon and mackerel provide omega-3s that reduce inflammation — important for your sanguinous tendency toward heat-related conditions.",
      },
      {
        name: "Whole grains (quinoa, brown rice, barley, oats)",
        why: "Whole grains provide steady, sustained energy without spiking blood sugar. Barley is particularly beneficial — it's cooling and helps clear excess moisture from the body, balancing your phlegmatic side.",
      },
      {
        name: "Herbal teas (chamomile, peppermint, hibiscus, fennel)",
        why: "Chamomile and peppermint are cooling and calming for the digestive system. Fennel tea aids digestion and reduces bloating, while hibiscus is a natural coolant that supports cardiovascular health.",
      },
      {
        name: "Healthy fats (avocado, olive oil, nuts, seeds)",
        why: "Healthy fats support hormone balance and brain function. Avocado provides moisture without heaviness, and olive oil's anti-inflammatory properties help temper the heat aspect of your constitution.",
      },
    ],
    foods_to_avoid: [
      {
        name: "Heavy fried and oily foods",
        why: "Fried foods generate excessive internal heat and create heaviness in the digestive system. For your phlegmatic tendency, they slow metabolism and promote fluid retention and lethargy.",
      },
      {
        name: "Excessive red meat (beef, lamb, pork)",
        why: "Red meat is heating and difficult to digest. It can aggravate your sanguinous heat, leading to inflammatory conditions, skin issues, and digestive sluggishness.",
      },
      {
        name: "Spicy and pungent dishes (chilli, cayenne, excessive garlic)",
        why: "While spices in moderation are beneficial, excessive pungent foods overheat the body. They can trigger inflammation, heartburn, and irritability in warm constitutions.",
      },
      {
        name: "Processed sugars and refined carbohydrates",
        why: "Sugar creates internal heat and dampness simultaneously — the worst combination for your Hot & Moist temperament. It promotes weight gain, mood swings, and candida overgrowth (a phlegmatic risk).",
      },
      {
        name: "Excessive caffeine and alcohol",
        why: "Caffeine is heating and dehydrating, while alcohol creates internal heat and toxins. Both disrupt sleep quality and can trigger anxiety in sanguinous types who already tend toward restlessness.",
      },
      {
        name: "Very cold or iced drinks with meals",
        why: "Iced drinks extinguish digestive fire (Agni), leading to poor nutrient absorption and bloating. Your phlegmatic side is especially vulnerable to this, as cold weakens already-slow digestion.",
      },
    ],
    cooking_methods: [
      "Steaming — preserves nutrients and keeps foods light",
      "Light sautéing with olive or coconut oil",
      "Boiling and poaching — gentle, non-heating methods",
      "Baking and roasting at moderate temperatures",
      "Raw preparations in summer (salads, smoothies)",
      "Slow cooking for soups and stews in cooler months",
    ],
    meal_timing:
      "Eat your largest meal at lunch (12pm-1pm) when digestion is strongest. Have a light breakfast by 8am, and finish dinner by 7pm — at least 3 hours before bed. Avoid snacking after 8pm to support overnight detoxification.",
    water_intake:
      "Aim for 8-10 glasses (2-2.5 litres) of water daily. Drink warm or room-temperature water throughout the day — avoid ice-cold water. Start your morning with 2 glasses of warm water with lemon to kickstart digestion and hydration.",
    tips: [
      "Chew each mouthful 20-30 times to support digestion before it reaches your stomach",
      "Include all 6 tastes (sweet, sour, salty, bitter, pungent, astringent) in your main meal",
      "Drink herbal tea between meals rather than with food to avoid diluting digestive enzymes",
      "Take a short (5-10 min) walk after meals to aid digestion without strenuous activity",
    ],
  },
  seasonal_protocol: {
    summer: summerProtocol,
    autumn: autumnProtocol,
    winter: winterProtocol,
    spring: springProtocol,
    current_season: "Early Summer",
  },
  exercise_plan: {
    recommended: [
      "Brisk walking (30 min, 5-6 days/week)",
      "Swimming or aqua aerobics",
      "Yoga (especially cooling sequences like moon salutations)",
      "Cycling at moderate pace",
      "Dancing or group fitness classes",
      "Tai Chi or Qi Gong",
    ],
    avoid: [
      "High-intensity interval training in midday heat",
      "Prolonged sun exposure during exercise",
      "Overexertion leading to excessive sweating",
      "Competitive sports that elevate stress hormones",
    ],
    best_time: "Morning (6am-9am) or Evening (5pm-7pm). Avoid midday 11am-3pm.",
    duration: "30-45 minutes per session",
    frequency: "5-6 days per week",
    notes:
      "Your Sanguinous-Phlegmatic temperament thrives on consistent, moderate exercise. Variety is key — mix cardio, strength, and flexibility work to stay motivated. Listen to your body: if you feel depleted, a gentle walk is better than pushing through intense exercise.",
  },
  sleep_plan: {
    ideal_hours: "7-8 hours per night. Bed by 10pm, awake by 6am.",
    best_position:
      "Sleep on your back or left side (the left side aids lymphatic drainage and supports heart function). Avoid sleeping on your stomach, which can strain the neck and compress internal organs.",
    routine: [
      "Wind down by 9:30pm — dim lights, reduce screen brightness",
      "Light stretching or gentle yoga for 10 minutes at 9pm",
      "Warm herbal tea (chamomile, lavender, or passionflower) at 9:15pm",
      "Read something light and uplifting for 15 minutes",
      "Write a gratitude list (3 things you're grateful for today)",
      "No screens for at least 30 minutes before bed",
      "Keep bedroom temperature at 18-20°C with good ventilation",
    ],
    best_practices: [
      "Consistent sleep and wake times — even on weekends",
      "Cool shower before bed in summer, warm foot bath in winter",
      "Use cotton or bamboo bed sheets for breathability",
      "Essential oil diffuser with lavender or cedarwood",
      "Practice 4-7-8 breathing (inhale 4, hold 7, exhale 8) to fall asleep",
      "Avoid heavy meals, caffeine, and alcohol within 3 hours of bed",
    ],
    notes:
      "Your Sanguinous-Phlegmatic constitution responds exceptionally well to routine. Once your sleep schedule is consistent for 21 days, it becomes automatic. If you wake during the night (common with phlegmatic types), resist checking your phone — instead, practice slow belly breathing for 5 minutes.",
  },
  emotional_wellness: {
    strengths: [
      "Naturally optimistic and cheerful — you uplift those around you",
      "Adaptable and open to new experiences",
      "Warm and approachable — people feel comfortable with you",
      "Calm under pressure — your phlegmatic side brings steadiness",
      "Socially skilled — you build connections easily",
    ],
    weaknesses: [
      "Tendency to avoid difficult emotions by staying busy",
      "May struggle with follow-through on long-term goals",
      "Can be overly agreeable to maintain harmony",
      "Prone to comfort-seeking when stressed (comfort eating, procrastination)",
      "May suppress feelings rather than expressing them directly",
    ],
    stress_management: [
      "Practice the 5-4-3-2-1 grounding technique: name 5 things you see, 4 you can touch, 3 you hear, 2 you can smell, 1 you can taste",
      "Take a 'mindful walk' — 20 minutes in nature without headphones or phone",
      "Use journaling to process emotions: write freely for 10 minutes without judgment",
      "Set healthy boundaries — it's okay to say no to preserve your energy",
      "Schedule 'white space' in your calendar — unscheduled time to just be",
    ],
    breathing_techniques: [
      "4-7-8 Breathing: Inhale through nose for 4 counts, hold for 7, exhale through mouth for 8. Repeat 4 times. This activates the parasympathetic nervous system.",
      "Alternate Nostril Breathing (Nadi Shodhana): Close right nostril, inhale left for 4 counts. Close left, exhale right for 8. Inhale right for 4, close, exhale left for 8. Repeat 5 rounds.",
      "Belly Breathing: Place hands on belly, inhale deeply feeling your belly rise, exhale slowly feeling it fall. Do this for 5 minutes before bed or during stress.",
    ],
    meditation_tips: [
      "Start with just 5 minutes daily — consistency matters more than duration",
      "Use a guided meditation app if sitting in silence feels difficult",
      "Practice loving-kindness meditation: 'May I be happy, may I be healthy, may I be at peace'",
      "Try walking meditation — focus on each step, the sensation of your feet touching the ground",
      "Body scan meditation: slowly bring attention to each part of your body from toes to crown",
    ],
    notes:
      "Your warm, social temperament thrives on connection, but your phlegmatic side requires quiet reflection. The key is balance: schedule social time AND solo time each week. When you feel overwhelmed, your body is asking for rest — not distraction. When you feel isolated, reach out — connection is your medicine.",
  },
  disease_risks: {
    conditions: [
      {
        name: "Digestive Sluggishness",
        risk_level: "High",
        early_warning_signs: [
          "Bloating after meals",
          "Irregular bowel movements",
          "Feeling heavy or lethargic after eating",
          "Acid reflux or heartburn",
        ],
      },
      {
        name: "Respiratory Congestion",
        risk_level: "Moderate",
        early_warning_signs: [
          "Frequent colds that linger",
          "Sinus congestion, especially in damp weather",
          "Post-nasal drip",
          "Allergies worsening seasonally",
        ],
      },
      {
        name: "Weight Management Challenges",
        risk_level: "Moderate",
        early_warning_signs: [
          "Gradual, unexplained weight gain",
          "Fluid retention (puffiness in hands, feet, face)",
          "Cravings for carbohydrates and sweets",
          "Slow metabolism — feeling cold often",
        ],
      },
      {
        name: "Circulation Concerns",
        risk_level: "Low-Moderate",
        early_warning_signs: [
          "Cold hands and feet, even in warm weather",
          "Numbness or tingling in extremities",
          "Varicose veins",
          "Slow-healing minor wounds",
        ],
      },
      {
        name: "Seasonal Affective Patterns",
        risk_level: "Moderate",
        early_warning_signs: [
          "Low energy and motivation in winter months",
          "Increased sleep need during colder seasons",
          "Carbohydrate cravings in autumn/winter",
          "Social withdrawal when days are short",
        ],
      },
    ],
    prevention_tips: [
      "Maintain consistent exercise — 30 min daily to support metabolism and circulation",
      "Eat warming spices like ginger, turmeric, cinnamon, and black pepper daily",
      "Stay hydrated with warm or room-temperature beverages — not ice-cold drinks",
      "Practice dry brushing 3-4 times weekly to stimulate circulation and lymph",
      "Get 15-20 minutes of morning sunlight for vitamin D and circadian rhythm support",
      "Schedule regular health check-ups, especially before seasonal transitions",
      "Alternate between hot and cold in your final minute of showering to stimulate circulation",
      "Include probiotic foods (yogurt, kefir, kimchi) to support gut health and immunity",
    ],
  },
  full_programme_url: "#",
};

export const MOCK_TEMPERAMENT_COMBINATIONS = [
  {
    id: 1,
    combination_name: "Sanguinous-Phlegmatic",
    description: "A balanced and adaptable combination. You blend warmth with calm, making you approachable, steady, and naturally nurturing.",
    foods_to_eat: ["Fresh fruits", "Leafy greens", "Light proteins", "Whole grains", "Herbal teas", "Healthy fats"],
    foods_to_avoid: ["Heavy dairy", "Excess carbs", "Fried foods", "Processed sugar", "Artificial sweeteners"],
    disease_risks: ["Weight gain", "Sluggish digestion", "Respiratory congestion", "Seasonal allergies"],
    seasonal_tips: "Spring is your best season for detox and renewal.",
  },
  {
    id: 2,
    combination_name: "Sanguinous-Bilious",
    description: "A vibrant combination of warmth and drive. You have natural charisma and leadership abilities.",
    foods_to_eat: ["Fresh vegetables", "Cooling fruits", "Whole grains", "Legumes", "Herbal teas"],
    foods_to_avoid: ["Spicy foods", "Fried foods", "Excess red meat", "Alcohol", "Processed sugars"],
    disease_risks: ["Inflammatory conditions", "Digestive imbalances", "Skin irritations"],
    seasonal_tips: "In summer, focus on cooling activities.",
  },
  {
    id: 3,
    combination_name: "Sanguinous-Melancholic",
    description: "An interesting mix of optimism and depth. You have both social energy and introspective wisdom.",
    foods_to_eat: ["Warming meals", "Root vegetables", "Healthy fats", "Nuts and seeds", "Dark leafy greens"],
    foods_to_avoid: ["Excess raw foods", "Caffeine late in day", "Processed foods", "Sugary snacks"],
    disease_risks: ["Mood fluctuations", "Digestive sensitivity", "Sleep disturbances"],
    seasonal_tips: "Autumn is your season for grounding routines.",
  },
  {
    id: 4,
    combination_name: "Bilious-Sanguinous",
    description: "A powerful combination of fire and vitality. You are a natural leader with infectious energy.",
    foods_to_eat: ["Cooling vegetables", "Sweet fruits", "Whole grains", "Mild legumes", "Aloe vera"],
    foods_to_avoid: ["Spicy foods", "Sour foods", "Fermented foods", "Hot beverages", "Excess red meat"],
    disease_risks: ["Acidity and heartburn", "Inflammatory skin", "Stress tension"],
    seasonal_tips: "Summer requires cooling practices.",
  },
  {
    id: 5,
    combination_name: "Bilious-Phlegmatic",
    description: "An uncommon but powerful mix of intensity and calm. You can switch between driven focus and relaxed contentment.",
    foods_to_eat: ["Bitter greens", "Steamed vegetables", "Light grains", "Warm lemon water", "Lean poultry"],
    foods_to_avoid: ["Heavy creamy sauces", "Deep-fried foods", "Excess salt", "Fermented foods", "Cold dairy"],
    disease_risks: ["Digestive inconsistencies", "Weight fluctuations", "Skin breakouts"],
    seasonal_tips: "Transitional seasons are key for resetting your routine.",
  },
  {
    id: 6,
    combination_name: "Bilious-Melancholic",
    description: "A driven and analytical combination. You have strong determination paired with deep thinking.",
    foods_to_eat: ["Warming soups", "Cooked vegetables", "Healthy grains", "Warming teas", "Omega-3 foods"],
    foods_to_avoid: ["Caffeine", "Cold foods", "Dry snacks", "Excess sugar", "Processed meats"],
    disease_risks: ["Stress disorders", "Digestive issues", "Sleep problems"],
    seasonal_tips: "Winter is your time to slow down and prioritise rest.",
  },
  {
    id: 7,
    combination_name: "Phlegmatic-Sanguinous",
    description: "A warm and easy-going combination. You bring people together with your calm presence.",
    foods_to_eat: ["Light meals", "Fresh fruits", "Lean proteins", "Herbal infusions", "Mild spices"],
    foods_to_avoid: ["Heavy creamy foods", "Excess carbs", "Very cold drinks", "Large dairy", "Fried food"],
    disease_risks: ["Slow metabolism", "Water retention", "Lethargy", "Respiratory congestion"],
    seasonal_tips: "Spring — incorporate light detox and more movement.",
  },
  {
    id: 8,
    combination_name: "Phlegmatic-Bilious",
    description: "A unique mix of calm with hidden fire. You appear relaxed but have a strong will.",
    foods_to_eat: ["Warm cooked meals", "Root vegetables", "Mild spices", "Whole grains", "Warm lemon water"],
    foods_to_avoid: ["Creamy sauces", "Deep-fried", "Excess cold foods", "Heavy red meat", "Sugary desserts"],
    disease_risks: ["Weight management", "Digestive sluggishness", "Mood swings"],
    seasonal_tips: "Summer is your best season for staying active.",
  },
  {
    id: 9,
    combination_name: "Phlegmatic-Melancholic",
    description: "A gentle and reflective combination. You are kind, thoughtful, and value stability.",
    foods_to_eat: ["Warming meals", "Cooked vegetables", "Healthy grains", "Warming herbs", "Soups"],
    foods_to_avoid: ["Raw cold foods", "Excess dairy", "Processed foods", "Sugar", "Caffeine"],
    disease_risks: ["Low energy", "Seasonal depression", "Slow circulation", "Weight gain"],
    seasonal_tips: "Late autumn/winter — extra self-care and warm meals.",
  },
  {
    id: 10,
    combination_name: "Melancholic-Sanguinous",
    description: "A creative and thoughtful combination. You blend depth with warmth.",
    foods_to_eat: ["Warm nourishing meals", "Healthy fats", "Cooked greens", "Whole grains", "Warming teas"],
    foods_to_avoid: ["Dry rough foods", "Excess raw salads", "Cold drinks", "Caffeine", "Processed snacks"],
    disease_risks: ["Anxiety", "Digestive sensitivity", "Sleep disruption", "Dry skin"],
    seasonal_tips: "Spring — establish new routines and spend time in nature.",
  },
  {
    id: 11,
    combination_name: "Melancholic-Bilious",
    description: "An intense and purposeful combination. You combine analytical depth with determination.",
    foods_to_eat: ["Warm moist foods", "Cooked grains", "Healthy oils", "Sweet vegetables", "Warming spices"],
    foods_to_avoid: ["Spicy foods", "Dry hard foods", "Excess caffeine", "Alcohol", "Fermented foods"],
    disease_risks: ["Stress tension", "Digestive inflammation", "Sleep issues", "Headaches"],
    seasonal_tips: "Autumn is your power season for focused projects.",
  },
  {
    id: 12,
    combination_name: "Melancholic-Phlegmatic",
    description: "A calm and thoughtful combination. You are deeply reflective with a gentle nature.",
    foods_to_eat: ["Warm digestible foods", "Steamed vegetables", "Light proteins", "Warm teas", "Porridges"],
    foods_to_avoid: ["Heavy greasy foods", "Excess dairy", "Cold foods", "Processed meats", "Sugary treats"],
    disease_risks: ["Low energy", "Digestive sluggishness", "Seasonal mood changes", "Circulation issues"],
    seasonal_tips: "Spring is your time for gentle renewal with small daily habits.",
  },
];