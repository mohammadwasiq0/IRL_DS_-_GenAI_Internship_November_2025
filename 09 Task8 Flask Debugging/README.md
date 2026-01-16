# 📝 Flask Notes Application

A simple, clean **Flask web application** that allows users to add notes via a text field and display them instantly as an **unordered list** on the same page.

This project focuses on **refactoring**, **bug fixing**, and **clear documentation**, as required in typical backend or full-stack coding assignments.

---

## 🎯 Objective

- Refactor an existing Flask application
- Fix functional bugs
- Ensure the app works correctly
- Document all identified bugs and their fixes

---

## ✅ Functional Requirements

- Home route `/`
- One **text input field**
- One **submit button**
- Users can add notes
- All notes are displayed below the input as an **unordered list**
- Notes persist during application runtime
- Page remains stable (no crashes, no duplicates)

---

## 🚀 Features

- Simple and intuitive UI
- Server-side note handling
- Input validation
- Clean Flask routing
- Uses **Post/Redirect/Get (PRG)** pattern
- Lightweight and dependency-free (only Flask)

---

## 🛠 Tech Stack

| Layer      | Technology |
|-----------|------------|
| Backend   | Flask (Python) |
| Frontend | HTML, CSS |
| Storage  | In-memory Python list |

---

## 📂 Project Structure

```
.
├── app.py
├── templates/
│   └── index.html
└── README.md

````

---

## ⚙️ Installation & Setup

### 2️⃣ Install Flask

```bash
pip install flask
```

### 3️⃣ Run the Application

```bash
python app.py
```

### 4️⃣ Open in Browser

```
http://127.0.0.1:5000/
```

---

## 🐞 Bug Report & Fix Documentation

### 🐛 Bug 1: Notes were not persisting

**Problem:**
Notes were being initialized inside the route, causing them to reset on every request.

**Fix:**
Moved the notes list to global scope:

```python
notes = []
```

---

### 🐛 Bug 2: Duplicate notes on page refresh

**Problem:**
Refreshing the page after submission re-added the same note.

**Fix:**
Implemented **Post/Redirect/Get (PRG)** pattern:

```python
return redirect(url_for("home"))
```

---

### 🐛 Bug 3: Empty notes allowed

**Problem:**
Users could submit empty or whitespace-only notes.

**Fix:**
Added input validation:

```python
if note and note.strip():
```

---

### 🐛 Bug 4: Incorrect form data handling

**Problem:**
Form data was incorrectly accessed using `request.args` for POST requests.

**Fix:**
Corrected to:

```python
request.form.get("note")
```

---

### 🐛 Bug 5: Notes not rendering in UI

**Problem:**
Notes were not passed to the template.

**Fix:**
Passed notes explicitly:

```python
return render_template("index.html", notes=notes)
```

---

## 🧠 How the Application Works

1. User enters a note in the text field
2. Clicks **Add Note**
3. Flask receives the POST request
4. Input is validated and stored in memory
5. User is redirected back to home page
6. Notes are displayed as an unordered list

---

## ⚠️ Limitations

* Notes are stored **in-memory** (lost on server restart)
* Single-user session only
* No database persistence

---

## 📈 Possible Enhancements

* Delete notes
* Edit notes
* Persist notes using SQLite
* Session-based storage
* AJAX-based submission (no page reload)
* User authentication
* REST API version

