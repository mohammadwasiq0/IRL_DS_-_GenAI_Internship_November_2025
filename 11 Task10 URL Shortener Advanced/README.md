# 🔗 URL Shortener Web Application

**Secure • Scalable • SaaS-Grade**

A **production-ready URL Shortener Web Application** built using **Flask**, featuring **user authentication**, **dashboard analytics**, **URL history management**, and a **modern SaaS-style UI**.

---

## 📌 Table of Contents

* [Overview](#overview)
* [Key Features](#key-features)
* [Tech Stack](#tech-stack)
* [Application Workflow](#application-workflow)
* [High Level Design (HLD)](#high-level-design-hld)
* [Low Level Design (LLD)](#low-level-design-lld)
* [Database Schema](#database-schema)
* [Security Considerations](#security-considerations)
* [Project Structure](#project-structure)
* [Installation & Setup](#installation--setup)
* [Usage](#usage)
* [Future Enhancements](#future-enhancements)
* [Author](#author)

---

## 📖 Overview

The **URL Shortener Web Application** allows users to convert long URLs into short, shareable links.
Authenticated users can **manage**, **track**, and **reuse** previously shortened URLs through a **modern dashboard**.

The application is designed with:

* Clean MVC-style separation
* Scalable database design
* Secure authentication
* SaaS-grade UI/UX

---

## ✨ Key Features

### 🔐 Authentication

* User Signup & Login
* Session-based authentication
* Auth-aware navigation

### ✂️ URL Shortening

* Generate short URLs instantly
* Persistent storage
* Unique hash generation

### 📊 Dashboard

* URL creation form
* Stats cards (future-ready)
* Copy-to-clipboard UX

### 📁 URL Management

* View previously shortened URLs
* Open shortened links
* Copy & reuse URLs

### 🎨 UI/UX

* Glassmorphism design
* Dark SaaS theme
* Responsive layout
* Consistent design system

---

## 🧰 Tech Stack

### Backend

* **Python**
* **Flask**
* **SQLAlchemy ORM**
* **SQLite** (easily scalable to PostgreSQL)

### Frontend

* **HTML5**
* **CSS3 (Custom, No Bootstrap dependency)**
* **JavaScript (Vanilla)**

### Security

* Password hashing
* Session protection
* Input validation

---

## 🔄 Application Workflow

### 1️⃣ User Authentication Flow

```
User → Signup/Login → Session Created → Dashboard Access
```

### 2️⃣ URL Shortening Flow

```
User Inputs URL
        ↓
Backend Validates URL
        ↓
Short Code Generated
        ↓
Stored in Database
        ↓
Short URL Returned to User
```

### 3️⃣ Redirection Flow

```
Short URL Accessed
        ↓
Database Lookup
        ↓
Original URL Retrieved
        ↓
HTTP Redirect
```

### 4️⃣ URL History Flow

```
Dashboard → Fetch User URLs → Display in Table → Copy / Open
```

---

## 🏗️ High Level Design (HLD)

### System Architecture

```
┌─────────────┐
│   Browser   │
└─────┬───────┘
      │ HTTP Requests
┌─────▼───────┐
│   Flask App │
│ (Controllers)
└─────┬───────┘
      │ ORM Calls
┌─────▼───────┐
│ SQLAlchemy  │
└─────┬───────┘
      │ SQL Queries
┌─────▼───────┐
│   Database  │
│  (SQLite)   │
└─────────────┘
```

### Major Components

* **Presentation Layer** → HTML/CSS/JS
* **Application Layer** → Flask routes & logic
* **Persistence Layer** → SQLAlchemy ORM
* **Database Layer** → SQLite

---

## 🔍 Low Level Design (LLD)

### Key Modules

#### 1. Authentication Module

* `/signup`
* `/login`
* `/logout`
* Session management
* Password hashing

#### 2. URL Shortener Module

* URL validation
* Hash generation
* Collision handling
* Short URL creation

#### 3. Dashboard Module

* URL input form
* Display shortened URL
* Copy functionality

#### 4. URL History Module

* Fetch user-specific URLs
* Render table view
* Redirect handling

---

## 🗄️ Database Schema

### User Table

| Column     | Type     | Description |
| ---------- | -------- | ----------- |
| id         | Integer  | Primary Key |
| username   | String   | Unique      |
| password   | String   | Hashed      |
| created_at | DateTime | Timestamp   |

### URL Table

| Column       | Type     | Description |
| ------------ | -------- | ----------- |
| id           | Integer  | Primary Key |
| original_url | String   | Long URL    |
| short_code   | String   | Unique      |
| user_id      | Integer  | FK → User   |
| created_at   | DateTime | Timestamp   |

---

## 🔐 Security Considerations

* Password hashing (never stored in plain text)
* Session-based authentication
* URL input validation
* Protection against unauthorized access
* Ready for CSRF & rate-limiting extensions

---

## 📁 Project Structure

```
url-shortener/
│
├── app.py
├── models.py
├── database.py
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── signup.html
│   ├── dashboard.html
│   └── urls.html
│
├── static/
│   ├── css/
│   │   ├── base.css
│   │   ├── index.css
│   │   ├── signup.css
│   │   ├── dashboard.css
│   │   └── urls.css
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Application

```bash
python app.py
```

Access at:

```
http://127.0.0.1:5000
```

---

## ▶️ Usage

1. Sign up for an account
2. Login to dashboard
3. Enter long URL
4. Generate short URL
5. Copy & share
6. View previous URLs anytime

---

## 🚀 Future Enhancements

* 📈 Click analytics & charts
* 🌍 Custom domains
* ⏱️ URL expiry
* 🧑‍💼 Admin panel
* 📱 Mobile-first optimization
* 🌗 Dark/Light theme toggle
* 🛡️ Rate limiting & CAPTCHA