from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Regex Playground</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
:root {
    --bg-dark: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    --bg-light: linear-gradient(135deg, #fdfbfb, #ebedee);
    --card-dark: rgba(255,255,255,0.15);
    --card-light: rgba(0,0,0,0.08);
    --text-dark: white;
    --text-light: #222;
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
    width: min(96vw, 1300px);
    background: var(--card-dark);
    backdrop-filter: blur(18px);
    padding: 30px;
    border-radius: 24px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.35);
    color: var(--text-dark);
    display: grid;
    gap: 18px;
}

body.light .card {
    background: var(--card-light);
    color: var(--text-light);
}

h1 {
    text-align: center;
    font-size: clamp(2rem, 4vw, 3rem);
    background: linear-gradient(90deg, #00f260, #0575e6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

@media (max-width: 900px) {
    .grid {
        grid-template-columns: 1fr;
    }
}

textarea, input {
    width: 100%;
    padding: 14px;
    border-radius: 14px;
    border: none;
    outline: none;
    background: rgba(0,0,0,0.35);
    color: white;
    font-size: 1rem;
}

body.light textarea,
body.light input {
    background: rgba(255,255,255,0.85);
    color: #222;
}

.flags {
    display: flex;
    gap: 14px;
    justify-content: center;
}

.flags label {
    cursor: pointer;
    font-weight: bold;
}

.result-box {
    padding: 20px;
    border-radius: 18px;
    background: rgba(0,0,0,0.45);
}

.highlight {
    background: rgba(0,242,96,0.35);
    border-radius: 4px;
    padding: 2px 4px;
    font-weight: 600;
}

.group {
    color: #00f260;
}

.error {
    color: #ff6b6b;
    font-weight: bold;
}

.toggle {
    position: fixed;
    top: 18px;
    right: 22px;
    font-size: 1.5rem;
    cursor: pointer;
}

footer {
    text-align: center;
    font-size: 0.85rem;
    opacity: 0.65;
}
</style>
</head>

<body>

<div class="toggle" onclick="toggleTheme()">🌗</div>

<div class="container">
<div class="card">

<h1>Regex Playground 🔍</h1>

<div class="grid">
    <textarea id="testString" rows="10" placeholder="Enter test string..."></textarea>
    <input id="regexInput" placeholder="Enter regex pattern...">
</div>

<div class="flags">
    <label><input type="checkbox" value="i"> i (IGNORECASE)</label>
    <label><input type="checkbox" value="m"> m (MULTILINE)</label>
    <label><input type="checkbox" value="s"> s (DOTALL)</label>
</div>

<div id="output" class="result-box"></div>

<footer>
    © 2026 • Flask Regex Playground • Inspired by regex101
</footer>

</div>
</div>

<script>
function toggleTheme() {
    document.body.classList.toggle("light");
}

function getFlags() {
    return [...document.querySelectorAll(".flags input:checked")]
           .map(cb => cb.value).join("");
}

function escapeHTML(text) {
    return text.replace(/[&<>"']/g, m => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[m]);
}

function runRegex() {
    const text = document.getElementById("testString").value;
    const pattern = document.getElementById("regexInput").value;
    const flags = getFlags();

    const output = document.getElementById("output");

    if (!pattern) {
        output.innerHTML = "";
        return;
    }

    try {
        const regex = new RegExp(pattern, flags + "g");
        let match;
        let matches = [];
        let highlighted = escapeHTML(text);

        while ((match = regex.exec(text)) !== null) {
            matches.push(match);
        }

        // Inline highlighting
        highlighted = escapeHTML(text).replace(regex, m =>
            `<span class="highlight">${m}</span>`
        );

        let html = `<p><strong>Matches:</strong> ${matches.length}</p>`;
        html += `<div>${highlighted}</div><hr>`;

        matches.forEach((m, i) => {
            html += `<p><strong>Match ${i + 1}:</strong> ${m[0]}</p>`;
            for (let g = 1; g < m.length; g++) {
                html += `<p class="group">Group ${g}: ${m[g]}</p>`;
            }
        });

        output.innerHTML = html || "<p>No matches</p>";

    } catch (e) {
        output.innerHTML = `<p class="error">❌ ${e.message}</p>`;
    }
}

document.querySelectorAll("#testString, #regexInput, .flags input")
        .forEach(el => el.addEventListener("input", runRegex));
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
