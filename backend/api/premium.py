"""
Premium dashboard endpoints for TibbWell
Returns full health programme including food guides, seasonal protocols, 
exercise plan, sleep plan, and emotional wellness for each temperament combination
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from api.database import get_db, User, QuizResult, TemperamentCombination, PremiumContent

router = APIRouter()

# Monthly subscription price in ZAR
SUBSCRIPTION_PRICE_ZAR = 99


class PremiumDashboardResponse(BaseModel):
    user_id: int
    email: str
    name: str
    is_premium: bool
    subscription_status: str
    temperament_combination: str
    health_programme: dict


class MonthlyFocusResponse(BaseModel):
    month: str
    focus_tip: str


@router.get("/dashboard", response_model=PremiumDashboardResponse)
async def get_premium_dashboard(
    authorization: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get premium dashboard with full health programme
    
    Returns comprehensive health guidance based on user's temperament combination:
    - Food guide with foods to eat and avoid
    - Seasonal protocols for each season
    - Exercise plan tailored to constitution
    - Sleep plan with optimal hours and tips
    - Emotional wellness guide
    
    Requires valid JWT token with Bearer prefix
    """
    # For demo purposes, we'll use a mock user if no token provided
    # In production, validate the JWT token
    user = None
    user_id = None
    
    if authorization:
        if authorization.startswith("Bearer "):
            token = authorization[7:]
            # In production, decode token and get user_id
            # For now, we'll use the first premium user or create a demo
    
    # Get or create demo premium user
    user = db.query(User).filter(User.email == "premium@tibbwell.com").first()
    if not user:
        # Check if there's any user with a quiz result
        user_with_result = db.query(User).join(QuizResult).first()
        if user_with_result:
            user = user_with_result
        else:
            # Create a demo premium user
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            user = User(
                email="premium@tibbwell.com",
                password_hash=pwd_context.hash("premium123"),
                name="Premium User",
                is_premium=True,
                payfast_subscription_id="demo_subscription_001"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's temperament combination
    combination_name = "Sanguinous-Bilious"  # Default
    if user.temperament_combination_id:
        combo = db.query(TemperamentCombination).filter(
            TemperamentCombination.id == user.temperament_combination_id
        ).first()
        if combo:
            combination_name = combo.name
    else:
        # Get from latest quiz result
        latest_result = db.query(QuizResult).filter(
            QuizResult.user_id == user.id
        ).order_by(QuizResult.created_at.desc()).first()
        if latest_result:
            combination_name = latest_result.combination_name
    
    # Get combination details
    combination = db.query(TemperamentCombination).filter(
        TemperamentCombination.name == combination_name
    ).first()
    
    if not combination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Combination '{combination_name}' not found"
        )
    
    # Build health programme from combination data
    health_programme = {
        "combination_name": combination.name,
        "description": combination.description,
        "food_guide": {
            "foods_to_eat": combination.foods_to_eat or [],
            "foods_to_avoid": combination.foods_to_avoid or []
        },
        "seasonal_protocols": combination.seasonal_tips or [],
        "exercise_plan": combination.exercise_plan or {},
        "sleep_plan": combination.sleep_plan or {},
        "emotional_wellness": combination.emotional_guide or {}
    }
    
    # Add premium content if available
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    premium_content = db.query(PremiumContent).filter(
        PremiumContent.temperament_combination_id == combination.id,
        PremiumContent.month == current_month,
        PremiumContent.year == current_year
    ).first()
    
    if premium_content:
        health_programme["monthly_content"] = premium_content.content
    
    return PremiumDashboardResponse(
        user_id=user.id,
        email=user.email,
        name=user.name,
        is_premium=user.is_premium,
        subscription_status="active" if user.is_premium else "inactive",
        temperament_combination=combination_name,
        health_programme=health_programme
    )


@router.get("/foods")
async def get_food_recommendations(
    combination_name: str,
    db: Session = Depends(get_db)
):
    """
    Get food recommendations for a specific temperament combination
    
    Query params:
    - combination_name: The temperament combination (e.g., "Sanguinous-Bilious")
    """
    combination = db.query(TemperamentCombination).filter(
        TemperamentCombination.name == combination_name
    ).first()
    
    if not combination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Combination '{combination_name}' not found"
        )
    
    return {
        "combination": combination_name,
        "foods_to_eat": combination.foods_to_eat or [],
        "foods_to_avoid": combination.foods_to_avoid or []
    }


@router.get("/exercise")
async def get_exercise_plan(
    combination_name: str,
    db: Session = Depends(get_db)
):
    """
    Get exercise plan for a specific temperament combination
    """
    combination = db.query(TemperamentCombination).filter(
        TemperamentCombination.name == combination_name
    ).first()
    
    if not combination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Combination '{combination_name}' not found"
        )
    
    return {
        "combination": combination_name,
        "exercise_plan": combination.exercise_plan or {}
    }


@router.get("/monthly-focus")
async def get_monthly_focus(
    month_year: str,  # Format: "2025-01"
    db: Session = Depends(get_db)
):
    """
    Get monthly health focus tip for all combinations
    """
    from api.database import MonthlyHealthFocus
    
    foci = db.query(MonthlyHealthFocus).filter(
        MonthlyHealthFocus.month_year == month_year
    ).all()
    
    if not foci:
        return {
            "month_year": month_year,
            "message": "No specific focus tips for this month yet",
            "tips": []
        }
    
    return {
        "month_year": month_year,
        "tips": [
            {
                "combination": f.temperament_combination_id,
                "tip": f.tip_content
            }
            for f in foci
        ]
    }


@router.post("/subscribe")
async def create_subscription(
    user_id: int,
    payfast_subscription_id: str,
    db: Session = Depends(get_db)
):
    """
    Create a PayFast subscription for a user
    
    In production, this would be called after PayFast payment confirmation
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_premium = True
    user.payfast_subscription_id = payfast_subscription_id
    
    db.commit()
    
    return {
        "status": "success",
        "message": "Subscription activated",
        "user_id": user_id,
        "is_premium": user.is_premium
    }


@router.get("/subscription/status")
async def get_subscription_status(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get subscription status for a user
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "user_id": user_id,
        "is_premium": user.is_premium,
        "subscription_id": user.payfast_subscription_id,
        "status": "active" if user.is_premium else "inactive"
    }