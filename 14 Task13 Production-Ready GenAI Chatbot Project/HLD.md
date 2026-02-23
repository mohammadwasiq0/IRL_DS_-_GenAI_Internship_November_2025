
# 🏗 High-Level Design (HLD)

## Production-Ready GenAI Career Advisor Chatbot

---

# 1️⃣ System Overview

The system is a **domain-specific AI chatbot** that provides structured career guidance using an external LLM (Euriai – `gpt-4.1-nano`).

It supports:

* User authentication
* Multi-turn conversation
* Persistent chat history
* Downloadable conversation logs
* Modular LLM integration
* Secure API key management
* Cloud deployment readiness

The system follows a **layered modular architecture** with clear separation of concerns.

---

# 2️⃣ Architectural Goals

### 🎯 Functional Goals

* Provide intelligent career guidance
* Maintain conversation context
* Store user chat history
* Allow users to download history
* Support secure login/register

### 🎯 Non-Functional Goals

* Security (Argon2 hashing)
* Scalability (modular LLM layer)
* Maintainability (clean architecture)
* Deployability (EC2 ready)
* Observability (logging system)

---

# 3️⃣ System Architecture Overview

```
User
  ↓
Streamlit UI
  ↓
Application Layer (Chat Service)
  ↓
Domain Layer (Auth + Prompt + Memory)
  ↓
Infrastructure Layer (LLM + DB + Logging)
  ↓
External LLM API (Euriai)
```

---

# 4️⃣ Architectural Layers

---

## 🔵 4.1 Presentation Layer

### Component: Streamlit UI (`app.py`)

### Responsibilities:

* Render chat interface
* Handle login/register
* Capture user input
* Display AI responses
* Display chat history
* Allow CSV download

### Key Features:

* Session-based login management
* Chat-style UI
* Real-time interaction
* Download button

This layer does NOT contain:

* Business logic
* LLM logic
* Database queries

---

## 🟢 4.2 Application Layer

### Component: `chat_service.py`

### Responsibilities:

* Orchestrate chat flow
* Build prompt
* Call LLM handler
* Save messages to DB
* Return final response to UI

### Flow:

```
User Input
   ↓
Build Prompt
   ↓
Call LLM
   ↓
Store user message
   ↓
Store assistant response
   ↓
Return response
```

This layer acts as the **central coordinator**.

---

## 🟡 4.3 Domain Layer

Contains core business logic modules.

---

### A. Authentication Module (`auth_handler.py`)

Responsibilities:

* Register user
* Hash password using Argon2
* Verify credentials
* Prevent duplicate users

Security:

* No plaintext storage
* Argon2 hashing
* No password length limitation

---

### B. Prompt Engineering Module (`prompt_manager.py`)

Responsibilities:

* Define system role
* Inject domain constraints
* Structure AI instructions
* Keep prompt reusable

Example Design:

```
System Prompt
  + User Input
  + Optional Memory Context
  = Final LLM Prompt
```

---

### C. Memory Module (`memory_manager.py`)

Responsibilities:

* Store messages persistently
* Retrieve chat history
* Maintain user-level isolation

Memory Type:

* Long-term (SQLite persistent)
* Short-term (Streamlit session)

---

## 🟣 4.4 Infrastructure Layer

Handles external integrations and low-level services.

---

### A. LLM Adapter Layer (`euriai_handler.py`)

Responsibilities:

* Initialize Euriai client
* Handle API requests
* Extract assistant content
* Log API errors
* Manage token parameters

Design Principle:

* Swappable LLM backend
* No UI logic
* No DB logic

You can replace Euriai with:

* Gemini
* OpenAI
* Anthropic
* Local LLM

Without touching UI or service layer.

---

### B. Database Layer (SQLite + SQLAlchemy)

Responsibilities:

* ORM-based model definitions
* Session management
* Persistent storage

Tables:

* users
* chat_history

Database can be upgraded to:

* PostgreSQL
* MySQL
* Cloud DB

Without changing business logic.

---

### C. Logging Module

Responsibilities:

* Log LLM errors
* Log system failures
* Write logs to file

Stored in:

```
logs/app.log
```

Improves observability and debugging.

---

# 5️⃣ Data Flow (End-to-End)

### Step-by-Step Runtime Flow

```
1. User logs in
2. User enters question
3. UI sends input to chat_service
4. chat_service builds prompt
5. euriai_handler sends request to LLM
6. LLM returns response
7. chat_service stores user + assistant message in DB
8. Response returned to UI
9. UI displays chat message
```

---

# 6️⃣ Security Architecture

### 🔐 Authentication

* Argon2 hashing
* No plaintext passwords

### 🔐 API Security

* API key stored in `.env`
* Loaded via dotenv
* Not committed to Git

### 🔐 Data Isolation

* Chat history linked via user_id
* No cross-user access

---

# 7️⃣ Scalability Considerations

Current:

* Single EC2
* SQLite

Upgradeable to:

* PostgreSQL
* Redis session store
* Docker containers
* Load balancer
* Background workers
* Token usage tracking

The architecture supports scaling without redesign.

---

# 8️⃣ Deployment Architecture

Deployed on AWS EC2:

```
Internet
  ↓
EC2 Instance
  ↓
Streamlit App (Port 8501)
  ↓
SQLite Database
  ↓
External Euriai API
```

Security group allows:

* Inbound: 8501
* Outbound: All

---

# 9️⃣ Design Principles Followed

✅ Separation of concerns
✅ Single responsibility principle
✅ Modular LLM abstraction
✅ Environment-based configuration
✅ ORM-based persistence
✅ Centralized error handling
✅ Production-grade password hashing

---

# 🔟 Risks & Mitigation

| Risk              | Mitigation           |
| ----------------- | -------------------- |
| LLM API failure   | Try/Except + Logging |
| Password breach   | Argon2 hashing       |
| API key exposure  | .env usage           |
| Model deprecation | Swappable LLM layer  |
| DB corruption     | ORM abstraction      |

---

# 1️⃣1️⃣ Future Architecture Roadmap

* Add JWT authentication
* Add token usage tracking per user
* Add Redis caching
* Add rate limiting
* Add vector database (RAG)
* Add Docker containerization
* Add CI/CD pipeline

---

# 🎓 Interview-Level Explanation (Short Version)

“This system follows a layered modular architecture.
The Streamlit UI handles presentation, the chat_service orchestrates business logic, the domain layer manages authentication, prompts, and memory, and the infrastructure layer integrates with the Euriai LLM and SQLite database.

Security is ensured via Argon2 hashing and environment-based API key management.
The LLM adapter layer allows model replacement without affecting other components.”

---
