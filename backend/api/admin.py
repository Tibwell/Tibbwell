"""
Admin dashboard endpoints for TibbWell
Provides statistics and management for administrators
"""
from fastapi import APIRouter, HTTPException, status, Depends, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from jose import JWTError, jwt

from api.database import get_db, User, QuizResult, TemperamentCombination, AdminUser
from api.auth import pwd_context

router = APIRouter()

# JWT settings (same as auth.py - should be in config in production)
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"

# Subscription price in ZAR
SUBSCRIPTION_PRICE_ZAR = 99


# ================ Admin Authentication ================

class AdminLoginRequest(BaseModel):
    """Admin login request"""
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=128)


class AdminLoginResponse(BaseModel):
    """Admin login response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    admin: dict


class AdminStatsResponse(BaseModel):
    total_users: int
    active_subscribers: int
    monthly_revenue: int
    quiz_completion_rate: float
    most_common_temperament: str
    temperament_distribution: Dict[str, int]
    recent_registrations: List[dict]
    registration_growth_percent: float


class TemperamentCount(BaseModel):
    temperament: str
    count: int
    percentage: float


async def get_current_admin_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> AdminUser:
    """
    Dependency to verify admin authentication
    
    Extracts and validates the JWT token from Authorization header,
    then verifies the user exists in the admin_users table.
    
    Raises HTTPException 401 if not authenticated
    Raises HTTPException 403 if not an admin
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Remove 'Bearer ' prefix if present
    if authorization.startswith("Bearer "):
        token = authorization[7:]
    else:
        token = authorization
    
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        
        # Check if user is an admin
        admin_user = db.query(AdminUser).filter(AdminUser.id == user_id).first()
        
        if not admin_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        return admin_user
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )


# ================ Admin Routes ================

@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(
    credentials: AdminLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Admin login endpoint
    
    Authenticates admin users and returns a JWT token.
    Admins have a separate token from regular users.
    """
    from jose import jwt
    from datetime import timedelta
    
    ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Admin tokens last 1 hour
    
    # Find admin user
    admin = db.query(AdminUser).filter(
        AdminUser.username == credentials.username
    ).first()
    
    if not admin or not pwd_context.verify(credentials.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials"
        )
    
    # Create admin token
    access_token = jwt.encode(
        {
            "sub": str(admin.id),
            "username": admin.username,
            "type": "admin",
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    return AdminLoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        admin={
            "id": admin.id,
            "username": admin.username
        }
    )


@router.get("/stats", response_model=AdminStatsResponse, dependencies=[Depends(get_current_admin_user)])
async def get_admin_stats(db: Session = Depends(get_db)):
    """
    Get admin dashboard statistics
    
    Returns:
    - Total users
    - Total premium subscribers
    - Total revenue (R99 per subscriber)
    - Quiz completion rate
    - Most common temperaments
    - Recent registrations
    - Registration growth percentage (vs last 30 days)
    """
    # Total users
    total_users = db.query(User).count()
    
    # Premium subscribers
    total_premium = db.query(User).filter(User.is_premium == True).count()
    
    # Revenue calculation (R99 per subscriber)
    total_revenue_zAR = total_premium * SUBSCRIPTION_PRICE_ZAR
    
    # Quiz completion rate
    # Users who have completed at least one quiz
    users_with_quiz = db.query(QuizResult.user_id).distinct().count()
    quiz_completion_rate = (users_with_quiz / total_users * 100) if total_users > 0 else 0
    
    # Most common temperaments (dominant)
    temperament_results = db.query(
        QuizResult.dominant_temperament,
        func.count(QuizResult.id).label('count')
    ).group_by(QuizResult.dominant_temperament).all()
    
    total_temperament_results = sum(r.count for r in temperament_results)
    
    most_common_temperaments = []
    for r in temperament_results:
        percentage = (r.count / total_temperament_results * 100) if total_temperament_results > 0 else 0
        most_common_temperaments.append({
            "temperament": r.dominant_temperament,
            "count": r.count,
            "percentage": round(percentage, 1)
        })
    
    # Sort by count descending
    most_common_temperaments.sort(key=lambda x: x["count"], reverse=True)
    
    # Recent registrations (last 7 days)
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_users = db.query(User).filter(
        User.created_at >= seven_days_ago
    ).order_by(User.created_at.desc()).limit(10).all()
    
    recent_registrations = [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "created_at": u.created_at.isoformat() if u.created_at else None,
            "is_premium": u.is_premium
        }
        for u in recent_users
    ]
    
    # Registration growth (vs previous 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    sixty_days_ago = datetime.now() - timedelta(days=60)
    
    registrations_last_30 = db.query(User).filter(
        User.created_at >= thirty_days_ago
    ).count()
    
    registrations_previous_30 = db.query(User).filter(
        User.created_at >= sixty_days_ago,
        User.created_at < thirty_days_ago
    ).count()
    
    if registrations_previous_30 > 0:
        registration_growth_percent = (
            (registrations_last_30 - registrations_previous_30) / registrations_previous_30 * 100
        )
    else:
        registration_growth_percent = 100.0 if registrations_last_30 > 0 else 0.0
    
    return AdminStatsResponse(
        total_users=total_users,
        active_subscribers=total_premium,
        monthly_revenue=total_revenue_zAR,
        quiz_completion_rate=round(quiz_completion_rate, 1),
        most_common_temperament=most_common_temperaments[0]["temperament"] if most_common_temperaments else "",
        temperament_distribution={r["temperament"]: r["count"] for r in most_common_temperaments},
        recent_registrations=recent_registrations,
        registration_growth_percent=round(registration_growth_percent, 1)
    )


@router.get("/users", dependencies=[Depends(get_current_admin_user)])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all users (paginated)
    """
    users = db.query(User).offset(skip).limit(limit).all()
    
    return {
        "total": db.query(User).count(),
        "users": [
            {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "is_premium": u.is_premium,
                "created_at": u.created_at.isoformat() if u.created_at else None
            }
            for u in users
        ]
    }


@router.get("/users/{user_id}", dependencies=[Depends(get_current_admin_user)])
async def get_user_details(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific user
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's quiz results
    quiz_results = db.query(QuizResult).filter(
        QuizResult.user_id == user_id
    ).order_by(QuizResult.created_at.desc()).all()
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "is_premium": user.is_premium,
        "subscription_id": user.payfast_subscription_id,
        "temperament_combination_id": user.temperament_combination_id,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "quiz_results": [
            {
                "session_id": r.session_id,
                "dominant_temperament": r.dominant_temperament,
                "sub_dominant_temperament": r.sub_dominant_temperament,
                "combination_name": r.combination_name,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in quiz_results
        ]
    }


@router.get("/quiz-stats", dependencies=[Depends(get_current_admin_user)])
async def get_quiz_statistics(db: Session = Depends(get_db)):
    """
    Get detailed quiz statistics
    """
    total_quizzes = db.query(QuizResult).count()
    
    # Combinations breakdown
    combination_stats = db.query(
        QuizResult.combination_name,
        func.count(QuizResult.id).label('count')
    ).group_by(QuizResult.combination_name).all()
    
    return {
        "total_quizzes": total_quizzes,
        "combinations": [
            {"name": c.combination_name, "count": c.count}
            for c in combination_stats
        ]
    }


@router.put("/users/{user_id}/premium", dependencies=[Depends(get_current_admin_user)])
async def update_user_premium_status(
    user_id: int,
    is_premium: bool,
    db: Session = Depends(get_db)
):
    """
    Update a user's premium status (admin function)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_premium = is_premium
    if is_premium and not user.payfast_subscription_id:
        user.payfast_subscription_id = f"admin_manual_{user_id}"
    
    db.commit()
    
    return {
        "status": "success",
        "user_id": user_id,
        "is_premium": user.is_premium
    }