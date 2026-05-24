"""
Database configuration and models for TibbWell
Uses SQLAlchemy with SQLite for local development
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# SQLite database URL
DATABASE_URL = "sqlite:///./tibbwell.db"

# Create engine with SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite specific
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== MODELS ====================

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_premium = Column(Boolean, default=False)
    payfast_subscription_id = Column(String(255), nullable=True)
    temperament_combination_id = Column(Integer, ForeignKey("temperament_combinations.id"), nullable=True)
    
    # Relationships
    quiz_results = relationship("QuizResult", back_populates="user")
    temperament_combination = relationship("TemperamentCombination", back_populates="users")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    options = Column(JSON, nullable=False)  # List of {text, temperament}
    display_order = Column(Integer, nullable=False)
    
    def get_options(self):
        """Return options as list of dicts"""
        return self.options if isinstance(self.options, list) else []


class QuizResult(Base):
    __tablename__ = "quiz_results"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    answers = Column(JSON, nullable=False)  # List of {question_id, selected_temperament}
    scores = Column(JSON, nullable=False)  # {temperament: score}
    dominant_temperament = Column(String(50), nullable=False)
    sub_dominant_temperament = Column(String(50), nullable=False)
    combination_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="quiz_results")


class Temperament(Base):
    __tablename__ = "temperaments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    quality = Column(String(100), nullable=False)
    element = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    traits = Column(JSON, nullable=True)  # List of trait strings


class TemperamentCombination(Base):
    __tablename__ = "temperament_combinations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    foods_to_eat = Column(JSON, nullable=True)
    foods_to_avoid = Column(JSON, nullable=True)
    disease_risks = Column(JSON, nullable=True)
    seasonal_tips = Column(JSON, nullable=True)
    exercise_plan = Column(JSON, nullable=True)
    sleep_plan = Column(JSON, nullable=True)
    emotional_guide = Column(JSON, nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="temperament_combination")
    premium_contents = relationship("PremiumContent", back_populates="combination")
    monthly_health_foci = relationship("MonthlyHealthFocus", back_populates="combination")


class PremiumContent(Base):
    __tablename__ = "premium_content"
    
    id = Column(Integer, primary_key=True, index=True)
    temperament_combination_id = Column(Integer, ForeignKey("temperament_combinations.id"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    content = Column(JSON, nullable=False)  # {food_guide, seasonal_protocol, exercise, sleep, emotional_wellness}
    
    # Relationships
    combination = relationship("TemperamentCombination", back_populates="premium_contents")


class MonthlyHealthFocus(Base):
    __tablename__ = "monthly_health_focus"
    
    id = Column(Integer, primary_key=True, index=True)
    month_year = Column(String(20), nullable=False)
    temperament_combination_id = Column(Integer, ForeignKey("temperament_combinations.id"), nullable=False)
    tip_content = Column(Text, nullable=False)
    
    # Relationships
    combination = relationship("TemperamentCombination", back_populates="monthly_health_foci")


class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all tables"""
    Base.metadata.drop_all(bind=engine)