# 🔗 URL Shortener Web Application (Flask)

A **modern, feature-rich, production-ready URL Shortener** built using **Flask + ORM + Ultra-Advanced Frontend**.
This project is designed to demonstrate **backend engineering**, **database design**, and **premium frontend UX/UI**, similar in quality to enterprise-grade web applications.

---

## 🌟 Features Overview

### ✅ Core Functionality

* 🔗 Shorten long URLs instantly
* 💾 Persist URLs in database
* 🔁 Redirect short URL → original URL
* 📜 Full URL history tracking

### 🎨 Premium Frontend (Ultra-Advanced)

* 🎬 Smooth animated transitions
* 📱 Fully responsive (mobile-first)
* 🧠 Modern glassmorphism UI

### ⚙️ Advanced Capabilities

* 🧾 Custom short URLs (user-defined)
* 📚 Pagination for large history lists
* 📋 One-click copy to clipboard
* 🧪 URL validation before shortening

---

## 🏗️ Tech Stack

### Backend

* **Python**
* **Flask**
* **Flask-SQLAlchemy (ORM)**
* **SQLite** (can be upgraded to PostgreSQL/MySQL)

### Frontend

* **HTML5**
* **CSS3 (Custom Ultra-Advanced Styling)**
* **Bootstrap 5**
* **Vanilla JavaScript**
* **CSS Animations & Transitions**

---

## 📁 Project Structure

```
url_shortener/
│
├── app.py                 # Main Flask application
├── model.py               # Database models (ORM)
│
├── static/
│   └── style.css      # Ultra-advanced UI styling
│
├── templates/
│   ├── index.html         # Home page (shorten URL)
│   └── history.html       # History
│
└── README.md              # Project documentation
```

---

## 🔄 Application Workflow

### 🏠 Home Page

1. User enters a **long URL**
2. (Optional) User enters a **custom short code**
3. Click **“Shorten URL”**
4. App:

   * Validates the URL
   * Generates a short URL
   * Stores it in the database
5. Short URL appears with:

   * Copy button
   * Visual animation feedback

---

### 📜 History Page

* Displays:

  * Original URL
  * Short URL

---

### 🔁 Redirection & Analytics

* When a short URL is accessed:

  * Redirects to original URL
  * Increments click count in database

---

## 🧪 URL Validation

Before shortening:

* Checks if URL is:

  * Properly formatted
  * Has valid scheme (`http://` or `https://`)
* Prevents invalid or broken URLs

---

## ⚙️ Installation & Setup

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

### 5️⃣ Open Browser

```
http://127.0.0.1:5000/
```

---

## 🧠 Database Model (Conceptual)

```text
URL
├── id (Primary Key)
├── original_url
├── short_code
├── click_count
├── created_at
```

---

## 🌙 Dark / Light Mode

* Toggle persists across pages
* Uses CSS variables
* Smooth animated transitions
* System-friendly contrast ratios

---

## 🚀 Why This Project Is Special

✔ Production-ready architecture
✔ ORM-based clean database design
✔ Advanced UI beyond basic Bootstrap

---

## 🧩 Future Enhancements

* 🔐 User authentication
* 🕒 URL expiry
* 📈 Analytics dashboard
* 🌍 Custom domains
* ☁️ Cloud deployment (AWS / Render / Railway)

---