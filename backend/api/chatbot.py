"""
Chatbot endpoint for TibbWell
Answers health questions based on temperament data using AI-like responses
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from datetime import datetime

from api.database import get_db, User, QuizResult, TemperamentCombination

router = APIRouter()

# Mock responses for common health questions
HEALTH_KNOWLEDGE_BASE = {
    "general": {
        "question": "What is TibbWell?",
        "answer": "TibbWell is a traditional Unani medicine health platform that helps you understand your mizaaj (temperament) constitution. Based on your unique temperament combination, we provide personalized health guidance including diet recommendations, exercise plans, sleep tips, and emotional wellness strategies."
    },
    "diet": {
        "question": "What should I eat for my temperament?",
        "answer_template": "Based on your {combination} constitution, you should focus on {foods}. Avoid {avoid_foods}. Remember to eat according to seasonal changes and listen to your body's signals."
    },
    "exercise": {
        "question": "What exercise is best for me?",
        "answer_template": "For your {combination} constitution, we recommend {exercise_type} exercise for {duration} minutes, {frequency}. {avoid_exercise} Keep your exercise routine consistent and adjust based on seasonal changes."
    },
    "sleep": {
        "question": "How can I improve my sleep?",
        "answer_template": "For your {combination} type, aim for {hours} hours of sleep per night. {tips}"
    },
    "stress": {
        "question": "How do I manage stress?",
        "answer_template": "Your {combination} constitution responds well to {stress_tips}. {additional_advice}"
    },
    "seasonal": {
        "question": "How should I adjust my routine seasonally?",
        "answer_template": "For {combination}: {seasonal_tips}"
    }
}


class ChatMessage(BaseModel):
    message: str
    user_id: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    temperament: Optional[str] = None
    combination: Optional[str] = None
    timestamp: str


def get_user_temperament_info(user_id: int, db: Session) -> tuple:
    """Get user's temperament combination from their quiz results"""
    # Get the most recent quiz result for this user
    quiz_result = db.query(QuizResult).filter(
        QuizResult.user_id == user_id
    ).order_by(QuizResult.created_at.desc()).first()
    
    if not quiz_result:
        return None, None
    
    combination = db.query(TemperamentCombination).filter(
        TemperamentCombination.name == quiz_result.combination_name
    ).first()
    
    if not combination:
        return quiz_result.dominant_temperament, quiz_result.combination_name
    
    return quiz_result.dominant_temperament, combination


def generate_response(user_message: str, combination_name: str, combination_data) -> str:
    """Generate a response based on user's temperament combination"""
    message_lower = user_message.lower()
    
    # Diet-related questions
    if any(word in message_lower for word in ["eat", "food", "diet", "meal", "hunger", "appetite"]):
        foods = ", ".join(combination_data.foods_to_eat[:5]) if combination_data.foods_to_eat else "a balanced diet"
        avoid = ", ".join(combination_data.foods_to_avoid[:5]) if combination_data.foods_to_avoid else "processed foods"
        return f"For your {combination_name} constitution, focus on {foods}. Avoid {avoid}. Eat at regular intervals and avoid eating when emotionally upset."
    
    # Exercise-related questions
    if any(word in message_lower for word in ["exercise", "workout", "fitness", "activity", "gym", "sport"]):
        exercise_plan = combination_data.exercise_plan or {}
        exercise_type = exercise_plan.get("type", "moderate")
        duration = exercise_plan.get("duration", "30-45 minutes")
        frequency = exercise_plan.get("frequency", "4-5x/week")
        activities = ", ".join(exercise_plan.get("activities", ["walking", "yoga"])) if exercise_plan.get("activities") else "walking and yoga"
        avoid = exercise_plan.get("avoid", "intense competitive sports")
        return f"For your {combination_name} type, engage in {exercise_type} exercise for {duration} {frequency}. Great activities include: {activities}. Avoid: {avoid}."
    
    # Sleep-related questions
    if any(word in message_lower for word in ["sleep", "rest", "tired", "insomnia", "night"]):
        sleep_plan = combination_data.sleep_plan or {}
        hours = sleep_plan.get("hours", 7)
        tips = ", ".join(sleep_plan.get("tips", ["maintain consistent schedule"])) if sleep_plan.get("tips") else "maintain consistent schedule"
        return f"Your {combination_name} constitution benefits from {hours} hours of sleep per night. {tips}. Avoid screens before bed and keep your bedroom cool."
    
    # Stress-related questions
    if any(word in message_lower for word in ["stress", "anxiety", "worried", "nervous", "calm"]):
        emotional_guide = combination_data.emotional_guide or {}
        practices = ", ".join(emotional_guide.get("practices", ["meditation", "deep breathing"])) if emotional_guide.get("practices") else "meditation and deep breathing"
        avoid = ", ".join(emotional_guide.get("avoid", ["overwork"])) if emotional_guide.get("avoid") else "overwork"
        return f"For stress management with your {combination_name} type, practice {practices}. Avoid {avoid}. Regular breaks and setting boundaries are essential."
    
    # Seasonal questions
    if any(word in message_lower for word in ["season", "summer", "winter", "autumn", "spring", "weather", "climate"]):
        seasonal = combination_data.seasonal_tips or []
        if seasonal:
            return f"For your {combination_name} constitution: {' '.join(seasonal[:3])}"
        return f"For your {combination_name} constitution, adjust your routine according to seasonal changes. In summer, stay cool and hydrated. In winter, maintain warmth and nourishment."
    
    # Disease/risk questions
    if any(word in message_lower for word in ["risk", "disease", "health problem", "symptom", "condition"]):
        risks = combination_data.disease_risks or []
        if risks:
            return f"Your {combination_name} constitution may be predisposed to: {', '.join(risks[:4])}. Prevention focus: maintain balanced diet, regular exercise, and stress management."
        return f"Maintain your {combination_name} constitution with balanced lifestyle practices. Focus on prevention through diet, exercise, and emotional balance."
    
    # General wellness
    if any(word in message_lower for word in ["health", "wellness", "balance", "wellbeing"]):
        return f"Optimal health for your {combination_name} constitution comes from balancing your Hot/Cold and Moist/Dry qualities through appropriate diet, exercise, sleep, and emotional practices."
    
    # Default response
    return f"For your {combination_name} constitution, I recommend maintaining a balanced lifestyle with attention to your unique temperament needs. Would you like specific guidance on diet, exercise, sleep, or stress management?"


@router.post("/ask", response_model=ChatResponse)
async def ask_chatbot(
    chat_message: ChatMessage,
    db: Session = Depends(get_db)
):
    """
    Ask the TibbWell chatbot a health question
    
    The chatbot provides personalized responses based on the user's
    temperament combination. For premium users, responses are more detailed.
    
    For non-premium users or anonymous users without quiz results,
    provides general wellness guidance.
    """
    user_message = chat_message.message
    user_id = chat_message.user_id
    
    # Get user's temperament info
    temperament, combination_name = None, None
    combination_data = None
    
    if user_id:
        temperament, combination_name = get_user_temperament_info(user_id, db)
        
        if combination_name:
            combination_data = db.query(TemperamentCombination).filter(
                TemperamentCombination.name == combination_name
            ).first()
    
    # Generate response
    if combination_data:
        response = generate_response(user_message, combination_name, combination_data)
    else:
        # Default response for users without temperament data
        response = "To provide personalized health guidance, please complete the TibbWell quiz first. Your mizaaj (temperament) assessment helps me give you tailored advice based on your unique constitution. Take the quiz at /quiz to discover your temperament combination."
    
    return ChatResponse(
        response=response,
        temperament=temperament,
        combination=combination_name,
        timestamp=datetime.now().isoformat()
    )


@router.get("/capabilities")
async def get_chatbot_capabilities():
    """
    Get information about what the chatbot can help with
    """
    return {
        "name": "TibbWell AI Assistant",
        "description": "Your personal Unani medicine health advisor based on your mizaaj (temperament) constitution",
        "capabilities": [
            {
                "category": "Diet & Nutrition",
                "examples": [
                    "What should I eat for my temperament?",
                    "Give me food recommendations",
                    "What foods should I avoid?"
                ]
            },
            {
                "category": "Exercise & Fitness",
                "examples": [
                    "What exercise is best for me?",
                    "Create a workout plan",
                    "How often should I exercise?"
                ]
            },
            {
                "category": "Sleep & Rest",
                "examples": [
                    "How can I improve my sleep?",
                    "How many hours should I sleep?",
                    "Tips for better rest"
                ]
            },
            {
                "category": "Stress Management",
                "examples": [
                    "How do I manage stress?",
                    "Help with anxiety",
                    "Emotional wellness tips"
                ]
            },
            {
                "category": "Seasonal Guidance",
                "examples": [
                    "How should I adjust seasonally?",
                    "Summer wellness tips",
                    "Winter health advice"
                ]
            }
        ],
        "premium_feature": "Premium subscribers get more detailed and personalized guidance based on their full health programme"
    }


@router.get("/health-tips/{category}")
async def get_health_tips(
    category: str,
    combination_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get specific health tips by category
    
    Categories: diet, exercise, sleep, stress, seasonal, general
    """
    tips = {
        "diet": {
            "title": "Diet Tips by Temperament",
            "content": {
                "Sanguinous": "Focus on cooling foods like cucumbers, melons, and leafy greens. Avoid spicy foods and excess red meat.",
                "Bilious": "Prefer moistening foods like avocados, pears, and zucchini. Avoid hot, spicy, and dry foods.",
                "Phlegmatic": "Eat warming foods like ginger, cinnamon, and cooked vegetables. Avoid cold, heavy, and dairy-rich foods.",
                "Melancholic": "Consume nourishing, slightly oily foods. Avoid dry, cold, and very light foods."
            }
        },
        "exercise": {
            "title": "Exercise Tips by Temperament",
            "content": {
                "Sanguinous": "Moderate cardio 4-5x/week for 30-45 minutes. Swimming and walking are ideal.",
                "Bilious": "Mindful exercise 3-4x/week for 30-40 minutes. Yoga and meditative walking suit you.",
                "Phlegmatic": "Active lifestyle 5-6x/week for 40-60 minutes. Combat sluggishness with brisk walking and dancing.",
                "Melancholic": "Gentle activation 4-5x/week for 25-35 minutes. Short walks and stretching build momentum."
            }
        },
        "sleep": {
            "title": "Sleep Tips by Temperament",
            "content": {
                "Sanguinous": "7 hours, maintain consistent schedule, cool room, light blanket only.",
                "Bilious": "8.5 hours, prioritize sleep, early bedtime, wind-down ritual essential.",
                "Phlegmatic": "8 hours, quality sleep priority, establish bedtime routine, avoid late meals.",
                "Melancholic": "9 hours, extra sleep often needed, morning sunlight exposure, gradual wake routine."
            }
        },
        "stress": {
            "title": "Stress Management by Temperament",
            "content": {
                "Sanguinous": "Channel energy constructively, set realistic goals, practice patience, take breaks.",
                "Bilious": "Regular breaks, set boundaries, practice self-compassion, seek support, laugh daily.",
                "Phlegmatic": "Set boundaries, practice saying no, schedule rest, cultivate inner peace.",
                "Melancholic": "Journaling, mindfulness meditation, creative expression, emotional awareness."
            }
        },
        "seasonal": {
            "title": "Seasonal Tips by Temperament",
            "content": {
                "Sanguinous": "Summer: Stay cool with melon. Winter: Balance with warm soups. Spring: Gentle detox.",
                "Bilious": "Summer: Cooling diet critical. Winter: Extra rest. Spring: Gradual activity increase.",
                "Phlegmatic": "Winter: Active exercise. Summer: Light activities. Spring: Natural detox with bitter foods.",
                "Melancholic": "Winter: Maintain warmth. Summer: Slight activity increase. Spring: Perfect for renewal."
            }
        },
        "general": {
            "title": "General Wellness Tips",
            "content": {
                "Sanguinous": "Balance your social energy with alone time. Don't overcommit.",
                "Bilious": "Prevent burnout by setting boundaries. Celebrate achievements.",
                "Phlegmatic": "Counter isolation with gentle connection. Small social gatherings help.",
                "Melancholic": "Counter rumination with creative pursuits. Nature exposure is healing."
            }
        }
    }
    
    if category not in tips:
        return {
            "error": f"Category '{category}' not found",
            "valid_categories": list(tips.keys())
        }
    
    return tips[category]