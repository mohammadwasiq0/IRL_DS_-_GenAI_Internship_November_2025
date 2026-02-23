# 🚀 Production-Ready GenAI Career Advisor Chatbot

## 📌 Project Title

**Building a Production-Ready Domain-Specific Chatbot using Euriai LLM API**

---

# 🧠 Project Overview

This project implements a **production-ready, domain-specific AI chatbot** built with:

* Streamlit (Interactive UI)
* Euriai LLM API (gpt-4.1-nano model)
* SQLite (Persistent storage)
* Argon2 (Secure authentication)
* Modular backend architecture
* Logging & error handling
* Long-term conversation memory
* Chat history export functionality

The chatbot is designed as a **Career Advisor AI**, capable of structured, contextual, and intelligent responses.

The system follows real-world AI engineering principles including:

* Clean architecture
* Secure API key handling
* Modular code separation
* Persistent memory
* Production-grade password hashing
* Deployment-ready configuration

---

# 🏗 System Architecture

```
User
  ↓
Streamlit UI
  ↓
Chat Service Layer
  ↓
Prompt Engineering Module
  ↓
LLM Handler (Euriai)
  ↓
Response Processing
  ↓
SQLite Database (Chat Memory)
  ↓
UI Rendering
```

---

# 🧩 High-Level Design (HLD)

## 1️⃣ Frontend Layer

* Built using Streamlit
* Chat-style interface
* Login/Register system
* Chat history display
* Chat history download (CSV)

## 2️⃣ Backend Layer

* Service-based architecture
* LLM abstraction layer
* Prompt management module
* Database layer (SQLAlchemy ORM)
* Authentication handler

## 3️⃣ LLM Integration

* EuriaiClient
* Model: `gpt-4.1-nano`
* Configurable temperature and token limits
* Error handling with logging

## 4️⃣ Database Layer

SQLite Database (`chatbot.db`)

Tables:

* `users`
* `chat_history`

## 5️⃣ Security Layer

* Argon2 password hashing
* Environment-based API key storage
* No hardcoded secrets
* Modular authentication logic

---

# 🏗 Low-Level Design (LLD)

## 📁 Project Structure

```
genai_chatbot/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
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
│
└── logs/
    └── app.log
```

---

# 🔐 Authentication Flow

1. User registers
2. Password hashed using Argon2
3. Stored in SQLite
4. Login verifies hash
5. Session stored in Streamlit session_state

Security Notes:

* Argon2 chosen for modern password security
* No 72-byte limitation (unlike bcrypt)
* Follows OWASP best practices

---

# 🧠 Memory Management

### Short-Term Memory

* Session-based in Streamlit

### Long-Term Memory

* Persistent storage in SQLite
* Chat history linked by `user_id`

Each message stored with:

* Role (user/assistant)
* Message content

---

# 🎯 Prompt Engineering Strategy

System prompt defines:

* Role: Career Advisor AI
* Structured output
* Practical advice
* No hallucinations
* Actionable roadmap

Prompts are modular and reusable via `prompt_manager.py`.

---

# ⚙️ LLM Integration

## Euriai Client Configuration

```python
client = EuriaiClient(
    api_key=Config.EURI_API_KEY,
    model="gpt-4.1-nano"
)
```

### Response Extraction

```python
response["choices"][0]["message"]["content"]
```

### Error Handling

* All errors logged in `logs/app.log`
* Graceful fallback messages returned

---

# 🗄 Database Schema

## Users Table

| Column   | Type                 |
| -------- | -------------------- |
| id       | Integer (PK)         |
| username | String (Unique)      |
| password | String (Argon2 hash) |

## Chat History Table

| Column  | Type         |
| ------- | ------------ |
| id      | Integer (PK) |
| user_id | Integer      |
| role    | String       |
| message | Text         |

---

# 🛠 Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone <repo_url>
cd genai_chatbot
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Setup Environment Variables

Create `.env`:

```
EURI_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///chatbot.db
SECRET_KEY=your_secret_key
```

## 5️⃣ Run Application

```bash
streamlit run app.py
```

---

# ☁️ AWS EC2 Deployment

## 1️⃣ Launch EC2 (Ubuntu)

## 2️⃣ Install Python & pip

```bash
sudo apt update
sudo apt install python3-pip
```

## 3️⃣ Clone Repository

## 4️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

## 5️⃣ Run Streamlit

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 6️⃣ Configure Security Group

Allow inbound port:

```
8501
```

Access:

```
http://<EC2_PUBLIC_IP>:8501
```

---

# 📊 Logging & Monitoring

All errors and system logs stored in:

```
logs/app.log
```

Logged Events:

* LLM errors
* API failures
* System exceptions

---

# 📥 Chat History Download

Users can download conversation history as CSV:

* Role
* Message
* Timestamp (if added later)

---

# 🔒 Security Considerations

* API keys stored in `.env`
* No credentials hardcoded
* Password hashing via Argon2
* Modular authentication logic
* Production-ready structure

---

# 🚀 Future Enhancements

* JWT authentication
* Redis session management
* PostgreSQL upgrade
* Token usage tracking per user
* Role-based access (Admin/User)
* Docker containerization
* CI/CD pipeline
* Vector database (RAG)
* Rate limiting

---

# 📈 Production Readiness Checklist

| Feature               | Status |
| --------------------- | ------ |
| Authentication        | ✅      |
| Secure Hashing        | ✅      |
| Environment Variables | ✅      |
| Modular Code          | ✅      |
| Error Handling        | ✅      |
| Logging               | ✅      |
| Persistent Memory     | ✅      |
| Download History      | ✅      |
| Cloud Deployable      | ✅      |

---

# 🎓 Interview Explanation Summary

This project demonstrates:

* End-to-end AI system design
* Clean architecture principles
* Secure authentication
* Persistent conversation memory
* LLM API integration
* Cloud deployment capability
* Production-grade error handling

---

# 👨‍💻 Tech Stack

* Python
* Streamlit
* Euriai LLM API
* SQLAlchemy
* SQLite
* Argon2
* dotenv

---