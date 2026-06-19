"""
Initialize the TibbWell database and seed with data
Run this script to create the SQLite database and load all seed data
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.database import engine, Base, SessionLocal, create_tables
from api.database import (
    User, QuizQuestion, QuizResult, Temperament, 
    TemperamentCombination, PremiumContent, MonthlyHealthFocus, AdminUser
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

# 25 Quiz Questions covering mizaaj (temperament) assessment
QUIZ_QUESTIONS_DATA = [
    {
        "id": 1,
        "question_text": "How would you describe your body frame?",
        "category": "Body Frame",
        "options": [
            {"text": "Well-rounded with soft curves, tendency to gain weight easily", "temperament": "Phlegmatic"},
            {"text": "Athletic and muscular, lean and strong", "temperament": "Bilious"},
            {"text": "Average build, can gain or lose weight depending on diet", "temperament": "Sanguinous"},
            {"text": "Thin and slender, difficulty gaining weight", "temperament": "Melancholic"}
        ],
        "display_order": 1
    },
    {
        "id": 2,
        "question_text": "How would you describe your skin texture?",
        "category": "Skin Texture",
        "options": [
            {"text": "Oily and warm to touch, prone to breakouts", "temperament": "Sanguinous"},
            {"text": "Dry and rough, may flake or feel tight", "temperament": "Melancholic"},
            {"text": "Soft and supple with good moisture", "temperament": "Phlegmatic"},
            {"text": "Combination skin, oily T-zone", "temperament": "Bilious"}
        ],
        "display_order": 2
    },
    {
        "id": 3,
        "question_text": "How would you describe your complexion?",
        "category": "Complexion",
        "options": [
            {"text": "Fair with a rosy flush, flushes easily", "temperament": "Sanguinous"},
            {"text": "Olive or medium with a warm undertone", "temperament": "Bilious"},
            {"text": "Pale or cool-toned, may have pink undertones", "temperament": "Phlegmatic"},
            {"text": "Darker or sallow, may have dull areas", "temperament": "Melancholic"}
        ],
        "display_order": 3
    },
    {
        "id": 4,
        "question_text": "Which climate do you feel most comfortable in?",
        "category": "Climatic Preferences",
        "options": [
            {"text": "Cool weather, I prefer autumn and winter", "temperament": "Melancholic"},
            {"text": "Warm weather, I thrive in summer", "temperament": "Sanguinous"},
            {"text": "Mild climate, I don't like extremes", "temperament": "Phlegmatic"},
            {"text": "I adapt well to any climate", "temperament": "Bilious"}
        ],
        "display_order": 4
    },
    {
        "id": 5,
        "question_text": "What types of foods do you typically crave?",
        "category": "Food Cravings",
        "options": [
            {"text": "Cold foods like ice cream, salads, and chilled drinks", "temperament": "Phlegmatic"},
            {"text": "Spicy foods, hot peppers, and flavorful seasonings", "temperament": "Bilious"},
            {"text": "Sweet foods, fruits, and carbohydrate-rich meals", "temperament": "Sanguinous"},
            {"text": "Bitter foods like dark leafy greens, coffee, and tea", "temperament": "Melancholic"}
        ],
        "display_order": 5
    },
    {
        "id": 6,
        "question_text": "How would you describe your appetite?",
        "category": "Food Cravings",
        "options": [
            {"text": "Strong appetite, I can eat large amounts", "temperament": "Sanguinous"},
            {"text": "Moderate appetite, I eat to live not live to eat", "temperament": "Phlegmatic"},
            {"text": "Variable appetite, sometimes I forget to eat", "temperament": "Bilious"},
            {"text": "Light eater, I feel full quickly", "temperament": "Melancholic"}
        ],
        "display_order": 6
    },
    {
        "id": 7,
        "question_text": "What recurring health issues do you experience?",
        "category": "Recurring Health Problems",
        "options": [
            {"text": "Digestive issues like bloating, gas, and sluggish digestion", "temperament": "Phlegmatic"},
            {"text": "Inflammatory issues like headaches, joint pain, or skin eruptions", "temperament": "Bilious"},
            {"text": "Respiratory issues, coughs, or sinus problems", "temperament": "Sanguinous"},
            {"text": "Anxiety, insomnia, or nervous stomach", "temperament": "Melancholic"}
        ],
        "display_order": 7
    },
    {
        "id": 8,
        "question_text": "How is your digestive system?",
        "category": "Recurring Health Problems",
        "options": [
            {"text": "Strong digestion, rarely experience digestive issues", "temperament": "Bilious"},
            {"text": "Sensitive stomach, need to be careful with food", "temperament": "Melancholic"},
            {"text": "Slow digestion, often feel heavy after meals", "temperament": "Phlegmatic"},
            {"text": "Variable digestion, depends on what I eat", "temperament": "Sanguinous"}
        ],
        "display_order": 8
    },
    {
        "id": 9,
        "question_text": "Describe your typical sleep pattern",
        "category": "Sleep Patterns",
        "options": [
            {"text": "Deep sleeper, 7-8 hours, wake refreshed", "temperament": "Phlegmatic"},
            {"text": "Light sleeper, often think at night, need 6-7 hours", "temperament": "Bilious"},
            {"text": "Average sleeper, sometimes oversleep, need 7-9 hours", "temperament": "Sanguinous"},
            {"text": "Restless sleeper, racing thoughts, often tired", "temperament": "Melancholic"}
        ],
        "display_order": 9
    },
    {
        "id": 10,
        "question_text": "How do you feel upon waking in the morning?",
        "category": "Sleep Patterns",
        "options": [
            {"text": "Full of energy, ready to start the day immediately", "temperament": "Sanguinous"},
            {"text": "Stiff and slow to start, need time to warm up", "temperament": "Phlegmatic"},
            {"text": "Grumpy and irritable until I've had coffee", "temperament": "Bilious"},
            {"text": "Already thinking about the day ahead, mind is active", "temperament": "Melancholic"}
        ],
        "display_order": 10
    },
    {
        "id": 11,
        "question_text": "How would you describe your speech style?",
        "category": "Speech Style",
        "options": [
            {"text": "Fast-talking, enthusiastic, often speak before thinking", "temperament": "Sanguinous"},
            {"text": "Direct and assertive, get to the point quickly", "temperament": "Bilious"},
            {"text": "Soft-spoken, thoughtful, choose words carefully", "temperament": "Phlegmatic"},
            {"text": "Detailed and analytical, may speak in long sentences", "temperament": "Melancholic"}
        ],
        "display_order": 11
    },
    {
        "id": 12,
        "question_text": "How often do you speak compared to listening?",
        "category": "Speech Style",
        "options": [
            {"text": "I speak more than I listen", "temperament": "Sanguinous"},
            {"text": "I balance speaking and listening equally", "temperament": "Bilious"},
            {"text": "I prefer to listen and observe", "temperament": "Phlegmatic"},
            {"text": "I listen more but when I speak it's well-considered", "temperament": "Melancholic"}
        ],
        "display_order": 12
    },
    {
        "id": 13,
        "question_text": "How would you describe your typical personality?",
        "category": "Personality Traits",
        "options": [
            {"text": "Sociable, cheerful, and always looking for fun", "temperament": "Sanguinous"},
            {"text": "Competitive, ambitious, and goal-oriented", "temperament": "Bilious"},
            {"text": "Easy-going, reliable, and patient", "temperament": "Phlegmatic"},
            {"text": "Introverted, creative, and deep-thinking", "temperament": "Melancholic"}
        ],
        "display_order": 13
    },
    {
        "id": 14,
        "question_text": "How do you handle stress?",
        "category": "Personality Traits",
        "options": [
            {"text": "I talk to friends and socialize to relieve stress", "temperament": "Sanguinous"},
            {"text": "I become more focused and tackle problems head-on", "temperament": "Bilious"},
            {"text": "I feel overwhelmed and withdraw temporarily", "temperament": "Phlegmatic"},
            {"text": "I analyze and try to understand the root cause", "temperament": "Melancholic"}
        ],
        "display_order": 14
    },
    {
        "id": 15,
        "question_text": "How do you make decisions?",
        "category": "Personality Traits",
        "options": [
            {"text": "Quick decisions based on gut feeling", "temperament": "Sanguinous"},
            {"text": "Fast decisions after weighing pros and cons", "temperament": "Bilious"},
            {"text": "Slow decisions, consider how it affects others", "temperament": "Phlegmatic"},
            {"text": "Very deliberate, analyze all possibilities first", "temperament": "Melancholic"}
        ],
        "display_order": 15
    },
    {
        "id": 16,
        "question_text": "How would you describe your emotional nature?",
        "category": "Emotional Tendencies",
        "options": [
            {"text": "Happy and optimistic most of the time", "temperament": "Sanguinous"},
            {"text": "Intense emotions, can be quick to anger", "temperament": "Bilious"},
            {"text": "Calm and even-keeled, rarely upset", "temperament": "Phlegmatic"},
            {"text": "Deep emotions, can be melancholy at times", "temperament": "Melancholic"}
        ],
        "display_order": 16
    },
    {
        "id": 17,
        "question_text": "How do you react when things go wrong?",
        "category": "Emotional Tendencies",
        "options": [
            {"text": "I get frustrated but bounce back quickly", "temperament": "Sanguinous"},
            {"text": "I get angry and then immediately look for solutions", "temperament": "Bilious"},
            {"text": "I become quiet and need support from others", "temperament": "Phlegmatic"},
            {"text": "I withdraw and think deeply about what happened", "temperament": "Melancholic"}
        ],
        "display_order": 17
    },
    {
        "id": 18,
        "question_text": "How do you handle criticism?",
        "category": "Emotional Tendencies",
        "options": [
            {"text": "It doesn't bother me much, I shrug it off", "temperament": "Sanguinous"},
            {"text": "I may become defensive or argumentative", "temperament": "Bilious"},
            {"text": "I take it personally but don't show it much", "temperament": "Phlegmatic"},
            {"text": "I think about it deeply and may take it to heart", "temperament": "Melancholic"}
        ],
        "display_order": 18
    },
    {
        "id": 19,
        "question_text": "How would you describe your work style?",
        "category": "Personality Traits",
        "options": [
            {"text": "Work in bursts of energy, enthusiastic starter", "temperament": "Sanguinous"},
            {"text": "Consistent and persistent, steady worker", "temperament": "Bilious"},
            {"text": "Methodical and thorough, quality focused", "temperament": "Phlegmatic"},
            {"text": "Perfectionist, may take longer to complete tasks", "temperament": "Melancholic"}
        ],
        "display_order": 19
    },
    {
        "id": 20,
        "question_text": "How do you feel about routine?",
        "category": "Personality Traits",
        "options": [
            {"text": "I find routine boring, I need variety", "temperament": "Sanguinous"},
            {"text": "I create my own structure around goals", "temperament": "Bilious"},
            {"text": "I thrive with routine and clear expectations", "temperament": "Phlegmatic"},
            {"text": "I resist routine but may create rituals", "temperament": "Melancholic"}
        ],
        "display_order": 20
    },
    {
        "id": 21,
        "question_text": "How do you interact in social situations?",
        "category": "Social Behavior",
        "options": [
            {"text": "I am the center of attention, love meeting new people", "temperament": "Sanguinous"},
            {"text": "I take charge and enjoy leading discussions", "temperament": "Bilious"},
            {"text": "I enjoy peaceful gatherings with close friends", "temperament": "Phlegmatic"},
            {"text": "I observe first, then participate thoughtfully", "temperament": "Melancholic"}
        ],
        "display_order": 21
    },
    {
        "id": 22,
        "question_text": "How do you feel about being alone?",
        "category": "Social Behavior",
        "options": [
            {"text": "I can be alone but prefer company", "temperament": "Sanguinous"},
            {"text": "I enjoy solitude for recharging", "temperament": "Bilious"},
            {"text": "I value my independence and time alone", "temperament": "Phlegmatic"},
            {"text": "I can feel lonely even in a crowd", "temperament": "Melancholic"}
        ],
        "display_order": 22
    },
    {
        "id": 23,
        "question_text": "What is your approach to exercise?",
        "category": "Physical Activity",
        "options": [
            {"text": "I enjoy social sports and group fitness classes", "temperament": "Sanguinous"},
            {"text": "I need vigorous exercise to feel good", "temperament": "Bilious"},
            {"text": "I prefer gentle exercise like walking or yoga", "temperament": "Phlegmatic"},
            {"text": "I struggle to motivate myself to exercise", "temperament": "Melancholic"}
        ],
        "display_order": 23
    },
    {
        "id": 24,
        "question_text": "How would you describe your memory?",
        "category": "Cognitive Style",
        "options": [
            {"text": "I remember experiences and emotions well", "temperament": "Sanguinous"},
            {"text": "I have good recall for facts and details", "temperament": "Bilious"},
            {"text": "I remember things I need to do practically", "temperament": "Phlegmatic"},
            {"text": "I have excellent long-term memory for everything", "temperament": "Melancholic"}
        ],
        "display_order": 24
    },
    {
        "id": 25,
        "question_text": "What motivates you most?",
        "category": "Emotional Tendencies",
        "options": [
            {"text": "Recognition, praise, and social approval", "temperament": "Sanguinous"},
            {"text": "Achievement, challenge, and personal growth", "temperament": "Bilious"},
            {"text": "Peace, stability, and harmonious relationships", "temperament": "Phlegmatic"},
            {"text": "Depth, meaning, and understanding", "temperament": "Melancholic"}
        ],
        "display_order": 25
    }
]

# Temperaments data
TEMPERAMENTS_DATA = [
    {
        "name": "Sanguinous",
        "quality": "Hot & Moist",
        "element": "Air",
        "description": "The Sanguinous temperament is characterized by warmth and moisture. People with this constitution tend to be social, enthusiastic, creative, and optimistic. They have a tendency toward weight gain, may experience circulatory issues, and often have a strong appetite.",
        "traits": ["sociable", "optimistic", "creative", "enthusiastic", "talkative", "generous", "warm-hearted", "spontaneous"]
    },
    {
        "name": "Bilious",
        "quality": "Hot & Dry",
        "element": "Fire",
        "description": "The Bilious temperament is characterized by heat and dryness. People with this constitution tend to be ambitious, determined, decisive, and passionate. They may experience inflammation, irritability, and have a strong metabolism with a tendency toward weight loss.",
        "traits": ["ambitious", "determined", "decisive", "passionate", "courageous", "leadership", "assertive", "intense"]
    },
    {
        "name": "Phlegmatic",
        "quality": "Cold & Moist",
        "element": "Water",
        "description": "The Phlegmatic temperament is characterized by coldness and moisture. People with this constitution tend to be calm, thoughtful, diplomatic, and patient. They may experience sluggishness, weight gain, and have a slower metabolism.",
        "traits": ["calm", "thoughtful", "diplomatic", "patient", "reliable", "easy-going", "observant", "sympathetic"]
    },
    {
        "name": "Melancholic",
        "quality": "Cold & Dry",
        "element": "Earth",
        "description": "The Melancholic temperament is characterized by coldness and dryness. People with this constitution tend to be analytical, detail-oriented, perfectionist, and creative. They may experience digestive issues, anxiety, and have a tendency toward weight loss.",
        "traits": ["analytical", "detail-oriented", "perfectionist", "creative", "introverted", "conscientious", "logical", "sensitive"]
    }
]

# Temperament Combinations data
COMBINATIONS_DATA = [
    {
        "name": "Sanguinous-Bilious",
        "description": "A dynamic combination of Hot & Moist with Hot & Dry. Characterized by high energy, ambition, and social charisma with a tendency toward inflammation and urgency.",
        "foods_to_eat": ["fresh fruits", "vegetables", "leafy greens", "cucumbers", "lettuce", "zucchini", "coconut water", "rose water", "mint tea", "barley water"],
        "foods_to_avoid": ["spicy foods", "fried foods", "red meat", "processed foods", "caffeine", "alcohol", "hot spices", "turmeric", "ginger", "garlic"],
        "disease_risks": ["hypertension", "heart disease", "stroke", "inflammatory conditions", "skin eruptions", "acne", "migraines", "ulcers"],
        "seasonal_tips": ["Summer: Stay cool with melon and cucumber. Avoid sun exposure.", "Spring: Gentle detox with green juices.", "Winter: Balance with warm soups.", "Autumn: Focus on hydration."],
        "exercise_plan": {"type": "moderate cardio", "duration": "30-45 minutes", "frequency": "4-5x/week", "activities": ["swimming", "walking", "yoga", "cycling"], "avoid": "intense competitive sports"},
        "sleep_plan": {"hours": 7, "recommendation": "Maintain consistent sleep schedule", "tips": ["Avoid screens before bed", "Keep room cool", "Light blanket only"]},
        "emotional_guide": {"focus": "Channel energy constructively", "practices": ["Set realistic goals", "Practice patience", "Take breaks", "Express emotions healthily"], "avoid": ["overcommitting", "suppressing feelings"]}
    },
    {
        "name": "Sanguinous-Phlegmatic",
        "description": "A balanced combination of Hot & Moist with Cold & Moist. Characterized by sociability, patience, and creativity with a tendency toward sluggishness and weight gain.",
        "foods_to_eat": ["light proteins", "fish", "turkey", "chicken", "beans", "lentils", "quinoa", "steamed vegetables", "green tea", "ginger tea"],
        "foods_to_avoid": ["heavy carbohydrates", "dairy", "bread", "pasta", "sugar", "processed snacks", "frozen foods", "cold drinks", "ice cream"],
        "disease_risks": ["obesity", "diabetes", "respiratory issues", "sinusitis", "catarrh", "edema", "sluggish metabolism", "depression"],
        "seasonal_tips": ["Winter: Active exercise to combat sluggishness.", "Summer: Light activities, avoid overheating.", "Spring: Natural detox with bitter foods.", "Autumn: Boost immunity."],
        "exercise_plan": {"type": "active lifestyle", "duration": "40-60 minutes", "frequency": "5-6x/week", "activities": ["brisk walking", "light jogging", "dancing", "gardening"], "focus": "combat sluggishness"},
        "sleep_plan": {"hours": 8, "recommendation": "Prioritize quality sleep", "tips": ["Establish bedtime routine", "Avoid late meals", "Use breathing exercises"]},
        "emotional_guide": {"focus": "Balance social needs with alone time", "practices": ["Set boundaries", "Practice saying no", "Schedule rest", "Cultivate inner peace"], "avoid": ["over-socializing", "isolation"]}
    },
    {
        "name": "Sanguinous-Melancholic",
        "description": "A contrasting combination of Hot & Moist with Cold & Dry. Characterized by creativity, social skills, and analytical ability with internal tension.",
        "foods_to_eat": ["balanced diet", "mixed fruits", "vegetables", "nuts", "seeds", "olive oil", "fish", "whole grains", "herbal teas", "honey"],
        "foods_to_avoid": ["extremes in diet", "very spicy food", "very cold food", "processed foods", "artificial additives", "excessive red meat", "excessive sugar"],
        "disease_risks": ["digestive issues", "IBS", "anxiety", "depression", "nutritional deficiencies", "fatigue", "constipation", "mood swings"],
        "seasonal_tips": ["Winter: Comfort foods in moderation.", "Summer: Cooling foods prevent burnout.", "Spring: Gentle cleanse.", "Autumn: Stabilize routine."],
        "exercise_plan": {"type": "balanced exercise", "duration": "30-45 minutes", "frequency": "4-5x/week", "activities": ["yoga", "pilates", "swimming", "walking in nature"], "focus": "reduce stress"},
        "sleep_plan": {"hours": 7.5, "recommendation": "Consistent sleep routine essential", "tips": ["Wind down with reading", "Meditation before bed", "Comfortable sleep environment"]},
        "emotional_guide": {"focus": "Integrate analytical and creative thinking", "practices": ["Journaling", "Mindfulness meditation", "Creative expression", "Emotional awareness"], "avoid": ["overthinking", "emotional suppression"]}
    },
    {
        "name": "Bilious-Phlegmatic",
        "description": "A contrasting combination of Hot & Dry with Cold & Moist. Characterized by determination tempered by patience, with internal balance challenges.",
        "foods_to_eat": ["cooling foods", "cucumbers", "melons", "zucchini", "coconut", "butter", "olive oil", "rice", "oatmeal", "marshmallow root tea"],
        "foods_to_avoid": ["very hot spices", "chili", "turmeric", "ginger", "garlic", "vinegar", "pickles", "fermented foods", "excessive salt", "alcohol"],
        "disease_risks": ["indigestion", "bloating", "alternating constipation/diarrhea", "skin conditions", "mood swings", "inflammation", "arthritis"],
        "seasonal_tips": ["Winter: Warm cooked foods.", "Summer: Stay hydrated with cooling foods.", "Spring: Gradual transition foods.", "Autumn: Build immunity."],
        "exercise_plan": {"type": "gentle but consistent", "duration": "35-45 minutes", "frequency": "4-5x/week", "activities": ["tai chi", "gentle yoga", "walking", "swimming"], "focus": "avoid overheating"},
        "sleep_plan": {"hours": 8, "recommendation": "Quality rest essential for balance", "tips": ["Cool bath before bed", "Light dinner", "Consistent schedule"]},
        "emotional_guide": {"focus": "Balance ambition with patience", "practices": ["Pause before reacting", "Practice deep breathing", "Set realistic deadlines", "Accept imperfection"], "avoid": ["perfectionism", "impatience with self"]}
    },
    {
        "name": "Bilious-Melancholic",
        "description": "A powerful combination of Hot & Dry with Cold & Dry. Characterized by intense intellect, ambition, and analytical thinking with a tendency toward burnout.",
        "foods_to_eat": ["moistening foods", "avocados", "pears", "apples", "peas", "beans", "zucchini", "cucumber", "bone broth", "slippery elm tea"],
        "foods_to_avoid": ["very hot foods", "chili", "paprika", "cayenne", "curry", "heavy spices", "coffee", "energy drinks", "processed meats", "excessive salt"],
        "disease_risks": ["burnout", "anxiety", "depression", "digestive ulcers", "IBS", "chronic fatigue", "insomnia", "heart conditions", "hypertension"],
        "seasonal_tips": ["Winter: Extra rest and nourishing foods.", "Summer: Cooling diet critical.", "Spring: Gradual increase in activity.", "Autumn: Prepare for intensity."],
        "exercise_plan": {"type": "mindful exercise", "duration": "30-40 minutes", "frequency": "3-4x/week", "activities": ["yoga", "meditative walking", "swimming", "gentle cycling"], "focus": "avoid overexertion"},
        "sleep_plan": {"hours": 8.5, "recommendation": "Prioritize sleep above all", "tips": ["Early bedtime", "Wind-down ritual", "Avoid work in bedroom", "Magnesium supplementation"]},
        "emotional_guide": {"focus": "Manage intensity and prevent burnout", "practices": ["Regular breaks", "Set boundaries", "Practice self-compassion", "Seek support", "Laugh daily"], "avoid": ["overwork", "self-criticism", "isolation"]}
    },
    {
        "name": "Phlegmatic-Melancholic",
        "description": "A subdued combination of Cold & Moist with Cold & Dry. Characterized by depth, thoughtfulness, and contemplation with a tendency toward isolation and sluggishness.",
        "foods_to_eat": ["warming foods", "ginger", "cinnamon", "turmeric", "black pepper", "warm soups", "cooked vegetables", "lean proteins", "eggs", "warm herbal teas"],
        "foods_to_avoid": ["cold foods", "ice cream", "frozen drinks", "raw salads", "excessive dairy", "bread", "pasta", "heavy carbs", "processed foods", "mushrooms"],
        "disease_risks": ["depression", "isolation", "sluggish metabolism", "constipation", "respiratory conditions", "sinusitis", "obesity", "low motivation"],
        "seasonal_tips": ["Winter: Most challenging - maintain warmth.", "Summer: Slightly increase activity.", "Spring: Perfect for renewal practices.", "Autumn: Build momentum gradually."],
        "exercise_plan": {"type": "gentle activation", "duration": "25-35 minutes", "frequency": "4-5x/week", "activities": ["short walks", "light stretching", "tai chi", "dancing alone"], "focus": "build momentum gradually"},
        "sleep_plan": {"hours": 9, "recommendation": "Extra sleep often needed", "tips": ["Morning sunlight exposure", "Gradual wake routine", "Avoid late sleeping"]},
        "emotional_guide": {"focus": "Counter isolation with gentle connection", "practices": ["Small social gatherings", "Creative pursuits", "Nature exposure", "Volunteering", "Pet therapy"], "avoid": ["complete isolation", "rumination"]}
    }
]


def seed_database():
    """Seed the database with initial data"""
    print("Creating tables...")
    create_tables()
    
    db = SessionLocal()
    
    try:
        # Check if already seeded
        existing = db.query(QuizQuestion).first()
        if existing:
            print("Database already seeded. Skipping...")
            return
        
        print("Seeding quiz questions...")
        for q in QUIZ_QUESTIONS_DATA:
            question = QuizQuestion(
                id=q["id"],
                question_text=q["question_text"],
                category=q["category"],
                options=q["options"],
                display_order=q["display_order"]
            )
            db.add(question)
        
        print("Seeding temperaments...")
        for t in TEMPERAMENTS_DATA:
            temperament = Temperament(
                name=t["name"],
                quality=t["quality"],
                element=t["element"],
                description=t["description"],
                traits=t["traits"]
            )
            db.add(temperament)
        
        print("Seeding temperament combinations...")
        for c in COMBINATIONS_DATA:
            combination = TemperamentCombination(
                name=c["name"],
                description=c["description"],
                foods_to_eat=c["foods_to_eat"],
                foods_to_avoid=c["foods_to_avoid"],
                disease_risks=c["disease_risks"],
                seasonal_tips=c["seasonal_tips"],
                exercise_plan=c["exercise_plan"],
                sleep_plan=c["sleep_plan"],
                emotional_guide=c["emotional_guide"]
            )
            db.add(combination)
        
        print("Creating admin user...")
        admin = AdminUser(
            username="admin",
            password_hash=pwd_context.hash("3d5d511bd347b00e97ef851e"),
            is_admin=True
        )
        db.add(admin)
        
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()