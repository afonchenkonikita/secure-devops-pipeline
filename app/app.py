from flask import Flask, request, render_template_string, redirect
import sqlite3
import os
import subprocess

app = Flask(__name__)

# Hardcoded secret — Gitleaks should detect this
SECRET_KEY = "sk_live_abc123fakekey456notreal789demo000"
DB_PASSWORD = "admin123"

DATABASE = "users.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'guest', 'guest')")
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return """
    <h1>Vulnerable Test App</h1>
    <ul>
        <li><a href="/login">Login (SQL injection)</a></li>
        <li><a href="/search?q=test">Search (XSS)</a></li>
        <li><a href="/ping?host=127.0.0.1">Ping (command injection)</a></li>
    </ul>
    """


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        # SQL injection vulnerability — SAST should detect this
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        if user:
            return f"Welcome, {username}!"
        return "Invalid credentials"
    return """
    <form method="post">
        <input name="username" placeholder="Username">
        <input name="password" type="password" placeholder="Password">
        <button>Login</button>
    </form>
    """


@app.route("/search")
def search():
    query = request.args.get("q", "")
    # XSS vulnerability — DAST should detect this
    template = f"<h2>Search results for: {query}</h2>"
    return render_template_string(template)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # Command injection vulnerability — SAST should detect this
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return f"<pre>{result.decode()}</pre>"


if __name__ == "__main__":
    init_db()
    # Debug mode enabled in production — SAST should flag this
    app.run(host="0.0.0.0", port=5000, debug=True)