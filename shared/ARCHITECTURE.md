# TibbWell Architecture

## Tech Stack
- **Backend**: Python FastAPI + PostgreSQL + SQLAlchemy
- **Frontend**: Next.js 14 (React) + Tailwind CSS + TypeScript
- **Auth**: JWT-based authentication
- **Payments**: PayFast subscription billing (R99/month)
- **AI Chatbot**: Claude API (for "Ask TibbWell" feature)
- **Database**: PostgreSQL

## Project Structure
```
/home/team/tibbwell/
├── backend/
│   ├── db/
│   │   ├── schema.sql          # Database tables
│   │   └── seed.sql            # Temperament data, health content
│   ├── api/
│   │   ├── main.py             # FastAPI app entry
│   │   ├── auth.py             # Auth endpoints (register, login, profile)
│   │   ├── quiz.py             # Quiz questions, scoring, results
│   │   ├── premium.py          # Premium dashboard endpoints + PayFast
│   │   ├── admin.py            # Admin dashboard endpoints
│   │   └── chatbot.py          # Claude API integration
│   └── requirements.txt
├── frontend/
│   ├── app/                    # Next.js 14 App Router pages
│   ├── components/             # Reusable components
│   └── public/                 # Static assets
└── shared/
    └── ARCHITECTURE.md
```

## Database Tables
1. **users** — id, email, password_hash, name, created_at, is_premium, payfast_subscription_id
2. **quiz_questions** — id, question_text, category, options (JSON array)
3. **quiz_results** — id, user_id (nullable for anonymous), answers (JSON), dominant_temperament, sub_dominant_temperament, combination, created_at
4. **temperaments** — id, name (Sanguinous/Bilious/Phlegmatic/Melancholic), quality, description, traits
5. **temperament_combinations** — id, combination_name, description, foods_to_eat (JSON), foods_to_avoid (JSON), disease_risks (JSON), seasonal_tips (JSON), exercise_plan, sleep_plan, emotional_guide
6. **premium_content** — id, temperament_combination_id, month, content (JSON with food guide, seasonal protocol, exercise, sleep, emotional wellness)
7. **monthly_health_focus** — id, month_year, temperament_combination_id, tip_content
8. **admin_users** — id, username, password_hash

## API Endpoints
- `GET /api/quiz/questions` — Get all quiz questions
- `POST /api/quiz/submit` — Submit quiz answers, get results
- `POST /api/auth/register` — Register user
- `POST /api/auth/login` — Login
- `GET /api/auth/profile` — Get user profile
- `POST /api/payfast/subscribe` — Create PayFast subscription
- `POST /api/payfast/webhook` — PayFast IPN webhook
- `GET /api/premium/dashboard` — Get full health programme
- `POST /api/chatbot/ask` — Ask TibbWell AI (premium only)
- `GET /api/admin/stats` — Admin dashboard stats
- `PUT /api/admin/content` — Update health content

## Temperament Scoring
The 25 questions assess 4 temperaments. Each answer maps to one temperament type:
- **Sanguinous (Hot & Moist)** — Air element
- **Bilious/Choleric (Hot & Dry)** — Fire element
- **Phlegmatic (Cold & Moist)** — Water element
- **Melancholic (Cold & Dry)** — Earth element

Scoring: Sum points per temperament type. Highest = Dominant, Second highest = Sub-dominant.

## PayFast Integration
- Monthly subscription: R99/month
- Use PayFast standard subscription URL with ITN (Instant Transaction Notification)
- Webhook to update user premium status

## Frontend Pages
1. `/` — Marketing Landing Page (Section 4)
2. `/quiz` — Free Quiz (Section 1)
3. `/quiz/results` — Quiz Results (free + premium preview)
4. `/dashboard` — Premium Dashboard (Section 2)
5. `/dashboard/ask` — Ask TibbWell Chatbot
6. `/admin` — Admin Dashboard (Section 3)