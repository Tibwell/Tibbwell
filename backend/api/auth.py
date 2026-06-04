"""
Authentication endpoints for TibbWell
Uses SQLite database for user storage
"""
from fastapi import APIRouter, HTTPException, status, Depends, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional
import re
import uuid

from api.database import get_db, User

# Password hashing context - bcrypt cost factor 12
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

# JWT settings - in production, use environment variables
SECRET_KEY = "your-secret-key-here-change-in-production"
REFRESH_SECRET_KEY = "your-refresh-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 minutes
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Rate limiting - in-memory store (IP -> list of timestamps)
rate_limit_store: dict = {}  # {ip: [timestamp1, timestamp2, ...]}
RATE_LIMIT_REQUESTS = 20  # requests per minute
RATE_LIMIT_WINDOW = 60  # seconds

# Account lockout settings
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15

router = APIRouter()


# ================ Pydantic Models ================

class UserRegister(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    name: str = Field(..., min_length=2, max_length=100)

    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60
    user: dict


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    is_premium: bool
    email_verified: bool
    created_at: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)


# ================ Helper Functions ================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh", "jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def hash_refresh_token(token: str) -> str:
    """Hash a refresh token for storage"""
    return pwd_context.hash(token)


def decode_access_token(token: str) -> dict:
    """Decode and validate an access token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


def decode_refresh_token(token: str) -> dict:
    """Decode and validate a refresh token"""
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )


def check_rate_limit(client_ip: str) -> bool:
    """Check if IP is within rate limits. Returns True if allowed, False if exceeded."""
    now = datetime.utcnow().timestamp()
    if client_ip not in rate_limit_store:
        rate_limit_store[client_ip] = []
    
    # Remove timestamps outside the window
    rate_limit_store[client_ip] = [
        ts for ts in rate_limit_store[client_ip]
        if now - ts < RATE_LIMIT_WINDOW
    ]
    
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT_REQUESTS:
        return False
    
    rate_limit_store[client_ip].append(now)
    return True


def get_client_ip(authorization: str = None, x_forwarded_for: str = None) -> str:
    """Get client IP from request headers"""
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    # In production, get from request directly
    return "unknown"


def generate_verification_token() -> str:
    """Generate a secure verification token"""
    return str(uuid.uuid4())


def generate_reset_token() -> str:
    """Generate a secure reset token"""
    return str(uuid.uuid4())


# ================ Routes ================

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    
    Returns access + refresh tokens for immediate login
    """
    # Sanitize name
    name = user.name.strip()
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create verification token
    verification_token = generate_verification_token()
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    
    new_user = User(
        email=user.email,
        password_hash=hashed_password,
        name=name,
        is_premium=False,
        email_verified=False,
        verification_token=verification_token
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(new_user.id), "email": user.email}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(new_user.id), "email": user.email}
    )
    
    # Store hashed refresh token
    new_user.refresh_token_hash = hash_refresh_token(refresh_token)
    db.commit()
    
    # In production: send verification email here
    # For now, we'll include the token in the response (development only)
    print(f"[DEV] Verification token for {user.email}: {verification_token}")
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": new_user.id,
            "email": new_user.email,
            "name": new_user.name,
            "is_premium": False,
            "email_verified": False
        }
    )


@router.post("/login")
async def login(
    user: UserLogin,
    db: Session = Depends(get_db),
    x_forwarded_for: str = None
):
    """
    Login with email and password
    
    Returns access + refresh tokens on successful authentication.
    Rate limited to 20 requests/minute per IP.
    Account locked after 5 failed attempts for 15 minutes.
    """
    client_ip = get_client_ip(x_forwarded_for=x_forwarded_for)
    
    # Check rate limit
    if not check_rate_limit(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later."
        )
    
    # Find user by email
    found_user = db.query(User).filter(User.email == user.email).first()
    
    if not found_user:
        # Still perform a hash computation to prevent timing attacks
        pwd_context.hash("dummy_password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if account is locked
    if found_user.locked_until and found_user.locked_until > datetime.utcnow():
        remaining_minutes = int((found_user.locked_until - datetime.utcnow()).total_seconds() / 60)
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=f"Account locked due to too many failed attempts. Try again in {remaining_minutes} minutes."
        )
    
    # Verify password
    if not verify_password(user.password, found_user.password_hash):
        # Increment failed attempts
        found_user.failed_attempts += 1
        
        if found_user.failed_attempts >= MAX_LOGIN_ATTEMPTS:
            found_user.locked_until = datetime.utcnow() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail=f"Account locked due to too many failed attempts. Try again in {LOCKOUT_DURATION_MINUTES} minutes."
            )
        
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check email verification
    if not found_user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email first. Check your inbox for the verification link."
        )
    
    # Reset failed attempts on successful login
    found_user.failed_attempts = 0
    found_user.locked_until = None
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(found_user.id), "email": found_user.email}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(found_user.id), "email": found_user.email}
    )
    
    # Store hashed refresh token
    found_user.refresh_token_hash = hash_refresh_token(refresh_token)
    db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": found_user.id,
            "email": found_user.email,
            "name": found_user.name,
            "is_premium": found_user.is_premium,
            "email_verified": found_user.email_verified
        }
    )


@router.post("/refresh")
async def refresh_token(refresh_req: RefreshRequest, db: Session = Depends(get_db)):
    """
    Refresh access token using a valid refresh token
    
    Returns new access + refresh token pair
    """
    # Decode refresh token
    payload = decode_refresh_token(refresh_req.refresh_token)
    user_id = int(payload.get("sub"))
    
    # Get user and verify refresh token hash
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.refresh_token_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Verify the refresh token matches the stored hash
    # We need to verify against the hash - but since we can't reverse the hash,
    # we verify by checking if a fresh hash of the token matches
    if not pwd_context.verify(refresh_req.refresh_token, user.refresh_token_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Create new tokens
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    new_refresh_token = create_refresh_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    # Update stored refresh token hash
    user.refresh_token_hash = hash_refresh_token(new_refresh_token)
    db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "is_premium": user.is_premium,
            "email_verified": user.email_verified
        }
    )


@router.get("/profile", response_model=UserResponse)
async def get_profile(authorization: str = None, db: Session = Depends(get_db)):
    """
    Get the current user's profile
    
    Requires Authorization header with Bearer token
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
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
        
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            is_premium=user.is_premium,
            email_verified=user.email_verified,
            created_at=user.created_at.isoformat() if user.created_at else ""
        )
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


@router.post("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Verify user email using the verification token sent during registration
    """
    user = db.query(User).filter(User.verification_token == token).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token"
        )
    
    if user.email_verified:
        return {"message": "Email already verified"}
    
    user.email_verified = True
    user.verification_token = None  # Clear the token after use
    db.commit()
    
    return {"message": "Email verified successfully"}


@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Request a password reset link. Generates a token valid for 1 hour.
    """
    user = db.query(User).filter(User.email == request.email).first()
    
    # Always return success to prevent email enumeration
    # In production, send email with reset link if user exists
    if not user:
        return {"message": "If the email exists, a reset link has been sent"}
    
    # Generate reset token
    reset_token = generate_reset_token()
    user.reset_token = reset_token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    
    # In production: send email via Resend API
    # For now, log the token (development only)
    print(f"[DEV] Password reset token for {request.email}: {reset_token}")
    
    return {"message": "If the email exists, a reset link has been sent"}


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Reset password using a valid reset token. Token expires after 1 hour.
    """
    user = db.query(User).filter(User.reset_token == request.token).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )
    
    if not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired. Please request a new one."
        )
    
    # Update password
    user.password_hash = get_password_hash(request.new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    user.refresh_token_hash = None  # Invalidate all refresh tokens
    user.failed_attempts = 0
    user.locked_until = None
    db.commit()
    
    return {"message": "Password reset successfully. Please login with your new password."}