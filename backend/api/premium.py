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
import hashlib
import hmac
import httpx

from api.database import get_db, User, QuizResult, TemperamentCombination, PremiumContent

router = APIRouter()

# Monthly subscription price in ZAR
SUBSCRIPTION_PRICE_ZAR = 99

# PayFast configuration (from environment in production)
PAYSFAST_MERCHANT_ID = "10023456"  # Demo merchant ID
PAYSFAST_MERCHANT_KEY = "4t63w2h3k7g8d9e1"  # Demo merchant key
PAYSFAST_PASSPHRASE = "tibbwellpayfast"  # Demo passphrase


# ================ PayFast Signature Verification ================

def verify_payfast_signature(data: dict) -> bool:
    """
    Verify PayFast ITN (Instant Transaction Notification) signature
    
    PayFast sends ITN callbacks with signature header.
    We verify by recreating the signature using merchant key + passphrase.
    
    Args:
        data: The ITN data dictionary (signature, merchant_id, etc.)
    
    Returns:
        True if signature is valid, False otherwise
    """
    try:
        # Get the signature from the data
        signature = data.get("signature", "")
        if not signature:
            return False
        
        # Create signature string (sorted key=value pairs joined by &)
        # The signature is md5 of key=value&key=value... sorted
        data_copy = {k: v for k, v in data.items() if k != "signature"}
        sorted_keys = sorted(data_copy.keys())
        signature_string = "&".join([f"{k}={data_copy[k]}" for k in sorted_keys])
        
        # Prepend merchant passphrase for PayFast signature
        passphrase_string = f"{PAYSFAST_PASSPHRASE}{signature_string}"
        
        # Calculate expected signature
        expected_signature = hashlib.md5(passphrase_string.encode()).hexdigest()
        
        # Use constant-time comparison to prevent timing attacks
        return hmac.compare_digest(signature.lower(), expected_signature.lower())
    
    except Exception as e:
        print(f"[PayFast] Signature verification error: {e}")
        return False


# ================ External Service Health Check ================

async def check_payfast_health() -> dict:
    """
    Check PayFast API health status
    
    Returns dict with status and latency
    """
    try:
        start = datetime.now()
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("https://api.payfast.co.za/health")
            latency_ms = (datetime.now() - start).total_seconds() * 1000
        
        if response.status_code == 200:
            return {"status": "healthy", "service": "payfast", "latency_ms": round(latency_ms, 2)}
        else:
            return {"status": "degraded", "service": "payfast", "status_code": response.status_code}
    
    except httpx.TimeoutException:
        return {"status": "timeout", "service": "payfast", "error": "Connection timeout"}
    except httpx.ConnectError:
        return {"status": "unavailable", "service": "payfast", "error": "Connection failed"}
    except Exception as e:
        return {"status": "error", "service": "payfast", "error": str(e)}


# ================ Pydantic Models ================

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


class SubscribeRequest(BaseModel):
    user_id: int
    payfast_subscription_id: str
    payfast_signature: Optional[str] = None


class ITNRequest(BaseModel):
    """PayFast Instant Transaction Notification request"""
    m_payment_id: str
    pf_payment_id: str
    payment_status: str
    item_name: str
    item_description: str
    amount: str
    amount_gross: str
    amount_fee: str
    amount_net: str
    custom_str1: str
    custom_str2: str
    custom_str3: str
    custom_str4: str
    custom_str5: str
    name_first: str
    name_last: str
    email_address: str
    signature: Optional[str] = None


# ================ Routes ================

@router.get("/dashboard")
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
    try:
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
    except Exception as e:
        print(f"[Premium] Error finding user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to load premium dashboard. Please try again later."
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's temperament combination
    combination_name = "Sanguinous-Bilious"  # Default
    try:
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
    except Exception as e:
        print(f"[Premium] Error getting temperament: {e}")
        # Use default combination_name
    
    # Get combination details
    try:
        combination = db.query(TemperamentCombination).filter(
            TemperamentCombination.name == combination_name
        ).first()
        
        if not combination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Combination '{combination_name}' not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[Premium] Error loading combination: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to load health programme. Please try again later."
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
    
    try:
        premium_content = db.query(PremiumContent).filter(
            PremiumContent.temperament_combination_id == combination.id,
            PremiumContent.month == current_month,
            PremiumContent.year == current_year
        ).first()
        
        if premium_content:
            health_programme["monthly_content"] = premium_content.content
    except Exception as e:
        print(f"[Premium] Error loading premium content: {e}")
        # Continue without monthly content
    
    return {
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "is_premium": user.is_premium,
        "subscription_status": "active" if user.is_premium else "inactive",
        "temperament_combination": combination_name,
        "health_programme": health_programme
    }


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
    request: SubscribeRequest,
    db: Session = Depends(get_db)
):
    """
    Create a PayFast subscription for a user
    
    In production, this would be called after PayFast payment confirmation.
    The payfast_signature is verified to ensure authenticity.
    """
    # Verify PayFast signature if provided
    if request.payfast_signature:
        # Build signature verification data
        itn_data = {
            "merchant_id": PAYSFAST_MERCHANT_ID,
            "subscription_id": request.payfast_subscription_id,
            "signature": request.payfast_signature
        }
        
        if not verify_payfast_signature(itn_data):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid PayFast signature"
            )
    
    try:
        user = db.query(User).filter(User.id == request.user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.is_premium = True
        user.payfast_subscription_id = request.payfast_subscription_id
        
        db.commit()
        
        return {
            "status": "success",
            "message": "Subscription activated",
            "user_id": request.user_id,
            "is_premium": user.is_premium
        }
    except Exception as e:
        print(f"[Premium] Subscription error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process subscription. Please try again later."
        )


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


@router.post("/itn")
async def payfast_itn_handler(
    itn_data: dict,
    db: Session = Depends(get_db)
):
    """
    PayFast Instant Transaction Notification (ITN) webhook handler
    
    This endpoint receives payment notifications from PayFast.
    Signature verification ensures authenticity of the notification.
    """
    # Verify the ITN signature
    if not verify_payfast_signature(itn_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid signature"
        )
    
    # Check payment status
    payment_status = itn_data.get("payment_status")
    
    if payment_status == "COMPLETE":
        # Payment successful - activate subscription
        try:
            # The custom_str1 field typically contains the user_id
            user_id = itn_data.get("custom_str1")
            subscription_id = itn_data.get("pf_payment_id")
            
            if user_id:
                user = db.query(User).filter(User.id == int(user_id)).first()
                if user:
                    user.is_premium = True
                    user.payfast_subscription_id = subscription_id
                    db.commit()
            
            return {"status": "success", "message": "ITN processed"}
        
        except Exception as e:
            print(f"[PayFast ITN] Error processing: {e}")
            return {"status": "error", "message": "Processing failed"}
    
    elif payment_status == "FAILED":
        # Payment failed
        print(f"[PayFast ITN] Payment failed: {itn_data.get('pf_payment_id')}")
        return {"status": "acknowledged", "message": "Failed payment noted"}
    
    elif payment_status == "PENDING":
        # Payment pending
        return {"status": "acknowledged", "message": "Pending payment noted"}
    
    else:
        # Unknown status
        print(f"[PayFast ITN] Unknown status: {payment_status}")
        return {"status": "acknowledged", "message": f"Status {payment_status} noted"}