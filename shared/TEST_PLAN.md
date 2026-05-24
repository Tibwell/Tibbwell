# TibbWell — Comprehensive Test Plan

## Overview
This test plan covers all sections of the TibbWell application: the Free Quiz (Section 1), Auth Flow, Premium Dashboard (Section 2), Admin Dashboard (Section 3), Chatbot, API, Frontend, and Edge Cases.

**Project Structure:**
- Backend: FastAPI (Python) → `/home/team/tibbwell/backend/`
- Frontend: Next.js 14 (TypeScript) → `/home/team/tibbwell/frontend/`
- Database: SQLite (via SQLAlchemy)

---

## 1. Quiz Flow (Section 1)

### 1.1 All 25 Questions Display
| ID | Test | Expected | Status |
|----|------|----------|--------|
| Q1.1 | GET `/api/quiz/questions` returns 25 questions | 25 items in response | |
| Q1.2 | Each question has `id`, `question_text`, `category`, `options` array | Correct schema | |
| Q1.3 | Questions ordered by `display_order` | 1 → 25 ascending | |
| Q1.4 | Each option has `text` and `temperament` | Schema validated | |
| Q1.5 | All 4 temperaments appear in options per question | 4 options per question | |

### 1.2 Option Selection Works
| ID | Test | Expected | Status |
|----|------|----------|--------|
| Q2.1 | Select option — state updates correctly | `answers` reflects selection | |
| Q2.2 | Re-select option — replaces previous selection | Old cleared, new stored | |
| Q2.3 | Navigate back — previous answer preserved | Answer still selected | |
| Q2.4 | All 25 questions can be answered | Progress reaches 25/25 | |

### 1.3 Scoring Produces Correct Temperament
| ID | Test | Expected | Status |
|----|------|----------|--------|
| Q3.1 | All Sanguinous answers → Dominant: Sanguinous | Sanguinous as dominant | |
| Q3.2 | All Bilious answers → Dominant: Bilious | Bilious as dominant | |
| Q3.3 | All Phlegmatic answers → Dominant: Phlegmatic | Phlegmatic as dominant | |
| Q3.4 | All Melancholic answers → Dominant: Melancholic | Melancholic as dominant | |
| Q3.5 | Mixed answers → Correct dominant/sub-dominant calculated | Highest two scores | |
| Q3.6 | Scores cached in sessionStorage | `tibbwell_results` key | |

### 1.4 Results Page Shows All Data
| ID | Test | Expected | Status |
|----|------|----------|--------|
| Q4.1 | Combination name displayed | `result.combination` present | |
| Q4.2 | Quality description shown | Dominant quality shown | |
| Q4.3 | Foods to Eat list displayed | 4+ items | |
| Q4.4 | Foods to Avoid list displayed | 4+ items | |
| Q4.5 | Disease Risks listed | 3+ items | |
| Q4.6 | Seasonal Tip displayed | Non-empty | |
| Q4.7 | Premium CTA visible | "Unlock Your Complete Health Programme" | |
| Q4.8 | Share buttons work | Opens WhatsApp/Facebook/X | |

### 1.5 Edge Cases — Quiz
| ID | Test | Expected | Status |
|----|------|----------|--------|
| Q5.1 | All 25 answers the same temperament | Correct dominant, ties for others | |
| Q5.2 | Equal scores across 2 temperaments (tie) | Handles tie-breaking | |
| Q5.3 | Equal scores across 3 temperaments | Picks correct top 2 | |
| Q5.4 | All 4 scores equal (minimum tie) | Deterministic result | |
| Q5.5 | Submit with missing answers | Should not be possible (UI constraint) | |
| Q5.6 | Session storage empty → redirect to quiz | Redirects to `/quiz` | |
| Q5.7 | Refreshing results page | Data persists from sessionStorage | |

---

## 2. Auth Flow

### 2.1 Registration
| ID | Test | Expected | Status |
|----|------|----------|--------|
| A1.1 | POST `/api/auth/register` with valid email/password/name | 201 Created, token returned | |
| A1.2 | Register with duplicate email | 400 Bad Request, "Email already registered" | |
| A1.3 | Register with invalid email format | Validation error | |
| A1.4 | Register with empty password | Validation error | |
| A1.5 | Token stored in localStorage | `tibbwell_token` key set | |

### 2.2 Login
| ID | Test | Expected | Status |
|----|------|----------|--------|
| A2.1 | POST `/api/auth/login` with valid credentials | 200 OK, token returned | |
| A2.2 | Login with wrong password | 401 Unauthorized | |
| A2.3 | Login with unregistered email | 401 Unauthorized | |
| A2.4 | Token stored after login | `tibbwell_token` key set | |

### 2.3 JWT Token Handling
| ID | Test | Expected | Status |
|----|------|----------|--------|
| A3.1 | GET `/api/auth/profile` with valid token | 200, user data returned | |
| A3.2 | GET `/api/auth/profile` without token | 401 Unauthorized | |
| A3.3 | GET `/api/auth/profile` with expired token | 401 Unauthorized | |
| A3.4 | GET `/api/auth/profile` with malformed token | 401 Unauthorized | |
| A3.5 | Token contains `sub` (user_id) and `email` | Valid JWT payload | |

### 2.4 Protected Routes
| ID | Test | Expected | Status |
|----|------|----------|--------|
| A4.1 | Access dashboard without token → redirect to login | Redirected | |
| A4.2 | Access dashboard with valid token → shows content | Dashboard loads | |
| A4.3 | Protected API endpoints reject unauthenticated requests | 401 | |

---

## 3. Premium Dashboard (Section 2)

### 3.1 All Sections Display
| ID | Test | Expected | Status |
|----|------|----------|--------|
| P1.1 | Food Guide section rendered | Foods to Eat/Avoid lists | |
| P1.2 | Seasonal Protocol section rendered | 4 seasons with tabs | |
| P1.3 | Exercise Plan section rendered | Recommended/avoid activities | |
| P1.4 | Sleep Plan section rendered | Hours, position, routine | |
| P1.5 | Emotional Wellness section rendered | Strengths, weaknesses, tips | |
| P1.6 | Disease Risk Profile rendered | Conditions with risk levels | |
| P1.7 | Monthly Focus banner shown | Current month focus | |

### 3.2 Data Matches Temperament
| ID | Test | Expected | Status |
|----|------|----------|--------|
| P2.1 | Dashboard returns data for user's combination | Correct combo data | |
| P2.2 | Food recommendations match temperament | Relevant foods | |
| P2.3 | Exercise plan tailored to combination | Correct type/duration | |
| P2.4 | Sleep recommendations appropriate | Correct hours/tips | |

### 3.3 Subscription Status
| ID | Test | Expected | Status |
|----|------|----------|--------|
| P3.1 | Premium user sees all content | Full programme | |
| P3.2 | Non-premium user redirected or shown upsell | Paywall/upsell | |
| P3.3 | Subscription status displayed correctly | "Premium Active" indicator | |
| P3.4 | GET `/api/premium/subscription/status` returns correct data | Active/inactive | |

---

## 4. Admin Dashboard (Section 3)

### 4.1 Login
| ID | Test | Expected | Status |
|----|------|----------|--------|
| AD1.1 | Admin login page renders | Login form visible | |
| AD1.2 | Login with valid credentials | Redirects to admin dashboard | |
| AD1.3 | Login with invalid credentials | Error message shown | |
| AD1.4 | Access admin without auth → redirect to login | Redirect | |

### 4.2 Stats Display
| ID | Test | Expected | Status |
|----|------|----------|--------|
| AD2.1 | Total users count displayed | Numeric value | |
| AD2.2 | Active subscribers count shown | Numeric value | |
| AD2.3 | Monthly revenue calculated (R99 × subscribers) | Correct calculation | |
| AD2.4 | Quiz completion rate shown | Percentage | |
| AD2.5 | Temperament distribution chart rendered | All 12 combos | |
| AD2.6 | Most common temperament highlighted | Top combo named | |

### 4.3 User Management
| ID | Test | Expected | Status |
|----|------|----------|--------|
| AD3.1 | User list shows name, email, date, temperament, status | 5+ columns | |
| AD3.2 | Toggle premium status for a user | Status updates | |
| AD3.3 | Remove premium from user | Status changes | |
| AD3.4 | Pagination works (skip/limit) | RESPECTS params | |

### 4.4 Content Management
| ID | Test | Expected | Status |
|----|------|----------|--------|
| AD4.1 | All 12 temperament combos listed in sidebar | 12 items | |
| AD4.2 | Selecting combo shows its data | Foods, risks, tips | |
| AD4.3 | PUT `/api/admin/content` updates content | Content updated | |

---

## 5. Chatbot

### 5.1 Questions Return Relevant Responses
| ID | Test | Expected | Status |
|----|------|----------|--------|
| C1.1 | Diet question → food recommendations | Food-related response | |
| C1.2 | Exercise question → exercise advice | Exercise-related response | |
| C1.3 | Sleep question → sleep tips | Sleep-related response | |
| C1.4 | Stress question → stress management | Stress-related response | |
| C1.5 | Seasonal question → seasonal protocol | Seasonal-related response | |
| C1.6 | General wellness question → general advice | Generic response | |
| C1.7 | Unknown question → default response | Default fallback | |

### 5.2 Responses Per Temperament
| ID | Test | Expected | Status |
|----|------|----------|--------|
| C2.1 | Response references user's combination name | "{combination_name}" in response | |
| C2.2 | Diet advice tailored to user's temperament | Correct foods | |
| C2.3 | Exercise advice matches temperament | Correct exercise type | |

### 5.3 Edge Cases — Chatbot
| ID | Test | Expected | Status |
|----|------|----------|--------|
| C3.1 | Empty message → prevent submission | Button disabled | |
| C3.2 | Very long message → no crash | Handled gracefully | |
| C3.3 | Special characters/emoji → handled | No errors | |
| C3.4 | No user_id (anonymous) → generic response | Default response | |
| C3.5 | User without quiz result → generic response | "Take the quiz first" | |

---

## 6. API Testing

### 6.1 Quiz Endpoints
| ID | Test | Expected | Status |
|----|------|----------|--------|
| API1.1 | GET `/api/quiz/questions` — 200, returns questions array | Valid schema | |
| API1.2 | GET `/api/quiz/questions` — schema validation | All fields present | |
| API1.3 | POST `/api/quiz/submit` — valid submission | 200, scores + combination | |
| API1.4 | POST `/api/quiz/submit` — invalid question_id | 400 Bad Request | |
| API1.5 | POST `/api/quiz/submit` — missing answers field | 422 Validation error | |
| API1.6 | GET `/api/quiz/result/{session_id}` — existing | 200, result data | |
| API1.7 | GET `/api/quiz/result/{session_id}` — not found | 404 Not Found | |
| API1.8 | GET `/api/quiz/temperaments` — returns all 4 | Sanguinous, Bilious, Phlegmatic, Melancholic | |
| API1.9 | GET `/api/quiz/combinations` — returns all 12 | 12 combination entries | |
| API1.10 | GET `/api/quiz/combination/{name}` — exists | 200 with data | |
| API1.11 | GET `/api/quiz/combination/{name}` — not found | 404 | |

### 6.2 Auth Endpoints
| ID | Test | Expected | Status |
|----|------|----------|--------|
| API2.1 | POST `/api/auth/register` — success | 201, token + user | |
| API2.2 | POST `/api/auth/register` — duplicate email | 400 | |
| API2.3 | POST `/api/auth/login` — success | 200, token + user | |
| API2.4 | POST `/api/auth/login` — wrong password | 401 | |
| API2.5 | GET `/api/auth/profile` — valid token | 200, user data | |
| API2.6 | GET `/api/auth/profile` — no token | 401 | |

### 6.3 Premium Endpoints
| ID | Test | Expected | Status |
|----|------|----------|--------|
| API3.1 | GET `/api/premium/dashboard` — with auth | 200, health programme | |
| API3.2 | GET `/api/premium/dashboard` — without auth | 401 or fallback | |
| API3.3 | GET `/api/premium/foods` — valid combo | 200, food data | |
| API3.4 | GET `/api/premium/foods` — invalid combo | 404 | |
| API3.5 | GET `/api/premium/exercise` — valid combo | 200, exercise plan | |
| API3.6 | GET `/api/premium/subscription/status` — existing user | 200, status | |
| API3.7 | GET `/api/premium/subscription/status` — not found | 404 | |
| API3.8 | POST `/api/premium/subscribe` — activate | 200, success | |

### 6.4 Admin Endpoints
| ID | Test | Expected | Status |
|----|------|----------|--------|
| API4.1 | GET `/api/admin/stats` — returns stats | All metrics present | |
| API4.2 | GET `/api/admin/users` — paginated | skip/limit respected | |
| API4.3 | GET `/api/admin/users/{id}` — existing | 200, details + quiz results | |
| API4.4 | GET `/api/admin/users/{id}` — not found | 404 | |
| API4.5 | GET `/api/admin/quiz-stats` — returns stats | total + combo breakdown | |
| API4.6 | PUT `/api/admin/users/{id}/premium` — toggle | Status updated | |

### 6.5 Chatbot Endpoints
| ID | Test | Expected | Status |
|----|------|----------|--------|
| API5.1 | POST `/api/chatbot/ask` — with user_id | 200, temperament-aware response | |
| API5.2 | POST `/api/chatbot/ask` — without user_id | 200, generic response | |
| API5.3 | GET `/api/chatbot/capabilities` — returns capabilities | All categories listed | |
| API5.4 | GET `/api/chatbot/health-tips/{category}` — valid | 200, tips by temperament | |
| API5.5 | GET `/api/chatbot/health-tips/{category}` — invalid | Error + valid categories | |

### 6.6 Health & Root Endpoints
| ID | Test | Expected | Status |
|----|------|----------|--------|
| API6.1 | GET `/` — API info | name, version, status | |
| API6.2 | GET `/health` — health check | status: healthy | |
| API6.3 | GET `/api/health` — detailed health | status, service, version | |

---

## 7. Frontend Testing

### 7.1 Mobile Responsive
| ID | Test | Expected | Status |
|----|------|----------|--------|
| F1.1 | Landing page renders at 375px width | No overflow, readable | |
| F1.2 | Quiz page renders at 375px width | Options stack vertically | |
| F1.3 | Results page renders at 375px width | 2-column → single column | |
| F1.4 | Dashboard renders at 375px width | Sidebar hidden, hamburger menu | |
| F1.5 | Admin dashboard renders at 768px width | Layout adapts | |
| F1.6 | Chatbot at 375px width | Input area usable | |

### 7.2 Green/White Theme Consistent
| ID | Test | Expected | Status |
|----|------|----------|--------|
| F2.1 | Wellness green (#2d6a4f) used consistently | Primary buttons, headers | |
| F2.2 | Wellness light (#d8f3dc) for pale backgrounds | Section backgrounds | |
| F2.3 | Wellness dark (#1b4332) for dark text | Headings, footer | |
| F2.4 | Wellness accent (#52b788) for accents | CTA highlights | |
| F2.5 | White backgrounds for cards | Card components | |

### 7.3 All Pages Load
| ID | Test | Expected | Status |
|----|------|----------|--------|
| F3.1 | `/` — Landing page loads | All 7 sections visible | |
| F3.2 | `/quiz` — Quiz page loads | First question visible | |
| F3.3 | `/quiz/results` — Results page loads | Results or redirect | |
| F3.4 | `/dashboard` — Dashboard loads (authed) | Full dashboard | |
| F3.5 | `/dashboard/ask` — Chatbot loads | Chat interface | |
| F3.6 | `/admin` — Admin dashboard loads (authed) | Stats + tabs | |
| F3.7 | `/admin/login` — Admin login loads | Login form | |
| F3.8 | All pages — no 404 or 500 errors | HTTP 200 | |
| F3.9 | All pages — no console errors | Clean console | |

---

## 8. Edge Cases

### 8.1 Empty States
| ID | Test | Expected | Status |
|----|------|----------|--------|
| E1.1 | Admin stats — no users in DB | Stats show 0 values gracefully | |
| E1.2 | Quiz results — no session data → redirect | Redirect to quiz | |
| E1.3 | Dashboard — no quiz taken for user | Graceful message | |
| E1.4 | Chatbot — no user_id | Generic response | |
| E1.5 | Admin user list — no users | Empty table with message | |
| E1.6 | Monthly health focus — no data for month | "No focus tips yet" message | |

### 8.2 Error States
| ID | Test | Expected | Status |
|----|------|----------|--------|
| E2.1 | Backend unreachable → frontend shows error | Error boundary or message | |
| E2.2 | Invalid API response → handled gracefully | Graceful degradation | |
| E2.3 | Database initialization failure | Error logged, app doesn't start | |
| E2.4 | Token expired → redirect to login | Redirect + clear token | |
| E2.5 | Invalid combination name in URL | 404 page or error | |
| E2.6 | Invalid category for health tips | Error + valid categories | |

### 8.3 Loading States
| ID | Test | Expected | Status |
|----|------|----------|--------|
| E3.1 | Quiz results page shows spinner while loading | Loading animation | |
| E3.2 | Dashboard shows spinner while loading data | Loading animation | |
| E3.3 | Admin dashboard shows spinner while loading | Loading animation | |
| E3.4 | Chatbot shows typing indicator while "thinking" | Typing animation | |
| E3.5 | Auth form shows loading state during submission | Button disabled + spinner | |

### 8.4 Security
| ID | Test | Expected | Status |
|----|------|----------|--------|
| E4.1 | JWT secret not in client-side code | Server-side only | |
| E4.2 | Password hashed (bcrypt) | Not stored in plaintext | |
| E4.3 | SQL injection prevention | Parameterized queries | |
| E4.4 | XSS prevention via React | Content escaped | |

---

## 9. Backend Unit Tests (Implemented)

The following tests have been implemented in `/home/team/tibbwell/backend/tests/`:

### `test_quiz.py`
- `test_calculate_temperament_scores_all_sanguinous` — All answers map to Sanguinous
- `test_calculate_temperament_scores_mixed` — Mixed answers produce correct scores
- `test_calculate_temperament_scores_empty` — Empty answers produce zero scores
- `test_calculate_temperament_scores_invalid_temperament` — Invalid temperament ignored
- `test_determine_dominant_temperaments_normal` — Highest score is dominant
- `test_determine_dominant_temperaments_tie` — Tie-breaking works
- `test_determine_dominant_temperaments_all_equal` — All equal handled
- `test_get_combination_name_valid` — Valid combo returns correct name
- `test_get_combination_name_reverse` — Reverse order maps correctly
- `test_get_combination_name_nonexistent` — Falls back to "{dominant}-{sub_dominant}"
- `test_submit_quiz_invalid_question_id` — Rejects invalid question IDs

### `test_auth.py`
- `test_password_hashing` — Hash and verify cycle works
- `test_password_hashing_different` — Different passwords produce different hashes
- `test_create_access_token` — Token created with correct sub
- `test_decode_token_valid` — Valid token decodes correctly
- `test_decode_token_expired` — Expired token raises error
- `test_decode_token_malformed` — Malformed token raises error
- `test_register_duplicate_email` — Duplicate email rejected
- `test_login_invalid_credentials` — Wrong password rejected

### `test_api.py`
- `test_health_check` — `/health` returns healthy
- `test_root_endpoint` — `/` returns API info
- `test_get_questions_returns_list` — Questions endpoint returns array
- `test_submit_quiz_returns_result` — Submit returns result structure
- `test_get_nonexistent_result` — 404 for unknown session
- `test_get_temperaments` — All 4 temperaments returned
- `test_get_combinations` — All 12 combinations returned
- `test_get_nonexistent_combination` — 404 for unknown combo
- `test_register_user` — Register creates user and returns token
- `test_register_duplicate` — Duplicate email handled
- `test_login_success` — Login returns token
- `test_login_wrong_password` — Wrong password rejected
- `test_get_profile_no_auth` — No auth header rejected
- `test_get_premium_dashboard` — Dashboard returns data
- `test_get_food_recommendations_valid` — Foods returned for valid combo
- `test_get_food_recommendations_invalid` — 404 for invalid combo
- `test_get_admin_stats` — Stats endpoint works
- `test_get_all_users` — Users endpoint works
- `test_get_user_details_not_found` — 404 for unknown user
- `test_get_monthly_focus_no_data` — Graceful empty response
- `test_update_user_premium` — Premium toggle works
- `test_ask_chatbot_no_user` — Works without user
- `test_ask_chatbot_invalid_category` — Health tips returns error
- `test_chatbot_capabilities` — Returns capabilities

---

## Test Execution Instructions

### Backend Tests (Python/pytest)
```bash
cd /home/team/tibbwell/backend
source venv/bin/activate
python -m pytest tests/ -v --maxfail=5
```

### Backend with Coverage
```bash
cd /home/team/tibbwell/backend
source venv/bin/activate
python -m pytest tests/ -v --cov=api --cov-report=term
```

---

## Environment Requirements
- Python 3.12+ with venv activated
- Node.js 18+ with npm packages installed
- SQLite database initialized (`python init_db.py`)
- Backend running on port 8000 (`uvicorn api.main:app --host 0.0.0.0 --port 8000`)
