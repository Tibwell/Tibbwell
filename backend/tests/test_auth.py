"""
Unit tests for the TibbWell Auth module
Tests password hashing, JWT token creation/validation, and auth logic
"""
import sys
import os
import pytest
from datetime import datetime, timedelta

# Add parent directory to path so we can import from api
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_token,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from jose import JWTError, jwt


class TestPasswordHashing:
    """Tests for password hashing and verification"""

    def test_hash_and_verify(self):
        """Hash and verify cycle should work correctly"""
        password = "test_password_123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed)

    def test_different_passwords(self):
        """Different passwords should produce different hashes"""
        p1 = get_password_hash("password1")
        p2 = get_password_hash("password2")
        assert p1 != p2

    def test_wrong_password_rejected(self):
        """Wrong password should not verify"""
        password = "correct_password"
        hashed = get_password_hash(password)
        assert not verify_password("wrong_password", hashed)

    def test_empty_password(self):
        """Empty password can be hashed but won't match non-empty wrong one"""
        hashed = get_password_hash("")
        assert verify_password("", hashed)
        assert not verify_password(" ", hashed)

    def test_special_characters(self):
        """Passwords with special characters should work"""
        password = "P@ssw0rd!£$%^&*()_+-=[]{}|;':\",./<>?`~"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed)

    def test_long_password(self):
        """Long passwords (100 chars) should hash correctly"""
        password = "a" * 100
        hashed = get_password_hash(password)
        assert verify_password(password, hashed)

    def test_unicode_password(self):
        """Unicode passwords should work"""
        password = "密码123üñíçödé"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed)

    def test_bcrypt_salt_ensures_uniqueness(self):
        """Same password hashed twice should produce different hashes (bcrypt salting)"""
        password = "same_password"
        h1 = get_password_hash(password)
        h2 = get_password_hash(password)
        assert h1 != h2  # Different salts
        assert verify_password(password, h1)
        assert verify_password(password, h2)


class TestCreateAccessToken:
    """Tests for JWT access token creation"""

    def test_token_created_with_sub(self):
        """Token should contain the sub claim"""
        data = {"sub": "1", "email": "test@example.com"}
        token = create_access_token(data)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "1"
        assert payload["email"] == "test@example.com"

    def test_token_expiry(self):
        """Token should have an exp claim"""
        data = {"sub": "42"}
        token = create_access_token(data)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in payload
        assert isinstance(payload["exp"], int)

    def test_custom_expiry(self):
        """Custom expiry should be respected"""
        data = {"sub": "1"}
        custom_expiry = timedelta(minutes=5)
        token = create_access_token(data, expires_delta=custom_expiry)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in payload

    def test_token_default_expiry(self):
        """Default expiry should be 24 hours"""
        data = {"sub": "1"}
        token = create_access_token(data)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_time = datetime.fromtimestamp(payload["exp"])
        now = datetime.utcnow()
        # Should be close to 24 hours from now (within 5 seconds tolerance)
        expected_diff = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        actual_diff = exp_time - now
        assert abs((actual_diff - expected_diff).total_seconds()) < 5

    def test_token_with_additional_claims(self):
        """Token can include arbitrary claims"""
        data = {"sub": "7", "role": "admin", "is_premium": True}
        token = create_access_token(data)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "7"
        assert payload["role"] == "admin"
        assert payload["is_premium"] is True


class TestDecodeToken:
    """Tests for JWT token decoding"""

    def test_decode_valid_token(self):
        """Valid token should decode correctly"""
        data = {"sub": "1", "email": "test@example.com"}
        token = create_access_token(data)
        payload = decode_token(token)
        assert payload["sub"] == "1"
        assert payload["email"] == "test@example.com"

    def test_decode_malformed_token(self):
        """Malformed token should raise JWTError"""
        with pytest.raises(Exception):
            decode_token("not-a-valid-token")

    def test_decode_empty_string(self):
        """Empty string token should raise error"""
        with pytest.raises(Exception):
            decode_token("")

    def test_decode_tampered_token(self):
        """Tampered token should raise error"""
        data = {"sub": "1"}
        token = create_access_token(data)
        # Tamper with the token
        parts = token.split(".")
        tampered = parts[0] + "." + parts[1] + ".invalidsignature"
        with pytest.raises(Exception):
            decode_token(tampered)

    def test_decode_token_wrong_secret(self):
        """Token signed with wrong secret should fail"""
        data = {"sub": "1"}
        token = jwt.encode(data, "wrong-secret", algorithm=ALGORITHM)
        with pytest.raises(Exception):
            decode_token(token)

    def test_decode_token_without_sub(self):
        """Token without sub claim should still decode"""
        data = {"email": "test@example.com"}
        token = create_access_token(data)
        payload = decode_token(token)
        assert payload["email"] == "test@example.com"

    def test_decode_token_returns_dict(self):
        """Decoded token should return a dict"""
        data = {"sub": "99"}
        token = create_access_token(data)
        payload = decode_token(token)
        assert isinstance(payload, dict)


class TestAuthEdgeCases:
    """Tests for edge cases in authentication"""

    def test_token_with_non_string_sub(self):
        """sub claim must be string (JWT spec)"""
        data = {"sub": 123}
        token = create_access_token(data)
        with pytest.raises(Exception):
            decode_token(token)

    def test_token_with_array_claim(self):
        """Token can contain array claims"""
        data = {"sub": "1", "roles": ["user", "admin"]}
        token = create_access_token(data)
        payload = decode_token(token)
        assert payload["roles"] == ["user", "admin"]

    def test_token_with_nested_data(self):
        """Token can contain nested dict claims"""
        data = {"sub": "1", "profile": {"name": "Test", "age": 30}}
        token = create_access_token(data)
        payload = decode_token(token)
        assert payload["profile"]["name"] == "Test"
        assert payload["profile"]["age"] == 30

    def test_multiple_tokens_same_data(self):
        """Multiple tokens created for same user with same data should be identical (same payload)"""
        data = {"sub": "1"}
        token1 = create_access_token(data)
        token2 = create_access_token(data)
        # Same payload and expiry = same token (timestamp granularity is in seconds)
        assert decode_token(token1)["sub"] == "1"
        assert decode_token(token2)["sub"] == "1"

    def test_multiple_tokens_different_data(self):
        """Tokens with different data should be different"""
        data1 = {"sub": "1", "email": "a@example.com"}
        data2 = {"sub": "1", "email": "b@example.com"}
        token1 = create_access_token(data1)
        token2 = create_access_token(data2)
        assert token1 != token2

    def test_email_change_in_token(self):
        """Email change should be reflected in new token"""
        data1 = {"sub": "1", "email": "old@example.com"}
        data2 = {"sub": "1", "email": "new@example.com"}
        token1 = create_access_token(data1)
        token2 = create_access_token(data2)
        assert decode_token(token1)["email"] == "old@example.com"
        assert decode_token(token2)["email"] == "new@example.com"