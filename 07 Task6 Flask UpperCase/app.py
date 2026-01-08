from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title> Innomatics Research Labs</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
:root {
    --bg-dark: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    --bg-light: linear-gradient(135deg, #fdfbfb, #ebedee);
    --card-dark: rgba(255,255,255,0.14);
    --card-light: rgba(0,0,0,0.07);
    --text-dark: #ffffff;
    --text-light: #1e1e1e;
}

* {
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
}

body {
    margin: 0;
    min-height: 100vh;
    background: var(--bg-dark);
    transition: 0.4s;
}

body.light {
    background: var(--bg-light);
}

.container {
    min-height: 100vh;
    display: grid;
    place-items: center;
    padding: 20px;
}

.card {
    width: min(92vw, 1100px);   /* 🔥 Ultra-wide capable */
    background: var(--card-dark);
    backdrop-filter: blur(18px);
    padding: 32px;
    border-radius: 24px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.35);
    color: var(--text-dark);

    display: grid;
    grid-template-columns: 1fr;
    gap: 18px;
}

body.light .card {
    background: var(--card-light);
    color: var(--text-light);
}

h1 {
    font-size: clamp(2.2rem, 4vw, 3.2rem);
    text-align: center;
    background: linear-gradient(90deg, #00f260, #0575e6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    opacity: 0.85;
}

input {
    width: 100%;
    padding: 16px;
    border-radius: 14px;
    border: none;
    outline: none;
    font-size: 1.05rem;
    background: rgba(0,0,0,0.35);
    color: white;
}

body.light input {
    background: rgba(255,255,255,0.85);
    color: #222;
}

button {
    padding: 16px;
    border-radius: 14px;
    border: none;
    font-weight: bold;
    cursor: pointer;
    background: linear-gradient(90deg, #00f260, #0575e6);
}

.result {
    text-align: center;
    padding: 22px;
    border-radius: 18px;
    background: rgba(0,0,0,0.45);
    box-shadow: 0 0 22px rgba(0,242,96,0.45);

    /* 🔥 AUTO FONT SCALING (NO WRAP) */
    font-size: clamp(1.6rem, 3.2vw, 2.6rem);
    font-weight: 800;
    white-space: nowrap;
}

.controls {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
}

footer {
    text-align: center;
    font-size: 0.85rem;
    opacity: 0.65;
    margin-top: 10px;
}

.toggle {
    position: fixed;
    top: 18px;
    right: 22px;
    font-size: 1.5rem;
    cursor: pointer;
}
</style>
</head>

<body>

<div class="toggle" onclick="toggleTheme()">🌗</div>

<div class="container">
    <div class="card">

        <h1>Innomatics Research Labs 🤖</h1>
        <div class="subtitle">Enter your name & see magic</div>

        <form method="GET">
            <input name="name" placeholder="Type your name..." required>
            <button type="submit">Convert</button>
        </form>

        {% if name %}
        <div class="result" id="result">{{ name }}</div>

        <div class="controls">
            <button onclick="speak()">🔊 Speak</button>
            <button onclick="copyText()">📋 Copy</button>
        </div>
        {% endif %}

        <footer>
            © 2026 • Flask UI • Crafted by MWASIQ ✨
        </footer>

    </div>
</div>

<script>
function toggleTheme() {
    document.body.classList.toggle("light");
}

function speak() {
    let raw = document.getElementById("result").innerText;
    let clean = raw.replace(/[^\w\s]/gi, '');
    let utter = new SpeechSynthesisUtterance(clean);
    utter.rate = 0.9;
    speechSynthesis.cancel();
    speechSynthesis.speak(utter);
}

function copyText() {
    navigator.clipboard.writeText(
        document.getElementById("result").innerText
    );
    alert("Copied!");
}
</script>

</body>
</html>
"""

def ai_style_name(name: str) -> str:
    name = " ".join(name.split()).upper()
    if len(name) <= 6:
        return f"✨ {name} ✨"
    elif len(name) <= 12:
        return f"🔥 {name} 🔥"
    else:
        return f"👑 {name} 👑"

@app.route("/")
def home():
    name = request.args.get("name")
    styled = ai_style_name(name) if name else None
    return render_template_string(HTML, name=styled)

if __name__ == "__main__":
    app.run(debug=True)
