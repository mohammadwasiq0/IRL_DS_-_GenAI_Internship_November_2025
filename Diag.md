# 1️⃣ 🔁 Sequence Diagram (Runtime Flow)

This shows **step-by-step execution when a user sends a message**.

---

## 🎯 Scenario: User Sends Chat Message

```
User
 │
 │ 1. Enter Message
 ▼
Streamlit UI (app.py)
 │
 │ 2. process_chat(user_id, input)
 ▼
Chat Service Layer
 │
 │ 3. build_prompt(user_input)
 ▼
Prompt Manager
 │
 │ 4. Return structured prompt
 ▼
Chat Service
 │
 │ 5. generate_response(prompt)
 ▼
LLM Handler (Euriai)
 │
 │ 6. API Request
 ▼
Euriai LLM API (External)
 │
 │ 7. Response JSON
 ▼
LLM Handler
 │
 │ 8. Extract content
 ▼
Chat Service
 │
 │ 9. save_message(user)
 ▼
Memory Manager
 │
 │ 10. Insert into ChatHistory
 ▼
SQLite Database
 │
 │ 11. save_message(assistant)
 ▼
SQLite Database
 │
 │ 12. Return response
 ▼
Streamlit UI
 │
 │ 13. Render chat message
 ▼
User
```

---

## 🔐 Login Sequence

```
User
 │
 │ Enter credentials
 ▼
Streamlit UI
 │
 │ authenticate_user()
 ▼
Auth Handler
 │
 │ Query User
 ▼
SQLite DB
 │
 │ Verify Argon2 hash
 ▼
Auth Handler
 │
 │ Return user object
 ▼
Streamlit UI
 │
 │ Set session_state.user
 ▼
Authenticated Session
```

---

# 2️⃣ 🧩 Component Diagram

Shows system-level components and interactions.

```
┌─────────────────────────────────────────────┐
│                 USER                       │
└────────────────────────┬────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────┐
│              Streamlit UI                  │
│---------------------------------------------│
│ - Login/Register                           │
│ - Chat Input                               │
│ - Chat Display                             │
│ - Download CSV                             │
└────────────────────────┬────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────┐
│             Chat Service Layer             │
│---------------------------------------------│
│ - Orchestrates flow                        │
│ - Calls Prompt + LLM + Memory              │
└───────────────┬───────────────┬────────────┘
                │               │
                ▼               ▼
      ┌────────────────┐  ┌────────────────┐
      │ Prompt Module  │  │ Auth Module    │
      │----------------│  │----------------│
      │ System Role    │  │ Argon2 Hashing │
      │ Prompt Build   │  │ Verification   │
      └────────────────┘  └────────────────┘
                │
                ▼
      ┌────────────────────────────┐
      │ LLM Adapter (Euriai)       │
      │----------------------------│
      │ - API Call                 │
      │ - Response Extraction      │
      │ - Error Logging            │
      └──────────────┬─────────────┘
                     │
                     ▼
            ┌──────────────────┐
            │ Euriai Cloud LLM │
            └──────────────────┘

Database Layer:

┌────────────────────────────┐
│ SQLite Database            │
│----------------------------│
│ Users Table                │
│ ChatHistory Table          │
└────────────────────────────┘
```

---

# 3️⃣ 🗄 ER Diagram (Entity Relationship)

---

## 📊 Entities

### 🧑 User

| Field    | Type            | Description            |
| -------- | --------------- | ---------------------- |
| id       | Integer (PK)    | Unique identifier      |
| username | String (Unique) | Login username         |
| password | String          | Argon2 hashed password |

---

### 💬 ChatHistory

| Field   | Type         | Description      |
| ------- | ------------ | ---------------- |
| id      | Integer (PK) | Unique ID        |
| user_id | Integer      | References User  |
| role    | String       | user / assistant |
| message | Text         | Chat message     |

---

## 📐 ER Diagram (ASCII)

```
┌──────────────┐
│    Users     │
├──────────────┤
│ id (PK)      │
│ username     │
│ password     │
└──────┬───────┘
       │
       │ 1
       │
       │
       │ N
┌──────▼────────┐
│  ChatHistory  │
├───────────────┤
│ id (PK)       │
│ user_id (FK)  │
│ role          │
│ message       │
└───────────────┘
```

---

## 🔗 Relationship

```
One User
   ────────< Has >────────
Many Chat Messages
```

Cardinality:

```
User (1) -------- (N) ChatHistory
```

---

# 📌 Database Relationship Explanation

* Each user can have multiple messages.
* Messages are isolated via `user_id`.
* No cross-user data leakage.
* Foreign key ensures logical relationship.

---