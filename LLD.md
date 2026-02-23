# 🏗 Low-Level Design (LLD)

## Production-Ready GenAI Career Advisor Chatbot

---

# 1️⃣ Module-Level Breakdown

```
genai_chatbot/
│
├── app.py
├── config.py
│
├── auth/
│   └── auth_handler.py
│
├── database/
│   ├── db.py
│   └── models.py
│
├── memory/
│   └── memory_manager.py
│
├── prompts/
│   └── prompt_manager.py
│
├── llm/
│   └── euriai_handler.py
│
├── services/
│   └── chat_service.py
│
├── utils/
│   └── logger.py
```

---

# 2️⃣ Configuration Layer

## 📁 `config.py`

### Responsibility:

Centralized environment configuration.

### Implementation Details:

```python
class Config:
    EURI_API_KEY: str
    DATABASE_URL: str
    SECRET_KEY: str
```

### Behavior:

* Loads `.env`
* Provides application-wide configuration
* Prevents hardcoded secrets

---

# 3️⃣ Database Layer

---

## 📁 `database/db.py`

### Responsibility:

* Create database engine
* Create session factory
* Provide Base ORM class

### Components:

```python
engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

### Design Pattern:

* Singleton DB engine
* Scoped sessions per operation

---

## 📁 `database/models.py`

### User Model

```python
class User(Base):
    id: int (PK)
    username: str (Unique)
    password: str (Argon2 hash)
```

### ChatHistory Model

```python
class ChatHistory(Base):
    id: int (PK)
    user_id: int
    role: str
    message: text
```

### Relationship Logic:

* `user_id` acts as foreign key (logical association)
* Enables user-specific data isolation

---

# 4️⃣ Authentication Module

## 📁 `auth/auth_handler.py`

---

## 🔹 `hash_password(password: str) -> str`

### Logic:

* Use Argon2 via passlib
* Generate salted secure hash

### Security:

* One-way hashing
* Resistant to rainbow tables
* No length limitation

---

## 🔹 `verify_password(plain, hashed) -> bool`

### Logic:

* Argon2 verification
* Constant-time comparison

---

## 🔹 `register_user(username, password)`

### Steps:

1. Create DB session
2. Check if username exists
3. Hash password
4. Insert new user
5. Commit
6. Close session

---

## 🔹 `authenticate_user(username, password)`

### Steps:

1. Fetch user by username
2. Verify password hash
3. Return user object if valid
4. Else return None

---

# 5️⃣ Memory Layer

## 📁 `memory/memory_manager.py`

---

## 🔹 `save_message(user_id, role, message)`

### Steps:

1. Create DB session
2. Insert ChatHistory record
3. Commit
4. Close session

---

## 🔹 `get_chat_history(user_id)`

### Steps:

1. Query ChatHistory by user_id
2. Return list of objects

---

### Data Stored:

| Field   | Description           |
| ------- | --------------------- |
| role    | "user" or "assistant" |
| message | Full text content     |

---

# 6️⃣ Prompt Engineering Module

## 📁 `prompts/prompt_manager.py`

---

## 🔹 `build_prompt(user_input: str) -> str`

### Structure:

```
SYSTEM_PROMPT
+
User Question
```

### System Prompt Responsibilities:

* Define AI role (Career Advisor)
* Constrain hallucinations
* Force structured output
* Maintain tone

---

# 7️⃣ LLM Adapter Layer

## 📁 `llm/euriai_handler.py`

---

## Initialization

```python
client = EuriaiClient(
    api_key=Config.EURI_API_KEY,
    model="gpt-4.1-nano"
)
```

Singleton-style client initialization.

---

## 🔹 `generate_response(prompt: str) -> str`

### Execution Steps:

1. Call `client.generate_completion`
2. Receive full JSON response
3. Extract:

   ```
   response["choices"][0]["message"]["content"]
   ```
4. Return assistant message

---

## Error Handling

```python
except Exception as e:
    logger.error(...)
    return error_message
```

Ensures:

* No crash propagation
* UI receives fallback message
* Logs written to file

---

# 8️⃣ Application Service Layer

## 📁 `services/chat_service.py`

---

## 🔹 `process_chat(user_id, user_input)`

### Detailed Flow:

```
1. Build Prompt
2. Call LLM
3. Save user message
4. Save assistant message
5. Return assistant message
```

---

### Pseudocode:

```python
prompt = build_prompt(user_input)
response = generate_response(prompt)

save_message(user_id, "user", user_input)
save_message(user_id, "assistant", response)

return response
```

---

### Responsibility:

Central orchestration layer.

Does NOT:

* Directly manage DB queries
* Directly manage API configuration
* Contain UI code

---

# 9️⃣ Presentation Layer

## 📁 `app.py`

---

## Responsibilities:

* Handle session_state
* Render login/register
* Render chat interface
* Trigger chat_service
* Display history
* Allow CSV download

---

## Chat Execution Flow

```python
if user_input:
    response = process_chat(user_id, user_input)
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(response)
```

---

## Session Management

```python
st.session_state.user
```

Used for:

* Authentication state
* Prevent unauthorized access

---

# 🔟 Error Handling Design

| Layer | Strategy                      |
| ----- | ----------------------------- |
| LLM   | Try/Except + Logging          |
| Auth  | Graceful return None          |
| DB    | Session close after operation |
| UI    | Display safe error message    |

---

# 1️⃣1️⃣ Logging Design

## 📁 `utils/logger.py`

* File-based logging
* Timestamped entries
* ERROR level tracking

Example log:

```
2026-02-19 - ERROR - Euriai Error: Rate limit exceeded
```

---

# 1️⃣2️⃣ Data Structures

---

## User Object

```
{
  id: int,
  username: str,
  password: str
}
```

---

## ChatHistory Object

```
{
  id: int,
  user_id: int,
  role: str,
  message: str
}
```

---

## LLM Response JSON

```
{
  "choices": [
      {
          "message": {
              "role": "assistant",
              "content": "..."
          }
      }
  ]
}
```

---

# 1️⃣3️⃣ Runtime Sequence (Detailed)

```
User → UI → chat_service
     → build_prompt
     → euriai_handler
     → Euriai API
     → Extract content
     → Save user message
     → Save assistant message
     → Return response
     → UI render
```

---

# 1️⃣4️⃣ Security Internals

* Argon2 hashing
* No raw password stored
* API keys hidden in .env
* No SQL injection (ORM used)
* User-level isolation

---

# 1️⃣5️⃣ Performance Considerations

* Lightweight SQLite
* Stateless LLM calls
* Minimal memory footprint
* Single-threaded Streamlit
* No global mutable state

---

# 1️⃣6️⃣ Extensibility Points

You can easily add:

* Token tracking table
* Role-based access
* Redis cache
* PostgreSQL backend
* RAG module
* Multi-model routing

Because LLM and DB are abstracted.

---

# 🎯 Interview-Level Summary

“This system uses a modular layered architecture.
Each module has single responsibility: authentication, prompt construction, memory persistence, LLM invocation, and UI rendering.

The chat_service acts as the orchestration layer.
The LLM adapter layer abstracts external model calls.
Database operations are isolated via ORM.

This makes the system secure, maintainable, and scalable.”

---