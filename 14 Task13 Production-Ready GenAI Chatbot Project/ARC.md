# 🏗 1️⃣ High-Level Architecture (ASCII Diagram)

```
                   ┌──────────────────────┐
                   │        User          │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │     Streamlit UI     │
                   │  - Chat Interface    │
                   │  - Login/Register    │
                   │  - Download History  │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │    Chat Service      │
                   │  (Business Logic)    │
                   └──────────┬───────────┘
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
     ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
     │ Prompt Engine│  │ Auth Handler │  │ Memory Layer │
     │ (System Role)│  │ (Argon2)     │  │ (SQLite)     │
     └──────────────┘  └──────────────┘  └──────────────┘
              │                                   │
              └───────────────┬───────────────────┘
                              ▼
                   ┌──────────────────────┐
                   │     LLM Handler      │
                   │   (Euriai Client)    │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │   Euriai LLM API     │
                   │   (gpt-4.1-nano)     │
                   └──────────────────────┘
```

---

# 🧠 2️⃣ Layered Clean Architecture Diagram

This shows proper separation of concerns.

```
┌─────────────────────────────────────────────┐
│                Presentation Layer           │
│---------------------------------------------│
│  Streamlit UI                              │
│  - Chat Input                              │
│  - Authentication UI                       │
│  - Chat History Display                    │
│  - Download CSV                            │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│                Application Layer            │
│---------------------------------------------│
│  chat_service.py                           │
│  - Orchestrates prompt + LLM + DB          │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│                 Domain Layer                │
│---------------------------------------------│
│  prompt_manager.py                         │
│  auth_handler.py                           │
│  memory_manager.py                         │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│             Infrastructure Layer            │
│---------------------------------------------│
│  euriai_handler.py                         │
│  database (SQLite + SQLAlchemy)            │
│  logger.py                                 │
│  .env configuration                        │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│            External Services Layer          │
│---------------------------------------------│
│  Euriai API (gpt-4.1-nano)                 │
└─────────────────────────────────────────────┘
```

---

# ☁️ 3️⃣ AWS EC2 Deployment Architecture

```
                   Internet
                       │
                       ▼
             ┌──────────────────┐
             │   AWS EC2        │
             │  Ubuntu Server   │
             └────────┬─────────┘
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
 ┌──────────────────┐      ┌──────────────────┐
 │  Streamlit App   │      │   SQLite DB      │
 │  (Port 8501)     │      │  chatbot.db      │
 └────────┬─────────┘      └──────────────────┘
          │
          ▼
 ┌──────────────────┐
 │ Euriai LLM API   │
 │ (External Cloud) │
 └──────────────────┘
```

Security Group:

* Allow inbound TCP 8501
* Outbound open (for LLM API calls)

---

# 🎨 4️⃣ Visual Diagram Layout (For draw.io / Lucidchart)

Use these blocks:

### Layer 1 (Top)

* User (Person Icon)

### Layer 2

* Streamlit Web App (Rounded rectangle)

### Layer 3 (Split into 3 components)

* Authentication Service
* Chat Service
* Memory Manager

### Layer 4

* Prompt Engineering Module
* LLM Handler (Euriai Client)

### Layer 5

* SQLite Database
* Euriai Cloud API

Connect arrows:

User
→ Streamlit
→ Chat Service
→ Prompt Module
→ LLM Handler
→ Euriai API
→ Response
→ Save to SQLite
→ Render in UI

---

# 🔥 Advanced (Professional Version Diagram)

If you want something that looks enterprise-level:

```
                ┌─────────────────────────┐
                │        End User         │
                └─────────────┬───────────┘
                              │ HTTPS
                              ▼
                ┌─────────────────────────┐
                │     Streamlit Frontend  │
                │     (Presentation)      │
                └─────────────┬───────────┘
                              │
                              ▼
                ┌─────────────────────────┐
                │     Application Core    │
                │  - Chat Orchestration   │
                │  - Business Rules       │
                └─────────────┬───────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌────────────────┐   ┌────────────────┐   ┌────────────────┐
│ Auth Module    │   │ Prompt Engine  │   │ Memory Manager │
│ (Argon2)       │   │ (System Role)  │   │ (SQLite ORM)   │
└────────────────┘   └────────────────┘   └────────────────┘
                              │
                              ▼
                ┌─────────────────────────┐
                │     LLM Adapter Layer   │
                │     (Euriai Client)     │
                └─────────────┬───────────┘
                              │ REST API
                              ▼
                ┌─────────────────────────┐
                │      Euriai Cloud LLM   │
                └─────────────────────────┘
```

---

