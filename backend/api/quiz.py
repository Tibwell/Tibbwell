"""
Quiz endpoints for TibbWell
Handles quiz questions and quiz submission/scoring
Uses SQLite database for storage
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
import uuid

from api.database import get_db, QuizQuestion, QuizResult, Temperament, TemperamentCombination

router = APIRouter()

# Temperament types
TEMPERAMENTS = ["Sanguinous", "Bilious", "Phlegmatic", "Melancholic"]

# Temperament qualities for response
TEMPERAMENT_INFO = {
    "Sanguinous": {
        "name": "Sanguinous",
        "quality": "Hot & Moist",
        "element": "Air",
        "description": "The Sanguinous temperament is characterized by warmth and moisture. People with this constitution tend to be social, enthusiastic, creative, and optimistic."
    },
    "Bilious": {
        "name": "Bilious",
        "quality": "Hot & Dry",
        "element": "Fire",
        "description": "The Bilious temperament is characterized by heat and dryness. People with this constitution tend to be ambitious, determined, decisive, and passionate."
    },
    "Phlegmatic": {
        "name": "Phlegmatic",
        "quality": "Cold & Moist",
        "element": "Water",
        "description": "The Phlegmatic temperament is characterized by coldness and moisture. People with this constitution tend to be calm, thoughtful, diplomatic, and patient."
    },
    "Melancholic": {
        "name": "Melancholic",
        "quality": "Cold & Dry",
        "element": "Earth",
        "description": "The Melancholic temperament is characterized by coldness and dryness. People with this constitution tend to be analytical, detail-oriented, perfectionist, and creative."
    }
}

# Combination name mapping based on dominant and sub-dominant temperament
COMBINATION_NAMES = {
    ("Sanguinous", "Bilious"): "Sanguinous-Bilious",
    ("Sanguinous", "Phlegmatic"): "Sanguinous-Phlegmatic",
    ("Sanguinous", "Melancholic"): "Sanguinous-Melancholic",
    ("Bilious", "Sanguinous"): "Sanguinous-Bilious",
    ("Bilious", "Phlegmatic"): "Bilious-Phlegmatic",
    ("Bilious", "Melancholic"): "Bilious-Melancholic",
    ("Phlegmatic", "Sanguinous"): "Sanguinous-Phlegmatic",
    ("Phlegmatic", "Bilious"): "Bilious-Phlegmatic",
    ("Phlegmatic", "Melancholic"): "Phlegmatic-Melancholic",
    ("Melancholic", "Sanguinous"): "Sanguinous-Melancholic",
    ("Melancholic", "Bilious"): "Bilious-Melancholic",
    ("Melancholic", "Phlegmatic"): "Phlegmatic-Melancholic",
}


# Quiz Question Model
class QuizOption(BaseModel):
    text: str
    temperament: str


class QuizQuestionResponse(BaseModel):
    id: int
    question_text: str
    category: str
    options: List[QuizOption]


# Quiz Submission Model
class QuizAnswer(BaseModel):
    question_id: int
    selected_temperament: str


class QuizSubmission(BaseModel):
    answers: List[QuizAnswer]
    session_id: Optional[str] = None
    user_id: Optional[int] = None


# Quiz Response Model
class QuizScore(BaseModel):
    Sanguinous: int
    Bilious: int
    Phlegmatic: int
    Melancholic: int


class QuizResultResponse(BaseModel):
    session_id: str
    scores: QuizScore
    dominant_temperament: str
    sub_dominant_temperament: str
    combination_name: str
    result_description: str


def calculate_temperament_scores(answers: List[QuizAnswer]) -> dict:
    """Calculate temperament scores from quiz answers"""
    scores = {"Sanguinous": 0, "Bilious": 0, "Phlegmatic": 0, "Melancholic": 0}
    
    for answer in answers:
        if answer.selected_temperament in scores:
            scores[answer.selected_temperament] += 1
    
    return scores


def determine_dominant_temperaments(scores: dict) -> tuple:
    """Determine dominant and sub-dominant temperaments from scores"""
    sorted_temperaments = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    dominant = sorted_temperaments[0][0]
    sub_dominant = sorted_temperaments[1][0]
    
    # Handle ties - if scores are equal, use the order that makes sense
    if len(sorted_temperaments) >= 2:
        if sorted_temperaments[0][1] == sorted_temperaments[1][1]:
            # Tie breaker - prefer the one that makes a valid combination
            dominant = sorted_temperaments[0][0]
            sub_dominant = sorted_temperaments[1][0]
    
    return dominant, sub_dominant


def get_combination_name(dominant: str, sub_dominant: str) -> str:
    """Get the combination name for dominant and sub-dominant temperaments"""
    combination_key = (dominant, sub_dominant)
    return COMBINATION_NAMES.get(
        combination_key,
        f"{dominant}-{sub_dominant}"
    )


@router.get("/questions", response_model=List[QuizQuestionResponse])
async def get_questions(db: Session = Depends(get_db)):
    """
    Get all quiz questions for temperament assessment
    
    Returns 25 questions covering body frame, skin texture, complexion,
    climatic preferences, food cravings, recurring health problems,
    sleep patterns, speech style, personality traits, and emotional tendencies.
    """
    questions = db.query(QuizQuestion).order_by(QuizQuestion.display_order).all()
    
    result = []
    for q in questions:
        options = []
        for opt in q.options:
            if isinstance(opt, dict):
                options.append(QuizOption(
                    text=opt.get("text", ""),
                    temperament=opt.get("temperament", "")
                ))
        result.append(QuizQuestionResponse(
            id=q.id,
            question_text=q.question_text,
            category=q.category or "",
            options=options
        ))
    
    return result


@router.post("/submit", response_model=QuizResultResponse)
async def submit_quiz(submission: QuizSubmission, db: Session = Depends(get_db)):
    """
    Submit quiz answers and receive temperament analysis
    
    Calculates scores for each temperament type, determines dominant
    and sub-dominant temperaments, and returns combination name with
    description.
    """
    # Validate that all answers are for valid questions
    question_ids = {q.id for q in db.query(QuizQuestion.id).all()}
    for answer in submission.answers:
        if answer.question_id not in question_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid question_id: {answer.question_id}"
            )
    
    # Calculate scores
    scores = calculate_temperament_scores(submission.answers)
    
    # Find dominant and sub-dominant temperaments
    dominant, sub_dominant = determine_dominant_temperaments(scores)
    
    # Get combination name
    combination_name = get_combination_name(dominant, sub_dominant)
    
    # Generate result description
    result_description = (
        f"Your dominant temperament is {dominant} ({TEMPERAMENT_INFO[dominant]['quality']}), "
        f"with {sub_dominant} as your secondary temperament. "
        f"This combination is known as {combination_name}. "
        f"{TEMPERAMENT_INFO[dominant]['description']}"
    )
    
    # Generate session ID if not provided
    session_id = submission.session_id or str(uuid.uuid4())
    
    # Prepare answers for storage
    answers_data = [
        {"question_id": a.question_id, "selected_temperament": a.selected_temperament}
        for a in submission.answers
    ]
    
    # Store result in database
    quiz_result = QuizResult(
        session_id=session_id,
        user_id=submission.user_id,
        answers=answers_data,
        scores=scores,
        dominant_temperament=dominant,
        sub_dominant_temperament=sub_dominant,
        combination_name=combination_name
    )
    
    db.add(quiz_result)
    db.commit()
    db.refresh(quiz_result)
    
    return QuizResultResponse(
        session_id=session_id,
        scores=QuizScore(**scores),
        dominant_temperament=dominant,
        sub_dominant_temperament=sub_dominant,
        combination_name=combination_name,
        result_description=result_description
    )


@router.get("/result/{session_id}")
async def get_result(session_id: str, db: Session = Depends(get_db)):
    """
    Get a previously submitted quiz result by session ID
    """
    result = db.query(QuizResult).filter(QuizResult.session_id == session_id).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz result not found"
        )
    
    return {
        "session_id": result.session_id,
        "scores": result.scores,
        "dominant_temperament": result.dominant_temperament,
        "sub_dominant_temperament": result.sub_dominant_temperament,
        "combination_name": result.combination_name
    }


@router.get("/temperaments")
async def get_temperaments(db: Session = Depends(get_db)):
    """
    Get information about all four temperament types
    """
    temperaments = db.query(Temperament).all()
    
    result = {}
    for t in temperaments:
        result[t.name] = {
            "name": t.name,
            "quality": t.quality,
            "element": t.element,
            "description": t.description
        }
    
    # If no temperaments in DB, return static info
    if not result:
        result = TEMPERAMENT_INFO
    
    return result


@router.get("/combinations")
async def get_combinations(db: Session = Depends(get_db)):
    """
    Get all temperament combinations with detailed health guidance
    """
    combinations = db.query(TemperamentCombination).all()
    
    result = []
    for c in combinations:
        result.append({
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "foods_to_eat": c.foods_to_eat or [],
            "foods_to_avoid": c.foods_to_avoid or [],
            "disease_risks": c.disease_risks or [],
            "seasonal_tips": c.seasonal_tips or [],
            "exercise_plan": c.exercise_plan or {},
            "sleep_plan": c.sleep_plan or {},
            "emotional_guide": c.emotional_guide or {}
        })
    
    return result


@router.get("/combination/{name}")
async def get_combination(name: str, db: Session = Depends(get_db)):
    """
    Get a specific temperament combination by name
    """
    combination = db.query(TemperamentCombination).filter(
        TemperamentCombination.name == name
    ).first()
    
    if not combination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Combination '{name}' not found"
        )
    
    return {
        "id": combination.id,
        "name": combination.name,
        "description": combination.description,
        "foods_to_eat": combination.foods_to_eat or [],
        "foods_to_avoid": combination.foods_to_avoid or [],
        "disease_risks": combination.disease_risks or [],
        "seasonal_tips": combination.seasonal_tips or [],
        "exercise_plan": combination.exercise_plan or {},
        "sleep_plan": combination.sleep_plan or {},
        "emotional_guide": combination.emotional_guide or {}
    }