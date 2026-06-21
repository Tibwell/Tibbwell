"""
TibbWell Backend API
FastAPI application entry point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from datetime import datetime

# Import routers
from api.auth import router as auth_router, pwd_context
from api.quiz import router as quiz_router
from api.premium import router as premium_router
from api.admin import router as admin_router
from api.chatbot import router as chatbot_router

# Application configuration
app = FastAPI(
    title="TibbWell API",
    description="Backend API for TibbWell - Traditional Unani Medicine Health Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS configuration - allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(quiz_router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(premium_router, prefix="/api/premium", tags=["Premium"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])
app.include_router(chatbot_router, prefix="/api/chatbot", tags=["Chatbot"])


@app.on_event("startup")
async def startup_db():
    """
    Run database migration and seeding on application startup.
    Creates tables if they don't exist and seeds initial data
    (temperaments, quiz questions, temperament combinations, admin user).
    Safe to run repeatedly — skips if data already exists.
    """
    from api.database import Base, engine, SessionLocal
    from api.database import (
        Temperament, QuizQuestion, TemperamentCombination, AdminUser
    )
    from api.auth import pwd_context
    import logging
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Step 1: Create all tables
    logger.info("Running database migration...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created/verified.")
    
    # Step 2: Seed data
    db = SessionLocal()
    try:
        # Check if already seeded
        existing_admin = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        if existing_admin:
            logger.info("Database already seeded. Skipping seed.")
            return
        
        logger.info("Seeding database...")
        
        # Seed temperaments
        temperaments_data = [
            {"name": "Sanguinous", "quality": "Hot & Wet", "element": "Air",
             "description": "The Sanguinous temperament is characterized by warmth and moisture. People with this constitution tend to be social, enthusiastic, creative, and optimistic.",
             "traits": ["Social", "Enthusiastic", "Creative", "Optimistic", "Outgoing"]},
            {"name": "Bilious", "quality": "Hot & Dry", "element": "Fire",
             "description": "The Bilious temperament is characterized by heat and dryness. People with this constitution tend to be ambitious, determined, decisive, and passionate.",
             "traits": ["Ambitious", "Determined", "Decisive", "Passionate", "Leadership"]},
            {"name": "Phlegmatic", "quality": "Cold & Wet", "element": "Water",
             "description": "The Phlegmatic temperament is characterized by coldness and moisture. People with this constitution tend to be calm, thoughtful, diplomatic, and patient.",
             "traits": ["Calm", "Thoughtful", "Diplomatic", "Patient", "Peaceful"]},
            {"name": "Melancholic", "quality": "Cold & Dry", "element": "Earth",
             "description": "The Melancholic temperament is characterized by coldness and dryness. People with this constitution tend to be analytical, detail-oriented, perfectionist, and creative.",
             "traits": ["Analytical", "Detail-oriented", "Perfectionist", "Creative", "Introspective"]},
        ]
        for t in temperaments_data:
            db.add(Temperament(**t))
        db.flush()
        
        # Get temperament IDs
        temp_map = {}
        for t in db.query(Temperament).all():
            temp_map[t.name] = t.id
        
        # Seed quiz questions
        questions_data = [
            {"question_text": "When you wake up in the morning, how do you usually feel?", "category": "Energy & Vitality", "display_order": 1, "options": [
                {"text": "Energetic and ready to go", "temperament": "Sanguinous"},
                {"text": "Warm and restless", "temperament": "Bilious"},
                {"text": "Slow to wake up, need time", "temperament": "Phlegmatic"},
                {"text": "Tired and sluggish", "temperament": "Melancholic"}
            ]},
            {"question_text": "What kind of weather do you prefer?", "category": "Climate Preference", "display_order": 2, "options": [
                {"text": "Mild and pleasant", "temperament": "Sanguinous"},
                {"text": "Cool weather", "temperament": "Bilious"},
                {"text": "Warm weather", "temperament": "Phlegmatic"},
                {"text": "Dry and cool", "temperament": "Melancholic"}
            ]},
            {"question_text": "How would you describe your skin?", "category": "Physical Characteristics", "display_order": 3, "options": [
                {"text": "Warm and moist", "temperament": "Sanguinous"},
                {"text": "Warm and dry", "temperament": "Bilious"},
                {"text": "Cool and moist", "temperament": "Phlegmatic"},
                {"text": "Cool and dry", "temperament": "Melancholic"}
            ]},
            {"question_text": "How is your appetite?", "category": "Digestion & Metabolism", "display_order": 4, "options": [
                {"text": "Good appetite, enjoy food", "temperament": "Sanguinous"},
                {"text": "Strong appetite, can eat anytime", "temperament": "Bilious"},
                {"text": "Moderate appetite", "temperament": "Phlegmatic"},
                {"text": "Variable appetite, picky", "temperament": "Melancholic"}
            ]},
            {"question_text": "How do you handle stress?", "category": "Emotional Response", "display_order": 5, "options": [
                {"text": "Stay positive and socialize", "temperament": "Sanguinous"},
                {"text": "Get angry and confront it", "temperament": "Bilious"},
                {"text": "Stay calm and avoid conflict", "temperament": "Phlegmatic"},
                {"text": "Worry and overthink", "temperament": "Melancholic"}
            ]},
            {"question_text": "What is your sleep pattern like?", "category": "Sleep Patterns", "display_order": 6, "options": [
                {"text": "Sleep well, wake refreshed", "temperament": "Sanguinous"},
                {"text": "Light sleeper, wake easily", "temperament": "Bilious"},
                {"text": "Heavy sleeper, love sleep", "temperament": "Phlegmatic"},
                {"text": "Trouble falling asleep", "temperament": "Melancholic"}
            ]},
            {"question_text": "How does your body react to cold weather?", "category": "Temperature Sensitivity", "display_order": 7, "options": [
                {"text": "I handle cold reasonably well", "temperament": "Sanguinous"},
                {"text": "I prefer cold weather, feel energetic", "temperament": "Bilious"},
                {"text": "I feel very cold and sluggish", "temperament": "Phlegmatic"},
                {"text": "Cold makes me feel more withdrawn", "temperament": "Melancholic"}
            ]},
            {"question_text": "How would you describe your social habits?", "category": "Social Behavior", "display_order": 8, "options": [
                {"text": "I love being around people", "temperament": "Sanguinous"},
                {"text": "I enjoy leading and organizing", "temperament": "Bilious"},
                {"text": "I prefer small groups or alone", "temperament": "Phlegmatic"},
                {"text": "I prefer solitude or one-on-one", "temperament": "Melancholic"}
            ]},
            {"question_text": "What kind of foods do you naturally crave?", "category": "Food Preferences", "display_order": 9, "options": [
                {"text": "Light and fresh foods", "temperament": "Sanguinous"},
                {"text": "Spicy and flavorful foods", "temperament": "Bilious"},
                {"text": "Comfort foods and sweets", "temperament": "Phlegmatic"},
                {"text": "Simple and plain foods", "temperament": "Melancholic"}
            ]},
            {"question_text": "How do you react to hot weather?", "category": "Climate Response", "display_order": 10, "options": [
                {"text": "Enjoy it moderately", "temperament": "Sanguinous"},
                {"text": "Feel irritable in heat", "temperament": "Bilious"},
                {"text": "Feel comfortable in warmth", "temperament": "Phlegmatic"},
                {"text": "Prefer to avoid heat", "temperament": "Melancholic"}
            ]},
            {"question_text": "What best describes your energy levels throughout the day?", "category": "Energy Pattern", "display_order": 11, "options": [
                {"text": "Consistently energetic", "temperament": "Sanguinous"},
                {"text": "Peak energy mid-day", "temperament": "Bilious"},
                {"text": "Slow but steady energy", "temperament": "Phlegmatic"},
                {"text": "Energy fluctuates greatly", "temperament": "Melancholic"}
            ]},
            {"question_text": "How do you typically react to disappointments?", "category": "Emotional Resilience", "display_order": 12, "options": [
                {"text": "Bounce back quickly", "temperament": "Sanguinous"},
                {"text": "Get frustrated and take action", "temperament": "Bilious"},
                {"text": "Accept it calmly", "temperament": "Phlegmatic"},
                {"text": "Dwell on it for a while", "temperament": "Melancholic"}
            ]},
            {"question_text": "What is your body frame like?", "category": "Physical Build", "display_order": 13, "options": [
                {"text": "Medium build, well-proportioned", "temperament": "Sanguinous"},
                {"text": "Lean and muscular", "temperament": "Bilious"},
                {"text": "Larger or softer build", "temperament": "Phlegmatic"},
                {"text": "Slender and delicate", "temperament": "Melancholic"}
            ]},
            {"question_text": "How do you handle decision making?", "category": "Decision Making", "display_order": 14, "options": [
                {"text": "Quick and intuitive decisions", "temperament": "Sanguinous"},
                {"text": "Decisive and confident", "temperament": "Bilious"},
                {"text": "Careful and deliberate", "temperament": "Phlegmatic"},
                {"text": "Analytical and cautious", "temperament": "Melancholic"}
            ]},
            {"question_text": "What type of exercise do you enjoy most?", "category": "Exercise Preference", "display_order": 15, "options": [
                {"text": "Dance, team sports, variety", "temperament": "Sanguinous"},
                {"text": "Competitive sports, intensity", "temperament": "Bilious"},
                {"text": "Walking, swimming, gentle movement", "temperament": "Phlegmatic"},
                {"text": "Yoga, pilates, individual activities", "temperament": "Melancholic"}
            ]},
            {"question_text": "How is your digestion generally?", "category": "Digestive Health", "display_order": 16, "options": [
                {"text": "Good digestion, regular", "temperament": "Sanguinous"},
                {"text": "Strong digestion, sometimes too fast", "temperament": "Bilious"},
                {"text": "Slow digestion, tendency to lethargy", "temperament": "Phlegmatic"},
                {"text": "Sensitive digestion, easily upset", "temperament": "Melancholic"}
            ]},
            {"question_text": "What best describes your typical mood?", "category": "M Disposition", "display_order": 17, "options": [
                {"text": "Cheerful and optimistic", "temperament": "Sanguinous"},
                {"text": "Intense and passionate", "temperament": "Bilious"},
                {"text": "Calm and content", "temperament": "Phlegmatic"},
                {"text": "Thoughtful and serious", "temperament": "Melancholic"}
            ]},
            {"question_text": "How do you react to pain or discomfort?", "category": "Pain Response", "display_order": 18, "options": [
                {"text": "Handle it well, stay positive", "temperament": "Sanguinous"},
                {"text": "Get frustrated and seek solutions", "temperament": "Bilious"},
                {"text": "Tolerate it quietly", "temperament": "Phlegmatic"},
                {"text": "Sensitive to pain, need reassurance", "temperament": "Melancholic"}
            ]},
            {"question_text": "What is your hair type?", "category": "Physical Traits", "display_order": 19, "options": [
                {"text": "Medium texture, healthy shine", "temperament": "Sanguinous"},
                {"text": "Dry or coarse hair", "temperament": "Bilious"},
                {"text": "Thick, lustrous hair", "temperament": "Phlegmatic"},
                {"text": "Fine or brittle hair", "temperament": "Melancholic"}
            ]},
            {"question_text": "How do you respond to criticism?", "category": "Social Response", "display_order": 20, "options": [
                {"text": "Take it lightly, move on", "temperament": "Sanguinous"},
                {"text": "Defend myself assertively", "temperament": "Bilious"},
                {"text": "Accept it calmly", "temperament": "Phlegmatic"},
                {"text": "Take it personally, reflect deeply", "temperament": "Melancholic"}
            ]},
            {"question_text": "How is your circulation and body temperature?", "category": "Circulation", "display_order": 21, "options": [
                {"text": "Warm hands and feet", "temperament": "Sanguinous"},
                {"text": "Warm body, tendency to overheat", "temperament": "Bilious"},
                {"text": "Cool hands and feet", "temperament": "Phlegmatic"},
                {"text": "Cold extremities", "temperament": "Melancholic"}
            ]},
            {"question_text": "What kind of environment helps you focus?", "category": "Work Style", "display_order": 22, "options": [
                {"text": "Social and interactive environment", "temperament": "Sanguinous"},
                {"text": "Structured and goal-oriented", "temperament": "Bilious"},
                {"text": "Peaceful and distraction-free", "temperament": "Phlegmatic"},
                {"text": "Quiet and organized space", "temperament": "Melancholic"}
            ]},
            {"question_text": "How would you describe your memory?", "category": "Cognitive Function", "display_order": 23, "options": [
                {"text": "Good memory for names and faces", "temperament": "Sanguinous"},
                {"text": "Good memory for facts and figures", "temperament": "Bilious"},
                {"text": "Good long-term memory", "temperament": "Phlegmatic"},
                {"text": "Excellent detail recall", "temperament": "Melancholic"}
            ]},
            {"question_text": "How do you react to change or new situations?", "category": "Adaptability", "display_order": 24, "options": [
                {"text": "Embrace change enthusiastically", "temperament": "Sanguinous"},
                {"text": "Take charge and adapt quickly", "temperament": "Bilious"},
                {"text": "Accept change gradually", "temperament": "Phlegmatic"},
                {"text": "Prefer routine, need time to adjust", "temperament": "Melancholic"}
            ]},
        ]
        for q in questions_data:
            db.add(QuizQuestion(**q))
        db.flush()
        logger.info(f"Seeded {len(questions_data)} quiz questions.")
        
        # Seed temperament combinations
        combinations_data = [
            {
                "name": "Sanguinous-Bilious",
                "description": "A dynamic and passionate constitution combining the warmth of Sanguinous with the intensity of Bilious. You are a natural leader with high energy and enthusiasm.",
                "foods_to_eat": ["Fresh fruits", "Vegetables", "Light proteins", "Cooling herbs like mint and coriander", "Whole grains"],
                "foods_to_avoid": ["Excessive spicy foods", "Fried foods", "Red meat in excess", "Alcohol", "Caffeine"],
                "disease_risks": ["Inflammatory conditions", "Skin rashes", "Acidity", "Liver heat", "Headaches"],
                "seasonal_tips": ["Spring: Focus on detox", "Summer: Stay cool and hydrated", "Autumn: Balance with routine", "Winter: Warm, nourishing foods"],
                "exercise_plan": {"frequency": "4-5 times per week", "type": "Moderate intensity mix", "activities": ["Swimming", "Cycling", "Team sports", "Yoga"], "duration": "30-45 minutes"},
                "sleep_plan": {"bedtime": "10:30 PM", "wake_time": "6:00 AM", "tips": ["Cool room temperature", "Avoid screens before bed", "Light reading before sleep"]},
                "emotional_guide": {"strengths": ["Leadership", "Enthusiasm", "Social energy"], "challenges": ["Impatience", "Overexertion"], "practices": ["Meditation", "Gratitude journaling"]}
            },
            {
                "name": "Sanguinous-Phlegmatic",
                "description": "A balanced and social constitution. Your Sanguinous warmth is tempered by Phlegmatic calm, making you approachable, patient, and well-liked.",
                "foods_to_eat": ["Light, balanced meals", "Seasonal vegetables", "Lean proteins", "Herbal teas", "Fresh fruits"],
                "foods_to_avoid": ["Heavy, oily foods", "Excessive sweets", "Processed foods", "Cold drinks with meals"],
                "disease_risks": ["Weight gain", "Slow metabolism", "Congestion", "Seasonal allergies", "Mild depression"],
                "seasonal_tips": ["Spring: Light detox", "Summer: Stay active outdoors", "Autumn: Warm, grounding foods", "Winter: Keep moving, avoid lethargy"],
                "exercise_plan": {"frequency": "3-4 times per week", "type": "Moderate, enjoyable", "activities": ["Walking", "Dancing", "Gentle yoga", "Social sports"], "duration": "30-40 minutes"},
                "sleep_plan": {"bedtime": "10:00 PM", "wake_time": "6:30 AM", "tips": ["Consistent schedule", "Warm bath before bed", "Herbal chamomile tea"]},
                "emotional_guide": {"strengths": ["Patience", "Social grace", "Flexibility"], "challenges": ["Procrastination", "Comfort zone"], "practices": ["Goal setting", "Morning routine"]}
            },
            {
                "name": "Sanguinous-Melancholic",
                "description": "A creative and thoughtful constitution. Your natural optimism is balanced with depth and introspection, making you both innovative and analytical.",
                "foods_to_eat": ["Warm, cooked meals", "Root vegetables", "Whole grains", "Nuts and seeds", "Warming spices"],
                "foods_to_avoid": ["Cold, raw foods", "Excessive sugar", "Processed foods", "Caffeine late in day"],
                "disease_risks": ["Anxiety", "Digestive sensitivity", "Sleep disorders", "Seasonal affective changes"],
                "seasonal_tips": ["Spring: Fresh beginnings", "Summer: Social activities", "Autumn: Creative projects", "Winter: Rest and reflection"],
                "exercise_plan": {"frequency": "3-4 times per week", "type": "Mind-body connection", "activities": ["Yoga", "Pilates", "Walking in nature", "Dance"], "duration": "30-45 minutes"},
                "sleep_plan": {"bedtime": "10:00 PM", "wake_time": "6:00 AM", "tips": ["Meditation before bed", "Journaling", "Dim lights 1 hour before"]},
                "emotional_guide": {"strengths": ["Creativity", "Depth", "Empathy"], "challenges": ["Overthinking", "Mood swings"], "practices": ["Creative expression", "Mindfulness"]}
            },
            {
                "name": "Bilious-Sanguinous",
                "description": "A dynamic and charismatic constitution. Your Bilious drive is enhanced by Sanguinous warmth, making you passionate, influential, and action-oriented.",
                "foods_to_eat": ["Cooling foods", "Fresh salads", "Sweet fruits", "Dairy in moderation", "Cucumber and melon"],
                "foods_to_avoid": ["Very spicy foods", "Fried foods", "Excessive red meat", "Alcohol", "Sour foods"],
                "disease_risks": ["Heartburn", "Skin inflammation", "High blood pressure", "Irritability", "Insomnia"],
                "seasonal_tips": ["Spring: Cooling practices", "Summer: Avoid heat", "Autumn: Moderate exercise", "Winter: Warm but light foods"],
                "exercise_plan": {"frequency": "4-5 times per week", "type": "Moderate, cooling", "activities": ["Swimming", "Walking", "Tai chi", "Moderate cycling"], "duration": "30-40 minutes"},
                "sleep_plan": {"bedtime": "10:00 PM", "wake_time": "5:30 AM", "tips": ["Cool room", "Essential oils (lavender)", "Avoid stimulating activities"]},
                "emotional_guide": {"strengths": ["Determination", "Charisma", "Drive"], "challenges": ["Anger", "Impatience"], "practices": ["Breathing exercises", "Cooling meditation"]}
            },
            {
                "name": "Bilious-Phlegmatic",
                "description": "A steady and determined constitution. Your Bilious drive is tempered by Phlegmatic calm, allowing you to pursue goals with both passion and patience.",
                "foods_to_eat": ["Balanced meals", "Steamed vegetables", "Lean proteins", "Warming but not spicy", "Herbal teas"],
                "foods_to_avoid": ["Extremes - very hot or very cold", "Greasy foods", "Processed foods", "Excessive salt"],
                "disease_risks": ["Digestive sluggishness", "Weight gain", "Joint stiffness", "Mood fluctuations"],
                "seasonal_tips": ["Spring: Gentle detox", "Summer: Stay active but cool", "Autumn: Build routine", "Winter: Maintain movement"],
                "exercise_plan": {"frequency": "3-4 times per week", "type": "Consistent, moderate", "activities": ["Brisk walking", "Strength training", "Hiking", "Swimming"], "duration": "35-45 minutes"},
                "sleep_plan": {"bedtime": "10:00 PM", "wake_time": "6:00 AM", "tips": ["Regular schedule", "Relaxation techniques", "Warm milk before bed"]},
                "emotional_guide": {"strengths": ["Persistence", "Balance", "Reliability"], "challenges": ["Stubbornness", "Resistance to change"], "practices": ["Flexibility exercises", "New experiences"]}
            },
            {
                "name": "Bilious-Melancholic",
                "description": "An intense and analytical constitution. Your Bilious passion combines with Melancholic depth, creating a powerful, focused, and determined personality.",
                "foods_to_eat": ["Warming, nourishing foods", "Cooked vegetables", "Whole grains", "Healthy oils", "Warming spices in moderation"],
                "foods_to_avoid": ["Extreme temperatures", "Dry, hard foods", "Excessive caffeine", "Processed foods", "Cold drinks"],
                "disease_risks": ["Joint inflammation", "Digestive issues", "Anxiety", "Tension headaches", "Sleep disturbance"],
                "seasonal_tips": ["Spring: Gentle movement", "Summer: Moderation", "Autumn: Grounding practices", "Winter: Nourish and rest"],
                "exercise_plan": {"frequency": "3-4 times per week", "type": "Structured, grounding", "activities": ["Yoga", "Strength training", "Walking", "Martial arts"], "duration": "30-45 minutes"},
                "sleep_plan": {"bedtime": "9:30 PM", "wake_time": "5:30 AM", "tips": ["Wind-down routine", "Warm bath", "Avoid mental stimulation"]},
                "emotional_guide": {"strengths": ["Focus", "Determination", "Depth"], "challenges": ["Perfectionism", "Tension"], "practices": ["Relaxation techniques", "Creative outlets"]}
            },
            {
                "name": "Phlegmatic-Bilious",
                "description": "A quietly determined constitution. Your natural Phlegmatic calm is energized by Bilious drive, making you steady yet capable of decisive action.",
                "foods_to_eat": ["Light, warming foods", "Steamed vegetables", "Lean proteins", "Ginger and warming spices", "Herbal teas"],
                "foods_to_avoid": ["Heavy, fatty foods", "Excessive dairy", "Cold foods and drinks", "Processed sugars"],
                "disease_risks": ["Weight gain", "Slow circulation", "Digestive sluggishness", "Low motivation", "Water retention"],
                "seasonal_tips": ["Spring: Increase activity", "Summer: Stay active outdoors", "Autumn: Warm, grounding foods", "Winter: Maintain routine"],
                "exercise_plan": {"frequency": "4-5 times per week", "type": "Energizing", "activities": ["Brisk walking", "Aerobic exercise", "Dancing", "Team sports"], "duration": "35-45 minutes"},
                "sleep_plan": {"bedtime": "10:00 PM", "wake_time": "6:00 AM", "tips": ["Consistent schedule", "Light stretching", "Avoid heavy meals late"]},
                "emotional_guide": {"strengths": ["Calm strength", "Reliability", "Patience"], "challenges": ["Low motivation", "Complacency"], "practices": ["Goal setting", "Morning motivation"]}
            },
            {
                "name": "Phlegmatic-Sanguinous",
                "description": "A warm and easygoing constitution. Your Phlegmatic calm combined with Sanguinous warmth makes you approachable, kind, and a natural peacemaker.",
                "foods_to_eat": ["Light, fresh foods", "Seasonal fruits", "Vegetables", "Light proteins", "Herbal infusions"],
                "foods_to_avoid": ["Heavy, oily foods", "Excessive sweets", "Very cold foods", "Processed foods"],
                "disease_risks": ["Weight gain", "Slow metabolism", "Respiratory congestion", "Lethargy", "Mild depression"],
                "seasonal_tips": ["Spring: Energize routine", "Summer: Social activities", "Autumn: Gradual transition", "Winter: Stay active indoors"],
                "exercise_plan": {"frequency": "3-4 times per week", "type": "Social, enjoyable", "activities": ["Group walks", "Dance", "Swimming", "Gentle aerobics"], "duration": "30-40 minutes"},
                "sleep_plan": {"bedtime": "10:00 PM", "wake_time": "6:30 AM", "tips": ["Avoid oversleeping", "Morning light exposure", "Gentle stretching"]},
                "emotional_guide": {"strengths": ["Kindness", "Adaptability", "Peacemaking"], "challenges": ["Avoidance of conflict", "Low drive"], "practices": ["Assertiveness practice", "Goal setting"]}
            },
            {
                "name": "Melancholic-Sanguinous",
                "description": "A creative and expressive constitution. Your natural depth and thoughtfulness are balanced with warmth and sociability, making you both insightful and engaging.",
                "foods_to_eat": ["Warm, grounding foods", "Cooked grains", "Root vegetables", "Healthy proteins", "Nuts and seeds"],
                "foods_to_avoid": ["Extreme temperatures", "Very dry foods", "Excessive caffeine", "Sugary snacks", "Processed foods"],
                "disease_risks": ["Anxiety", "Digestive sensitivity", "Sleep issues", "Seasonal mood changes", "Low energy"],
                "seasonal_tips": ["Spring: New beginnings", "Summer: Social connection", "Autumn: Creative focus", "Winter: Rest and rejuvenation"],
                "exercise_plan": {"frequency": "3-4 times per week", "type": "Creative, varied", "activities": ["Yoga", "Nature walks", "Dance", "Pilates"], "duration": "30-45 minutes"},
                "sleep_plan": {"bedtime": "10:00 PM", "wake_time": "6:00 AM", "tips": ["Calming routine", "Journaling", "Herbal tea before bed"]},
                "emotional_guide": {"strengths": ["Creativity", "Empathy", "Insight"], "challenges": ["Moodiness", "Overthinking"], "practices": ["Creative expression", "Gratitude practice"]}
            },
            {
                "name": "Melancholic-Phlegmatic",
                "description": "A thoughtful and calm constitution. Your deep analytical nature is balanced with Phlegmatic serenity, making you wise, patient, and introspective.",
                "foods_to_eat": ["Warm, cooked meals", "Whole grains", "Cooked vegetables", "Warming spices", "Herbal teas"],
                "foods_to_avoid": ["Cold, raw foods", "Dry snacks", "Excessive sweets", "Caffeine", "Processed foods"],
                "disease_risks": ["Low metabolism", "Digestive issues", "Joint stiffness", "Seasonal depression", "Lethargy"],
                "seasonal_tips": ["Spring: Gentle movement", "Summer: Outdoor activities", "Autumn: Structure routine", "Winter: Warm, nourishing foods"],
                "exercise_plan": {"frequency": "3-4 times per week", "type": "Gentle, consistent", "activities": ["Walking", "Tai chi", "Gentle yoga", "Stretching"], "duration": "30-40 minutes"},
                "sleep_plan": {"bedtime": "9:30 PM", "wake_time": "6:30 AM", "tips": ["Relaxation exercises", "Avoid overstimulation", "Warm bath"]},
                "emotional_guide": {"strengths": ["Wisdom", "Patience", "Depth"], "challenges": ["Isolation tendency", "Low energy"], "practices": ["Social connection", "Physical activity"]}
            },
        ]
        for c in combinations_data:
            db.add(TemperamentCombination(**c))
        db.flush()
        logger.info(f"Seeded {len(combinations_data)} temperament combinations.")
        
        # Seed admin user
        admin = AdminUser(
            username="admin",
            password_hash=pwd_context.hash("3d5d511bd347b00e97ef851e"),
            is_admin=True
        )
        db.add(admin)
        db.commit()
        logger.info("Admin user created.")
        logger.info("Database seeded successfully!")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return JSONResponse(
        status_code=200,
        content={
            "name": "TibbWell API",
            "version": "1.0.0",
            "status": "running",
            "docs": "/api/docs"
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "tibbwell-backend"
        }
    )


@app.get("/api/health")
async def api_health_check():
    """
    API health check with external service status
    
    Reports the health status of:
    - Local API service
    - PayFast payment service (if configured)
    """
    health_status = {
        "status": "healthy",
        "service": "tibbwell-backend",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "external_services": {}
    }
    
    # Check PayFast health
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("https://api.payfast.co.za/health")
            if response.status_code == 200:
                health_status["external_services"]["payfast"] = {
                    "status": "healthy",
                    "latency_ms": round(response.elapsed.total_seconds() * 1000, 2)
                }
            else:
                health_status["external_services"]["payfast"] = {
                    "status": "degraded",
                    "status_code": response.status_code
                }
    except httpx.TimeoutException:
        health_status["external_services"]["payfast"] = {
            "status": "timeout",
            "error": "Connection timeout"
        }
        health_status["status"] = "degraded"
    except httpx.ConnectError:
        health_status["external_services"]["payfast"] = {
            "status": "unavailable",
            "error": "Connection failed"
        }
        health_status["status"] = "degraded"
    except Exception as e:
        health_status["external_services"]["payfast"] = {
            "status": "unknown",
            "error": str(e)
        }
    
    # Check database connectivity (basic query)
    try:
        from api.database import SessionLocal, User
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        health_status["database"] = {"status": "healthy"}
    except Exception as e:
        health_status["database"] = {"status": "error", "error": str(e)}
        health_status["status"] = "degraded"
    
    return JSONResponse(
        status_code=200 if health_status["status"] == "healthy" else 503,
        content=health_status
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )