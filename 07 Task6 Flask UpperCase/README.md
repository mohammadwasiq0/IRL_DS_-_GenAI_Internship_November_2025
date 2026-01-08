# 🤖 Name Styler – Flask Application

A modern, responsive **Flask web application** that takes a user’s name (via UI or URL query parameter), converts it to **UPPERCASE**, applies **Styling**, and displays it using a **premium, ultra-wide, grid-based UI**.

The app is designed with **mobile-first principles**, **auto font scaling**, **dark/light theme toggle**, and **text-to-speech support**.

---

## 🚀 Features

### 🔤 Core Functionality
- Accepts name via:
  - Input form
  - URL query parameter (`?name=`)
- Converts name to **UPPERCASE**
- Applies **Styling** using smart rules:
  - ✨ Short names
  - 🔥 Medium names
  - 👑 Long names

### 🎨 UI / UX
- 🌈 Animated input form
- 🎨 Dark / Light theme toggle
- 📱 Mobile-first design
- 🖥 Ultra-wide desktop layout
- 🧩 Grid-based responsive card layout
- 🔠 **Auto font scaling** (no forced wrapping)
- 🪟 Glassmorphism UI with soft shadows

### 🔊 Accessibility
- Text-to-speech (speaks name only, no emojis)
- Copy-to-clipboard button

---

## 🖼 Preview

- Responsive card that **expands on large screens**
- Font automatically scales instead of wrapping
- Clean, professional UI suitable for portfolios

---

## 🔗 Example Usage

### From Browser UI
1. Open the app
2. Enter your name
3. Click **Convert**

### Using Query Parameter
```

[http://127.0.0.1:5000/?name=Mohammad+Wasiq](http://127.0.0.1:5000/?name=Mohammad+Wasiq)

```

---

## 🛠 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (Grid, Clamp, Glassmorphism), Vanilla JavaScript
- **Speech**: Web Speech API (Browser-based)

---

## 📂 Project Structure

```

.
├── app.py
└── README.md

````

> ✅ Single-file Flask application  
> ❌ No external CSS/JS libraries  
> ❌ No database required  

---

## ⚙️ Installation & Run

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/mohammadwasiq0/IRL_DS_-_GenAI_Internship_November_2025.git
cd irl_internship
```

### 2️⃣ Install Dependencies

```bash
pip install flask
```

### 3️⃣ Run the App

```bash
python app.py
```

### 4️⃣ Open in Browser

```
http://127.0.0.1:5000/
```

---

## 🧠 Styling Logic

```text
Name Length ≤ 6   → ✨ NAME ✨
Name Length ≤ 12  → 🔥 NAME 🔥
Name Length > 12  → 👑 NAME 👑
```

The styling is deterministic.

---

## ♿ Accessibility & UX Improvements

* Emojis are **removed before text-to-speech**
* Font scales automatically based on screen size
* No layout blinking or flickering
* Fully responsive across devices

---

**Crafted with ❤️ using Flask**