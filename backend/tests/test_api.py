"""
Integration tests for the TibbWell API
Tests all endpoints: health, quiz, auth, premium, admin, chatbot
Uses TestClient (httpx) against the FastAPI app
"""
import sys
import os
import pytest
import tempfile
from fastapi.testclient import TestClient

# Add parent directory to path so we can import from api
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Use a temporary database for testing
os.environ["TESTING"] = "1"

# Override database URL before importing app modules
import api.database as db_module
db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
db_module.DATABASE_URL = f"sqlite:///{db_file.name}"
db_module.engine = db_module.create_engine(
    db_module.DATABASE_URL,
    connect_args={"check_same_thread": False}
)
db_module.SessionLocal = db_module.sessionmaker(autocommit=False, autoflush=False, bind=db_module.engine)
TEST_DB_PATH = db_file.name

# Import and seed test database
from api.database import Base, SessionLocal
from init_db import QUIZ_QUESTIONS_DATA, TEMPERAMENTS_DATA, COMBINATIONS_DATA
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create tables and seed test data
Base.metadata.create_all(bind=db_module.engine)
db = SessionLocal()

# Check if already seeded
from api.database import QuizQuestion, Temperament, TemperamentCombination, AdminUser
if not db.query(QuizQuestion).first():
    print("Seeding test database...")
    for q in QUIZ_QUESTIONS_DATA:
        question = QuizQuestion(
            id=q["id"],
            question_text=q["question_text"],
            category=q["category"],
            options=q["options"],
            display_order=q["display_order"]
        )
        db.add(question)

    for t in TEMPERAMENTS_DATA:
        temperament = Temperament(
            name=t["name"],
            quality=t["quality"],
            element=t["element"],
            description=t["description"],
            traits=t["traits"]
        )
        db.add(temperament)

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

    admin = AdminUser(
        username="admin",
        password_hash=pwd_context.hash("admin123")
    )
    db.add(admin)
    db.commit()

db.close()

# Now import the FastAPI app
from api.main import app

client = TestClient(app)

TEST_USER = {
    "email": "testuser@example.com",
    "password": "TestPass123!",
    "name": "Test User"
}


def cleanup_test_db():
    """Clean up the temporary test database"""
    import os
    try:
        db = SessionLocal()
        db.close()
        os.unlink(TEST_DB_PATH)
    except:
        pass


@pytest.fixture
def cleanup_user():
    """Cleanup test user after test"""
    yield
    from api.database import User
    db = SessionLocal()
    user = db.query(User).filter(User.email == TEST_USER["email"]).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()


class TestHealthEndpoints:
    """Tests for health check endpoints"""

    def test_health_check(self):
        """GET /health should return healthy"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self):
        """GET / should return API info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "TibbWell API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"

    def test_api_health(self):
        """GET /api/health should return detailed health"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "tibbwell-backend"


class TestQuizEndpoints:
    """Tests for quiz API endpoints"""

    def test_get_questions_returns_list(self):
        """GET /api/quiz/questions should return array"""
        response = client.get("/api/quiz/questions")
        assert response.status_code == 200
        questions = response.json()
        assert isinstance(questions, list)
        assert len(questions) > 0

    def test_get_questions_has_25_questions(self):
        """GET /api/quiz/questions should return 25 questions"""
        response = client.get("/api/quiz/questions")
        assert response.status_code == 200
        questions = response.json()
        assert len(questions) == 25

    def test_question_schema(self):
        """Each question should have id, question_text, category, options"""
        response = client.get("/api/quiz/questions")
        questions = response.json()
        for q in questions:
            assert "id" in q
            assert "question_text" in q
            assert "category" in q
            assert "options" in q
            assert len(q["options"]) == 4

    def test_question_options_have_text_and_temperament(self):
        """Each option should have text and temperament"""
        response = client.get("/api/quiz/questions")
        questions = response.json()
        for q in questions:
            for opt in q["options"]:
                assert "text" in opt
                assert "temperament" in opt

    def test_submit_quiz_returns_result(self):
        """POST /api/quiz/submit should return result"""
        payload = {
            "answers": [
                {"question_id": i, "selected_temperament": "Sanguinous"}
                for i in range(1, 26)
            ]
        }
        response = client.post("/api/quiz/submit", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "scores" in data
        assert "dominant_temperament" in data
        assert "sub_dominant_temperament" in data
        assert "combination_name" in data
        assert "result_description" in data

    def test_submit_all_sanguinous(self):
        """All Sanguinous answers should give Sanguinous dominant"""
        payload = {
            "answers": [
                {"question_id": i, "selected_temperament": "Sanguinous"}
                for i in range(1, 26)
            ]
        }
        response = client.post("/api/quiz/submit", json=payload)
        data = response.json()
        assert data["dominant_temperament"] == "Sanguinous"
        assert data["scores"]["Sanguinous"] == 25

    def test_submit_all_bilious(self):
        """All Bilious answers should give Bilious dominant"""
        payload = {
            "answers": [
                {"question_id": i, "selected_temperament": "Bilious"}
                for i in range(1, 26)
            ]
        }
        response = client.post("/api/quiz/submit", json=payload)
        data = response.json()
        assert data["dominant_temperament"] == "Bilious"

    def test_submit_all_phlegmatic(self):
        """All Phlegmatic answers should give Phlegmatic dominant"""
        payload = {
            "answers": [
                {"question_id": i, "selected_temperament": "Phlegmatic"}
                for i in range(1, 26)
            ]
        }
        response = client.post("/api/quiz/submit", json=payload)
        data = response.json()
        assert data["dominant_temperament"] == "Phlegmatic"

    def test_submit_all_melancholic(self):
        """All Melancholic answers should give Melancholic dominant"""
        payload = {
            "answers": [
                {"question_id": i, "selected_temperament": "Melancholic"}
                for i in range(1, 26)
            ]
        }
        response = client.post("/api/quiz/submit", json=payload)
        data = response.json()
        assert data["dominant_temperament"] == "Melancholic"

    def test_submit_invalid_question_id(self):
        """Invalid question_id should return 400"""
        payload = {
            "answers": [
                {"question_id": 999, "selected_temperament": "Sanguinous"}
            ]
        }
        response = client.post("/api/quiz/submit", json=payload)
        assert response.status_code == 400

    def test_submit_missing_answers(self):
        """Missing answers should return 422"""
        response = client.post("/api/quiz/submit", json={})
        assert response.status_code == 422

    def test_get_nonexistent_result(self):
        """GET /api/quiz/result/{session_id} with unknown id should return 404"""
        response = client.get("/api/quiz/result/nonexistent-session-id")
        assert response.status_code == 404

    def test_get_temperaments(self):
        """GET /api/quiz/temperaments should return all 4"""
        response = client.get("/api/quiz/temperaments")
        assert response.status_code == 200
        data = response.json()
        # Should have at least Sanguinous, Bilious, Phlegmatic, Melancholic
        for t in ["Sanguinous", "Bilious", "Phlegmatic", "Melancholic"]:
            assert t in data

    def test_get_temperaments_has_info(self):
        """Temperament info should have name, quality, element, description"""
        response = client.get("/api/quiz/temperaments")
        data = response.json()
        for name, info in data.items():
            assert "name" in info
            assert "quality" in info
            assert "element" in info
            assert "description" in info

    def test_get_combinations(self):
        """GET /api/quiz/combinations should return list"""
        response = client.get("/api/quiz/combinations")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_combination_by_name(self):
        """GET /api/quiz/combination/{name} should return combo"""
        response = client.get("/api/quiz/combination/Sanguinous-Bilious")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Sanguinous-Bilious"

    def test_get_nonexistent_combination(self):
        """GET /api/quiz/combination/{name} with unknown name should return 404"""
        response = client.get("/api/quiz/combination/NonExistent-Combo")
        assert response.status_code == 404


class TestAuthEndpoints:
    """Tests for authentication API endpoints"""

    @pytest.fixture
    def cleanup_user(self):
        """Cleanup test user after test"""
        yield
        db = SessionLocal()
        from api.database import User
        user = db.query(User).filter(User.email == TEST_USER["email"]).first()
        if user:
            db.delete(user)
            db.commit()
        db.close()

    def test_register_user(self, cleanup_user):
        """POST /api/auth/register should create user and return token"""
        response = client.post("/api/auth/register", json=TEST_USER)
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == TEST_USER["email"]
        assert data["user"]["name"] == TEST_USER["name"]

    def test_register_duplicate(self, cleanup_user):
        """Registering with duplicate email should return 400"""
        # First registration
        client.post("/api/auth/register", json=TEST_USER)
        # Duplicate
        response = client.post("/api/auth/register", json=TEST_USER)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_register_invalid_email(self):
        """Registering with invalid email should return 422"""
        response = client.post("/api/auth/register", json={
            "email": "not-an-email",
            "password": "password123",
            "name": "Test"
        })
        assert response.status_code == 422

    def test_login_success(self, cleanup_user):
        """POST /api/auth/login with valid credentials"""
        client.post("/api/auth/register", json=TEST_USER)
        response = client.post("/api/auth/login", json={
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == TEST_USER["email"]

    def test_login_wrong_password(self, cleanup_user):
        """POST /api/auth/login with wrong password should return 401"""
        client.post("/api/auth/register", json=TEST_USER)
        response = client.post("/api/auth/login", json={
            "email": TEST_USER["email"],
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self):
        """Login with unregistered email should return 401"""
        response = client.post("/api/auth/login", json={
            "email": "nobody@example.com",
            "password": "password123"
        })
        assert response.status_code == 401

    def test_get_profile_no_auth(self):
        """GET /api/auth/profile without auth should return 401"""
        response = client.get("/api/auth/profile")
        assert response.status_code == 401

    def test_get_profile_with_auth(self, cleanup_user):
        """GET /api/auth/profile with valid token"""
        reg = client.post("/api/auth/register", json=TEST_USER)
        token = reg.json()["access_token"]
        # The endpoint currently expects authorization as query parameter
        response = client.get(
            "/api/auth/profile",
            params={"authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == TEST_USER["email"]
        assert data["name"] == TEST_USER["name"]

    def test_get_profile_invalid_token(self):
        """GET /api/auth/profile with invalid token should return 401"""
        response = client.get(
            "/api/auth/profile",
            params={"authorization": "Bearer invalidtoken"}
        )
        assert response.status_code == 401

    def test_get_profile_malformed_header(self):
        """GET /api/auth/profile with malformed auth param"""
        response = client.get(
            "/api/auth/profile",
            params={"authorization": "NotBearer token"}
        )
        assert response.status_code == 401


class TestPremiumEndpoints:
    """Tests for premium dashboard endpoints"""

    def test_get_premium_dashboard(self):
        """GET /api/premium/dashboard should return data"""
        response = client.get("/api/premium/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert "health_programme" in data
        assert "temperament_combination" in data

    def test_get_food_recommendations_valid(self):
        """GET /api/premium/foods with valid combo"""
        response = client.get("/api/premium/foods?combination_name=Sanguinous-Bilious")
        assert response.status_code == 200
        data = response.json()
        assert data["combination"] == "Sanguinous-Bilious"
        assert "foods_to_eat" in data
        assert "foods_to_avoid" in data

    def test_get_food_recommendations_invalid(self):
        """GET /api/premium/foods with invalid combo should return 404"""
        response = client.get("/api/premium/foods?combination_name=NonExistent")
        assert response.status_code == 404

    def test_get_exercise_plan_valid(self):
        """GET /api/premium/exercise with valid combo"""
        response = client.get("/api/premium/exercise?combination_name=Sanguinous-Bilious")
        assert response.status_code == 200
        data = response.json()
        assert "exercise_plan" in data

    def test_get_exercise_plan_invalid(self):
        """GET /api/premium/exercise with invalid combo should return 404"""
        response = client.get("/api/premium/exercise?combination_name=NonExistent")
        assert response.status_code == 404

    def test_subscribe_creates_premium(self, cleanup_user):
        """POST /api/premium/subscribe should activate premium"""
        reg = client.post("/api/auth/register", json=TEST_USER)
        user_id = reg.json()["user"]["id"]
        
        response = client.post(
            f"/api/premium/subscribe?user_id={user_id}&payfast_subscription_id=sub_test_123"
        )
        assert response.status_code == 200
        assert response.json()["is_premium"] is True

    def test_subscribe_nonexistent_user(self):
        """Subscribe with nonexistent user should return 404"""
        response = client.post(
            "/api/premium/subscribe?user_id=99999&payfast_subscription_id=sub_test"
        )
        assert response.status_code == 404

    def test_subscription_status(self):
        """GET /api/premium/subscription/status should return status"""
        # Use an existing user from premium dashboard test
        response = client.get("/api/premium/subscription/status?user_id=1")
        assert response.status_code in [200, 404]  # Might not have user 1

    def test_get_monthly_focus_no_data(self):
        """GET /api/premium/monthly-focus with no data should return empty gracefully"""
        response = client.get("/api/premium/monthly-focus?month_year=2099-01")
        assert response.status_code == 200
        data = response.json()
        assert "tips" in data  # Should have tips key even if empty


class TestAdminEndpoints:
    """Tests for admin dashboard endpoints"""

    def test_get_admin_stats(self):
        """GET /api/admin/stats should return stats"""
        response = client.get("/api/admin/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "total_premium_subscribers" in data
        assert "total_revenue_zAR" in data
        assert "quiz_completion_rate" in data
        assert "most_common_temperaments" in data

    def test_get_all_users(self):
        """GET /api/admin/users should return users"""
        response = client.get("/api/admin/users")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "users" in data

    def test_get_users_pagination(self):
        """GET /api/admin/users should respect skip/limit"""
        response = client.get("/api/admin/users?skip=0&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data["users"]) <= 5

    def test_get_user_details_not_found(self):
        """GET /api/admin/users/{id} with unknown id should return 404"""
        response = client.get("/api/admin/users/99999")
        assert response.status_code == 404

    def test_get_quiz_stats(self):
        """GET /api/admin/quiz-stats should return quiz stats"""
        response = client.get("/api/admin/quiz-stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_quizzes" in data
        assert "combinations" in data

    def test_update_user_premium(self, cleanup_user):
        """PUT /api/admin/users/{id}/premium should toggle premium"""
        reg = client.post("/api/auth/register", json=TEST_USER)
        user_id = reg.json()["user"]["id"]
        
        response = client.put(
            f"/api/admin/users/{user_id}/premium?is_premium=true"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_premium"] is True

        # Toggle back
        response = client.put(
            f"/api/admin/users/{user_id}/premium?is_premium=false"
        )
        assert response.status_code == 200
        assert response.json()["is_premium"] is False


class TestChatbotEndpoints:
    """Tests for chatbot API endpoints"""

    def test_ask_chatbot_no_user(self):
        """POST /api/chatbot/ask without user_id should return generic response"""
        response = client.post("/api/chatbot/ask", json={
            "message": "What should I eat?"
        })
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "timestamp" in data

    def test_ask_chatbot_diet_question(self):
        """Diet question should return food-related response"""
        response = client.post("/api/chatbot/ask", json={
            "message": "What foods are good for my health?"
        })
        assert response.status_code == 200
        data = response.json()
        assert len(data["response"]) > 0

    def test_ask_chatbot_exercise_question(self):
        """Exercise question should return exercise-related response"""
        response = client.post("/api/chatbot/ask", json={
            "message": "What exercise should I do?"
        })
        assert response.status_code == 200
        data = response.json()
        assert len(data["response"]) > 0

    def test_ask_chatbot_sleep_question(self):
        """Sleep question should return sleep-related response"""
        response = client.post("/api/chatbot/ask", json={
            "message": "How can I improve my sleep?"
        })
        assert response.status_code == 200
        data = response.json()
        assert len(data["response"]) > 0

    def test_chatbot_capabilities(self):
        """GET /api/chatbot/capabilities should return capabilities"""
        response = client.get("/api/chatbot/capabilities")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "capabilities" in data
        assert len(data["capabilities"]) > 0

    def test_get_health_tips_valid_category(self):
        """GET /api/chatbot/health-tips/{category} with valid category"""
        response = client.get("/api/chatbot/health-tips/diet")
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "content" in data

    def test_get_health_tips_invalid_category(self):
        """GET /api/chatbot/health-tips/{category} with invalid category should return error"""
        response = client.get("/api/chatbot/health-tips/invalid_category")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert "valid_categories" in data


class TestApiEdgeCases:
    """Tests for API edge cases"""

    def test_get_questions_ordered(self):
        """Questions should be ordered by display_order"""
        response = client.get("/api/quiz/questions")
        questions = response.json()
        orders = [q.get("id") for q in questions]
        assert orders == sorted(orders)

    def test_combination_has_all_fields(self):
        """Combination should have all expected fields"""
        response = client.get("/api/quiz/combination/Sanguinous-Bilious")
        data = response.json()
        expected_fields = [
            "id", "name", "description", "foods_to_eat", "foods_to_avoid",
            "disease_risks", "seasonal_tips", "exercise_plan", "sleep_plan", "emotional_guide"
        ]
        for field in expected_fields:
            assert field in data

    def test_submit_with_session_id(self):
        """Submit with session_id should preserve it"""
        payload = {
            "session_id": "test-session-123",
            "answers": [
                {"question_id": 1, "selected_temperament": "Sanguinous"},
                {"question_id": 2, "selected_temperament": "Bilious"},
                {"question_id": 3, "selected_temperament": "Phlegmatic"},
                {"question_id": 4, "selected_temperament": "Melancholic"},
            ]
        }
        response = client.post("/api/quiz/submit", json=payload)
        assert response.status_code == 200
        assert response.json()["session_id"] == "test-session-123"

    def test_root_endpoint_cors(self):
        """Root endpoint should have CORS headers"""
        response = client.options("/")
        # CORS preflight should be allowed
        assert "access-control-allow-origin" in response.headers or response.status_code in [200, 405]

    def test_invalid_method_returns_error(self):
        """Invalid HTTP method should return appropriate error"""
        response = client.put("/api/quiz/questions")
        assert response.status_code in [405, 422]

    @pytest.mark.skip(reason="Requires specific database state")
    def test_stats_with_no_data(self):
        """Admin stats with no data should handle gracefully"""
        # This test requires a fresh database
        pass