-- TibbWell Database Seed Data
-- 25 Quiz Questions + 4 Temperaments + Example Combinations + Premium Content

-- ============================================
-- TEMPERAMENTS (The 4 Base Types)
-- ============================================

INSERT INTO temperaments (name, quality, element, description, traits) VALUES
('Sanguinous', 'Hot & Moist', 'Air', 
 'The Sanguinous temperament is characterized by warmth and moisture. People with this constitution tend to be social, enthusiastic, creative, and optimistic. They have a tendency toward weight gain, may experience circulatory issues, and often have a strong appetite.',
 '["sociable", "optimistic", "creative", "enthusiastic", "talkative", "generous", "warm-hearted", "spontaneous"]'),
 
('Bilious', 'Hot & Dry', 'Fire',
 'The Bilious temperament is characterized by heat and dryness. People with this constitution tend to be ambitious, determined, decisive, and passionate. They may experience inflammation, irritability, and have a strong metabolism with a tendency toward weight loss.',
 '["ambitious", "determined", "decisive", "passionate", "courageous", "leadership", "assertive", "intense"]'),
 
('Phlegmatic', 'Cold & Moist', 'Water',
 'The Phlegmatic temperament is characterized by coldness and moisture. People with this constitution tend to be calm, thoughtful, diplomatic, and patient. They may experience sluggishness, weight gain, and have a slower metabolism.',
 '["calm", "thoughtful", "diplomatic", "patient", "reliable", "easy-going", "observant", "sympathetic"]'),
 
('Melancholic', 'Cold & Dry', 'Earth',
 'The Melancholic temperament is characterized by coldness and dryness. People with this constitution tend to be analytical, detail-oriented, perfectionist, and creative. They may experience digestive issues, anxiety, and have a tendency toward weight loss.',
 '["analytical", "detail-oriented", "perfectionist", "creative", "introverted", "conscientious", "logical", "sensitive"]');

-- ============================================
-- TEMPERAMENT COMBINATIONS (6 Common Pairs)
-- ============================================

INSERT INTO temperament_combinations (name, description, foods_to_eat, foods_to_avoid, disease_risks, seasonal_tips, exercise_plan, sleep_plan, emotional_guide) VALUES
('Sanguinous-Bilious', 'A dynamic combination of Hot & Moist with Hot & Dry. Characterized by high energy, ambition, and social charisma with a tendency toward inflammation and urgency.',
 '["fresh fruits", "vegetables", "leafy greens", "cucumbers", "lettuce", "zucchini", "coconut water", "rose water", "mint tea", "barley water"]',
 '["spicy foods", "fried foods", "red meat", "processed foods", "caffeine", "alcohol", "hot spices", "turmeric", "ginger", "garlic"]',
 '["hypertension", "heart disease", "stroke", "inflammatory conditions", "skin eruptions", "acne", "migraines", "ulcers"]',
 '["Summer: Stay cool with melon and cucumber. Avoid sun exposure.", "Spring: Gentle detox with green juices.", "Winter: Balance with warm soups.", "Autumn: Focus on hydration."]',
 '{"type": "moderate cardio", "duration": "30-45 minutes", "frequency": "4-5x/week", "activities": ["swimming", "walking", "yoga", "cycling"], "avoid": "intense competitive sports"}',
 '{"hours": 7, "recommendation": "Maintain consistent sleep schedule", "tips": ["Avoid screens before bed", "Keep room cool", "Light blanket only"]}',
 '{"focus": "Channel energy constructively", "practices": ["Set realistic goals", "Practice patience", "Take breaks", "Express emotions healthily"], "avoid": ["overcommitting", "suppressing feelings"]}'),

('Sanguinous-Phlegmatic', 'A balanced combination of Hot & Moist with Cold & Moist. Characterized by sociability, patience, and creativity with a tendency toward sluggishness and weight gain.',
 '["light proteins", "fish", "turkey", "chicken", "beans", "lentils", "quinoa", "steamed vegetables", "green tea", "ginger tea"]',
 '["heavy carbohydrates", "dairy", "bread", "pasta", "sugar", "processed snacks", "frozen foods", "cold drinks", "ice cream"]',
 '["obesity", "diabetes", "respiratory issues", "sinusitis", "catarrh", "edema", " sluggish metabolism", "depression"]',
 '["Winter: Active exercise to combat sluggishness.", "Summer: Light activities, avoid overheating.", "Spring: Natural detox with bitter foods.", "Autumn: Boost immunity."]',
 '{"type": "active lifestyle", "duration": "40-60 minutes", "frequency": "5-6x/week", "activities": ["brisk walking", "light jogging", "dancing", "gardening"], "focus": "combat sluggishness"}',
 '{"hours": 8, "recommendation": "Prioritize quality sleep", "tips": ["Establish bedtime routine", "Avoid late meals", "Use breathing exercises"]}',
 '{"focus": "Balance social needs with alone time", "practices": ["Set boundaries", "Practice saying no", "Schedule rest", "Cultivate inner peace"], "avoid": ["over-socializing", "isolation"]}'),

('Sanguinous-Melancholic', 'A contrasting combination of Hot & Moist with Cold & Dry. Characterized by creativity, social skills, and analytical ability with internal tension.',
 '["balanced diet", "mixed fruits", "vegetables", "nuts", "seeds", "olive oil", "fish", "whole grains", "herbal teas", "honey"]',
 '["extremes in diet", "very spicy food", "very cold food", "processed foods", "artificial additives", "excessive red meat", "excessive sugar"]',
 '["digestive issues", " IBS", "anxiety", "depression", "nutritional deficiencies", "fatigue", "constipation", "mood swings"]',
 '["Winter: Comfort foods in moderation.", "Summer: Cooling foods prevent burnout.", "Spring: Gentle cleanse.", "Autumn: Stabilize routine."]',
 '{"type": "balanced exercise", "duration": "30-45 minutes", "frequency": "4-5x/week", "activities": ["yoga", "pilates", "swimming", "walking in nature"], "focus": "reduce stress"}',
 '{"hours": 7.5, "recommendation": "Consistent sleep routine essential", "tips": ["Wind down with reading", "Meditation before bed", "Comfortable sleep environment"]}',
 '{"focus": "Integrate analytical and creative thinking", "practices": ["Journaling", "Mindfulness meditation", "Creative expression", "Emotional awareness"], "avoid": ["overthinking", "emotional suppression"]}'),

('Bilious-Phlegmatic', 'A contrasting combination of Hot & Dry with Cold & Moist. Characterized by determination tempered by patience, with internal balance challenges.',
 '["cooling foods", "cucumbers", "melons", "zucchini", "coconut", "butter", "olive oil", "rice", "oatmeal", "marshmallow root tea"]',
 '["very hot spices", "chili", "turmeric", "ginger", "garlic", "vinegar", "pickles", "fermented foods", "excessive salt", "alcohol"]',
 '[" indigestion", "bloating", " alternating constipation/diarrhea", "skin conditions", "mood swings", "inflammation", "arthritis"]',
 '["Winter: Warm cooked foods.", "Summer: Stay hydrated with cooling foods.", "Spring: Gradual transition foods.", "Autumn: Build immunity."]',
 '{"type": "gentle but consistent", "duration": "35-45 minutes", "frequency": "4-5x/week", "activities": ["tai chi", "gentle yoga", "walking", "swimming"], "focus": "avoid overheating"}',
 '{"hours": 8, "recommendation": "Quality rest essential for balance", "tips": ["Cool bath before bed", "Light dinner", "Consistent schedule"]}',
 '{"focus": "Balance ambition with patience", "practices": ["Pause before reacting", "Practice deep breathing", "Set realistic deadlines", "Accept imperfection"], "avoid": ["perfectionism", "impatience with self"]}'),

('Bilious-Melancholic', 'A powerful combination of Hot & Dry with Cold & Dry. Characterized by intense intellect, ambition, and analytical thinking with a tendency toward burnout.',
 '["moistening foods", "avocados", "pears", "apples", "peas", "beans", "zucchini", "cucumber", "bone broth", "slippery elm tea"]',
 '["very hot foods", "chili", "paprika", "cayenne", "curry", "heavy spices", "coffee", "energy drinks", "processed meats", "excessive salt"]',
 '["burnout", "anxiety", "depression", "digestive ulcers", " IBS", "chronic fatigue", "insomnia", "heart conditions", "hypertension"]',
 '["Winter: Extra rest and nourishing foods.", "Summer: Cooling diet critical.", "Spring: Gradual increase in activity.", "Autumn: Prepare for intensity."]',
 '{"type": "mindful exercise", "duration": "30-40 minutes", "frequency": "3-4x/week", "activities": ["yoga", "meditative walking", "swimming", "gentle cycling"], "focus": "avoid overexertion"}',
 '{"hours": 8.5, "recommendation": "Prioritize sleep above all", "tips": ["Early bedtime", "Wind-down ritual", "Avoid work in bedroom", "Magnesium supplementation"]}',
 '{"focus": "Manage intensity and prevent burnout", "practices": ["Regular breaks", "Set boundaries", "Practice self-compassion", "Seek support", "Laugh daily"], "avoid": ["overwork", "self-criticism", "isolation"]}'),

('Phlegmatic-Melancholic', 'A subdued combination of Cold & Moist with Cold & Dry. Characterized by depth, thoughtfulness, and contemplation with a tendency toward isolation and sluggishness.',
 '["warming foods", "ginger", "cinnamon", "turmeric", "black pepper", "warm soups", "cooked vegetables", "lean proteins", "eggs", "warm herbal teas"]',
 '["cold foods", "ice cream", "frozen drinks", "raw salads", "excessive dairy", "bread", "pasta", "heavy carbs", "processed foods", "mushrooms"]',
 '["depression", "isolation", "sluggish metabolism", "constipation", "respiratory conditions", "sinusitis", "obesity", "low motivation"]',
 '["Winter: Most challenging - maintain warmth.", "Summer: Slightly increase activity.", "Spring: Perfect for renewal practices.", "Autumn: Build momentum gradually."]',
 '{"type": "gentle activation", "duration": "25-35 minutes", "frequency": "4-5x/week", "activities": ["short walks", "light stretching", "tai chi", "dancing alone"], "focus": "build momentum gradually"}',
 '{"hours": 9, "recommendation": "Extra sleep often needed", "tips": ["Morning sunlight exposure", "Gradual wake routine", "Avoid late sleeping"]}',
 '{"focus": "Counter isolation with gentle connection", "practices": ["Small social gatherings", "Creative pursuits", "Nature exposure", "Volunteering", "Pet therapy"], "avoid": ["complete isolation", "rumination"]}');

-- ============================================
-- QUIZ QUESTIONS (25 Questions)
-- Each option maps to a temperament type
-- ============================================

INSERT INTO quiz_questions (question_text, category, options, display_order) VALUES
('How would you describe your typical energy levels throughout the day?', 'Energy', 
 '[{"text": "High energy, I am active and enthusiastic most of the day", "temperament": "Sanguinous"}, {"text": "Strong energy but can flag by evening, I am intense and focused", "temperament": "Bilious"}, {"text": "Moderate energy, I pace myself and maintain steady levels", "temperament": "Phlegmatic"}, {"text": "Variable energy, I often feel tired and need rest", "temperament": "Melancholic"}]', 1),

('How do you typically respond to stress?', 'Stress Response',
 '[{"text": "I talk it out with others and seek social support", "temperament": "Sanguinous"}, {"text": "I become more driven and want to solve the problem immediately", "temperament": "Bilious"}, {"text": "I feel overwhelmed and tend to withdraw", "temperament": "Phlegmatic"}, {"text": "I analyze the situation thoroughly before responding", "temperament": "Melancholic"}]', 2),

('What is your typical sleep pattern?', 'Sleep',
 '[{"text": "I sleep easily and wake up refreshed, sometimes too much", "temperament": "Phlegmatic"}, {"text": "I have trouble switching off my mind, often light sleeper", "temperament": "Bilious"}, {"text": "I sleep well but could sleep more if allowed", "temperament": "Sanguinous"}, {"text": "I need a lot of sleep and have difficulty waking", "temperament": "Melancholic"}]', 3),

('How would you describe your skin type?', 'Physical',
 '[{"text": "Warm, flushed, prone to redness and oiliness", "temperament": "Sanguinous"}, {"text": "Oily, prone to acne and inflammation", "temperament": "Bilious"}, {"text": "Cool, pale, prone to puffiness and water retention", "temperament": "Phlegmatic"}, {"text": "Dry, prone to flakiness and sensitivity", "temperament": "Melancholic"}]', 4),

('How do you feel in hot weather?', 'Weather',
 '[{"text": "I struggle with heat, feel sluggish and uncomfortable", "temperament": "Phlegmatic"}, {"text": "I enjoy the warmth but feel I need to cool down often", "temperament": "Bilious"}, {"text": "I love the heat and feel most alive in summer", "temperament": "Sanguinous"}, {"text": "I adapt reasonably well but prefer cooler environments", "temperament": "Melancholic"}]', 5),

('How do you typically approach food and eating?', 'Diet',
 '[{"text": "I have a hearty appetite and enjoy variety in meals", "temperament": "Sanguinous"}, {"text": "I eat regularly but not excessively, prefer quality over quantity", "temperament": "Bilious"}, {"text": "I can skip meals easily and sometimes forget to eat", "temperament": "Melancholic"}, {"text": "I enjoy food but can go without if needed, prefer lighter meals", "temperament": "Phlegmatic"}]', 6),

('How would you describe your typical body build?', 'Physical',
 '[{"text": "Well-rounded, I gain weight easily especially around the waist", "temperament": "Phlegmatic"}, {"text": "Athletic, I build muscle easily and stay relatively lean", "temperament": "Bilious"}, {"text": "Average build with soft tissues, I gain weight in hips and thighs", "temperament": "Sanguinous"}, {"text": "Thin, I have difficulty gaining weight", "temperament": "Melancholic"}]', 7),

('How do you interact in social situations?', 'Social',
 '[{"text": "I am the life of the party and enjoy meeting new people", "temperament": "Sanguinous"}, {"text": "I take charge and enjoy leading discussions", "temperament": "Bilious"}, {"text": "I prefer smaller groups and listening rather than talking", "temperament": "Melancholic"}, {"text": "I am friendly but prefer to observe before engaging", "temperament": "Phlegmatic"}]', 8),

('How do you handle criticism?', 'Emotional',
 '[{"text": "It bounces off me, I shrug it off and move on", "temperament": "Sanguinous"}, {"text": "I can become defensive and may react with frustration", "temperament": "Bilious"}, {"text": "I take it personally and need time to process", "temperament": "Melancholic"}, {"text": "I listen calmly and consider whether it has merit", "temperament": "Phlegmatic"}]', 9),

('How would you describe your memory?', 'Mental',
 '[{"text": "I remember the big picture and overall experiences well", "temperament": "Sanguinous"}, {"text": "I have a sharp, detail-oriented memory", "temperament": "Melancholic"}, {"text": "I remember things that need to be done but sometimes forget names", "temperament": "Phlegmatic"}, {"text": "I have excellent recall for facts and figures", "temperament": "Bilious"}]', 10),

('How do you react to changes in routine?', 'Lifestyle',
 '[{"text": "I embrace change and enjoy trying new things", "temperament": "Sanguinous"}, {"text": "I prefer routine but can adapt when necessary", "temperament": "Phlegmatic"}, {"text": "I resist change and prefer familiar patterns", "temperament": "Melancholic"}, {"text": "I actually enjoy disruption and welcome new challenges", "temperament": "Bilious"}]', 11),

('How do you describe your typical mood?', 'Emotional',
 '[{"text": "Generally cheerful, I see the glass as half full", "temperament": "Sanguinous"}, {"text": "Can be intense, I have strong reactions to things", "temperament": "Bilious"}, {"text": "Even-keeled, I am rarely extremely happy or sad", "temperament": "Phlegmatic"}, {"text": "Thoughtful, I lean toward introspection and can be moody", "temperament": "Melancholic"}]', 12),

('How would you describe your digestive system?', 'Digestion',
 '[{"text": "I have a strong digestion but sometimes eat too quickly", "temperament": "Bilious"}, {"text": "I tend toward bloating and sluggish digestion", "temperament": "Phlegmatic"}, {"text": "I have a sensitive stomach and need to be careful with food", "temperament": "Melancholic"}, {"text": "My digestion is generally good with a healthy appetite", "temperament": "Sanguinous"}]', 13),

('How do you handle physical pain?', 'Pain',
 '[{"text": "I tend to ignore it and push through", "temperament": "Bilious"}, {"text": "I am very sensitive to pain and seek relief quickly", "temperament": "Sanguinous"}, {"text": "I have a high pain threshold and can endure quite a bit", "temperament": "Phlegmatic"}, {"text": "I analyze pain and try to understand its cause", "temperament": "Melancholic"}]', 14),

('How do you feel about exercise?', 'Exercise',
 '[{"text": "I enjoy it and need regular activity to feel good", "temperament": "Bilious"}, {"text": "I need motivation but feel better after moving", "temperament": "Phlegmatic"}, {"text": "I love social sports and group activities", "temperament": "Sanguinous"}, {"text": "I prefer solitary activities like yoga or walking", "temperament": "Melancholic"}]', 15),

('How do you make decisions?', 'Decision Making',
 '[{"text": "I decide quickly and act on instinct", "temperament": "Sanguinous"}, {"text": "I weigh all options carefully before deciding", "temperament": "Melancholic"}, {"text": "I consider impact on others before deciding", "temperament": "Phlegmatic"}, {"text": "I make decisions decisively, sometimes without hesitation", "temperament": "Bilious"}]', 16),

('How would you describe your creativity?', 'Creativity',
 '[{"text": "Very creative, I have lots of ideas and enjoy brainstorming", "temperament": "Sanguinous"}, {"text": "Creative in a focused, methodical way", "temperament": "Melancholic"}, {"text": "More practical creativity, solving real-world problems", "temperament": "Bilious"}, {"text": "I appreciate creativity but am not particularly creative myself", "temperament": "Phlegmatic"}]', 17),

('How do you feel in cold weather?', 'Weather',
 '[{"text": "I feel the cold deeply and struggle to warm up", "temperament": "Phlegmatic"}, {"text": "I adapt reasonably well, layer up as needed", "temperament": "Sanguinous"}, {"text": "I actually enjoy cooler weather and feel most comfortable", "temperament": "Melancholic"}, {"text": "I dislike the cold and feel stiff and achy", "temperament": "Bilious"}]', 18),

('How would you describe your relationships?', 'Relationships',
 '[{"text": "I have many friends and enjoy deep connections", "temperament": "Sanguinous"}, {"text": "I have a few close friends and prefer quality over quantity", "temperament": "Melancholic"}, {"text": "I am a loyal friend who values harmony", "temperament": "Phlegmatic"}, {"text": "I am a strong leader in relationships", "temperament": "Bilious"}]', 19),

('How do you react when things go wrong?', 'Stress',
 '[{"text": "I get frustrated and may show my irritation", "temperament": "Bilious"}, {"text": "I tend to get sad and withdraw", "temperament": "Melancholic"}, {"text": "I adapt and find solutions quickly", "temperament": "Sanguinous"}, {"text": "I become quieter and need support from others", "temperament": "Phlegmatic"}]', 20),

('How do you feel about being alone?', 'Social',
 '[{"text": "I value my solitude and recharge when alone", "temperament": "Melancholic"}, {"text": "I enjoy my own company but also love being with others", "temperament": "Phlegmatic"}, {"text": "I prefer being around people and can get lonely alone", "temperament": "Sanguinous"}, {"text": "Being alone can make me feel restless", "temperament": "Bilious"}]', 21),

('How would you describe your work style?', 'Work',
 '[{"text": "I work in bursts of energy with periods of rest", "temperament": "Sanguinous"}, {"text": "I work steadily at a consistent pace", "temperament": "Phlegmatic"}, {"text": "I work hard and can become obsessed with tasks", "temperament": "Bilious"}, {"text": "I am thorough and careful, sometimes too slow", "temperament": "Melancholic"}]', 22),

('How do you respond to conflict?', 'Conflict',
 '[{"text": "I avoid direct conflict and prefer harmony", "temperament": "Phlegmatic"}, {"text": "I engage directly and can be confrontational", "temperament": "Bilious"}, {"text": "I get upset but often suppress my feelings", "temperament": "Melancholic"}, {"text": "I try to smooth things over with charm", "temperament": "Sanguinous"}]', 23),

('How do you feel about routine?', 'Lifestyle',
 '[{"text": "I thrive on routine and feel lost without it", "temperament": "Melancholic"}, {"text": "I need some structure but enjoy flexibility", "temperament": "Phlegmatic"}, {"text": "I find routine boring and love spontaneity", "temperament": "Sanguinous"}, {"text": "I create my own structure around goals", "temperament": "Bilious"}]', 24),

('How would you describe your ideal environment?', 'Environment',
 '[{"text": "Warm, social, stimulating with lots of activity", "temperament": "Sanguinous"}, {"text": "Cool, organized, quiet and peaceful", "temperament": "Melancholic"}, {"text": "Temperate, balanced, with nature around", "temperament": "Phlegmatic"}, {"text": "Challenging, dynamic, with clear goals", "temperament": "Bilious"}]', 25);

-- ============================================
-- EXAMPLE PREMIUM CONTENT (for 2 combinations)
-- ============================================

INSERT INTO premium_content (temperament_combination_id, month, year, content) VALUES
(1, 1, 2025, 
 '{"food_guide": "Start the year with light, cooling foods. Focus on fresh fruits, vegetables, and hydration. Avoid heavy meats and spicy foods.", 
   "seasonal_protocol": "January focus: Gentle start with green juices and raw foods. Avoid alcohol and caffeine.", 
   "exercise": "Swimming and water aerobics. 30 minutes, 4x/week.",
   "sleep": "Maintain 7 hours. Cool room temperature.",
   "emotional_wellness": "Practice patience. Journal your experiences."}'),

(1, 2, 2025,
 '{"food_guide": "Continue with light foods. Add steamed vegetables and quinoa for sustained energy.",
   "seasonal_protocol": "February: Heart health awareness. Reduce salt intake.",
   "exercise": "Brisk walking 40 minutes, 5x/week. Include stretching.",
   "sleep": "Consistent bedtime around 10pm.",
   "emotional_wellness": "Channel enthusiasm into creative projects."}'),

(5, 1, 2025,
 '{"food_guide": "Nourishing, moistening foods. Bone broth, avocado, pears, cooked vegetables.",
   "seasonal_protocol": "January: Combat burnout. Prioritize rest and self-care.",
   "exercise": "Gentle yoga 30 minutes, 3x/week. Avoid overexertion.",
   "sleep": "8-9 hours. Early bedtime essential.",
   "emotional_wellness": "Set boundaries. Practice self-compassion. Seek support when needed."}'),

(5, 2, 2025,
 '{"food_guide": "Continue nourishing foods. Add warming spices like cinnamon and ginger.",
   "seasonal_protocol": "February: Prevent overthinking. Mindful practices daily.",
   "exercise": "Meditative walking in nature, 25 minutes, 4x/week.",
   "sleep": "Maintain 8.5+ hours. Wind-down ritual before bed.",
   "emotional_wellness": "Counter isolation with small social gatherings. Creative pursuits."}');

-- ============================================
-- EXAMPLE MONTHLY HEALTH FOCUS
-- ============================================

INSERT INTO monthly_health_focus (month_year, temperament_combination_id, tip_content) VALUES
('2025-01', 1, 'Focus on hydration and cooling the body. Start with a glass of room temperature water with lemon each morning.'),
('2025-01', 5, 'Prioritize rest and recovery. January is a critical month for preventing burnout.'),
('2025-02', 1, 'Heart health awareness. Monitor blood pressure and reduce sodium intake.'),
('2025-02', 5, 'Emotional balance through gentle social connection. Small gatherings over isolation.');