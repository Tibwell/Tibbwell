-- TibbWell Database Schema
-- PostgreSQL

-- Drop tables if they exist (for clean re-creation)
DROP TABLE IF EXISTS monthly_health_focus CASCADE;
DROP TABLE IF EXISTS premium_content CASCADE;
DROP TABLE IF EXISTS quiz_results CASCADE;
DROP TABLE IF EXISTS temperament_combinations CASCADE;
DROP TABLE IF EXISTS temperaments CASCADE;
DROP TABLE IF EXISTS quiz_questions CASCADE;
DROP TABLE IF EXISTS admin_users CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 1. Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_premium BOOLEAN DEFAULT FALSE,
    payfast_subscription_id VARCHAR(255),
    temperament_combination_id INTEGER
);

-- 2. Quiz Questions table
CREATE TABLE quiz_questions (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    category VARCHAR(100),
    options JSONB NOT NULL,
    display_order INTEGER NOT NULL
);

-- 3. Quiz Results table
CREATE TABLE quiz_results (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255),
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    answers JSONB NOT NULL,
    scores JSONB NOT NULL,
    dominant_temperament VARCHAR(50) NOT NULL,
    sub_dominant_temperament VARCHAR(50) NOT NULL,
    combination_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Temperaments table (the 4 base types)
CREATE TABLE temperaments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    quality VARCHAR(100) NOT NULL,
    element VARCHAR(50) NOT NULL,
    description TEXT,
    traits JSONB
);

-- 5. Temperament Combinations table
CREATE TABLE temperament_combinations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    foods_to_eat JSONB,
    foods_to_avoid JSONB,
    disease_risks JSONB,
    seasonal_tips JSONB,
    exercise_plan JSONB,
    sleep_plan JSONB,
    emotional_guide JSONB
);

-- Add foreign key constraint for users.temperament_combination_id
ALTER TABLE users 
ADD CONSTRAINT fk_temperament_combination 
FOREIGN KEY (temperament_combination_id) 
REFERENCES temperament_combinations(id) ON DELETE SET NULL;

-- 6. Premium Content table
CREATE TABLE premium_content (
    id SERIAL PRIMARY KEY,
    temperament_combination_id INTEGER REFERENCES temperament_combinations(id) ON DELETE CASCADE,
    month INTEGER NOT NULL CHECK (month >= 1 AND month <= 12),
    year INTEGER NOT NULL,
    content JSONB NOT NULL
);

-- 7. Monthly Health Focus table
CREATE TABLE monthly_health_focus (
    id SERIAL PRIMARY KEY,
    month_year VARCHAR(20) NOT NULL,
    temperament_combination_id INTEGER REFERENCES temperament_combinations(id) ON DELETE CASCADE,
    tip_content TEXT NOT NULL
);

-- 8. Admin Users table
CREATE TABLE admin_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_temperament_combination ON users(temperament_combination_id);
CREATE INDEX idx_quiz_results_user_id ON quiz_results(user_id);
CREATE INDEX idx_quiz_results_session_id ON quiz_results(session_id);
CREATE INDEX idx_quiz_results_dominant_temperament ON quiz_results(dominant_temperament);
CREATE INDEX idx_premium_content_combination ON premium_content(temperament_combination_id);
CREATE INDEX idx_premium_content_month_year ON premium_content(month, year);
CREATE INDEX idx_monthly_health_focus_combination ON monthly_health_focus(temperament_combination_id);