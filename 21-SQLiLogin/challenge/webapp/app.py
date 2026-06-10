import os
import sqlite3
from flask import Flask, request, render_template_string, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "ctf-flask-session-key-2024"
FLAG = os.environ.get("FLAG", "CTF{placeholder}")


def init_db():
    conn = sqlite3.connect("/tmp/users.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)""")
    c.execute("DELETE FROM users")
    c.execute("INSERT INTO users VALUES (1, 'admin', 'V3ryS3cr3tP4$$w0rd!', 'admin')")
    c.execute("INSERT INTO users VALUES (2, 'alice', 'alice1234', 'user')")
    c.execute("INSERT INTO users VALUES (3, 'bob', 'ilovebob', 'user')")
    conn.commit()
    conn.close()


init_db()

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>SecureLogin Corp</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', sans-serif;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      min-height: 100vh; display: flex; justify-content: center; align-items: center;
    }
    .card {
      background: rgba(255,255,255,0.05); backdrop-filter: blur(10px);
      border: 1px solid rgba(255,255,255,0.1);
      padding: 48px 40px; border-radius: 16px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.4); width: 380px;
    }
    .logo { text-align: center; margin-bottom: 32px; }
    .logo h1 { color: #e94560; font-size: 24px; letter-spacing: 2px; }
    .logo p { color: #888; font-size: 13px; margin-top: 6px; }
    label { display: block; color: #aaa; font-size: 13px; margin-bottom: 6px; margin-top: 18px; }
    input[type=text], input[type=password] {
      width: 100%; padding: 12px 16px;
      background: rgba(255,255,255,0.07); color: #eee;
      border: 1px solid rgba(255,255,255,0.15); border-radius: 8px;
      font-size: 14px; transition: border-color 0.2s;
    }
    input:focus { outline: none; border-color: #e94560; }
    button {
      width: 100%; margin-top: 28px; padding: 13px;
      background: #e94560; color: white; border: none;
      border-radius: 8px; font-size: 15px; font-weight: 600;
      cursor: pointer; letter-spacing: 0.5px; transition: background 0.2s;
    }
    button:hover { background: #c73652; }
    .error {
      color: #ff6b6b; background: rgba(255,107,107,0.1);
      border: 1px solid rgba(255,107,107,0.3);
      padding: 10px 14px; border-radius: 8px;
      font-size: 13px; margin-top: 18px; text-align: center;
    }
    .hint {
      color: #555; font-size: 12px; text-align: center;
      margin-top: 24px; line-height: 1.6;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">
      <h1>&#128274; SECURE<span style="color:#eee">LOGIN</span></h1>
      <p>Enterprise Authentication Portal</p>
    </div>
    <form method="POST" action="/login">
      <label>Username</label>
      <input type="text" name="username" placeholder="Enter your username" autocomplete="off">
      <label>Password</label>
      <input type="password" name="password" placeholder="Enter your password">
      <button type="submit">Sign In</button>
    </form>
    {% if error %}
    <div class="error">&#10007; {{ error }}</div>
    {% endif %}
    <p class="hint">&#128161; Registered users: alice, bob<br>There&apos;s also an admin account with the real prize...</p>
  </div>
</body>
</html>"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dashboard — SecureLogin</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', sans-serif;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      min-height: 100vh; display: flex; justify-content: center; align-items: center;
    }
    .card {
      background: rgba(255,255,255,0.05); backdrop-filter: blur(10px);
      border: 1px solid rgba(255,255,255,0.1);
      padding: 40px; border-radius: 16px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.4); width: 520px;
    }
    h2 { color: #eee; margin-bottom: 8px; }
    .badge {
      display: inline-block; padding: 3px 12px; border-radius: 20px;
      font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;
    }
    .admin-badge { background: #e94560; color: white; }
    .user-badge  { background: #0f3460; color: #89b4fa; border: 1px solid #89b4fa; }
    .flag-box {
      background: rgba(78,204,163,0.1); border: 2px solid #4ecca3;
      border-radius: 10px; padding: 20px; margin: 24px 0;
      text-align: center;
    }
    .flag-box p { color: #aaa; font-size: 13px; margin-bottom: 10px; }
    .flag-box code { color: #4ecca3; font-size: 18px; font-weight: bold; word-break: break-all; }
    .no-flag { color: #888; margin: 24px 0; padding: 16px; background: rgba(255,255,255,0.03); border-radius: 8px; }
    a { color: #888; font-size: 13px; text-decoration: none; }
    a:hover { color: #eee; }
    .divider { border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 24px 0; }
  </style>
</head>
<body>
  <div class="card">
    <h2>Welcome, {{ username }}!</h2>
    <p style="margin-top:8px">
      <span class="badge {% if role == 'admin' %}admin-badge{% else %}user-badge{% endif %}">{{ role }}</span>
    </p>
    {% if flag %}
    <div class="flag-box">
      <p>&#127881; Congratulations! You bypassed authentication as admin.</p>
      <code>{{ flag }}</code>
    </div>
    {% else %}
    <div class="no-flag">
      &#128274; You are logged in as a regular user.<br>
      Only the <strong>admin</strong> account holds the flag.
    </div>
    {% endif %}
    <hr class="divider">
    <a href="/logout">&#8592; Logout</a>
  </div>
</body>
</html>"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(INDEX_HTML, error=None)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = sqlite3.connect("/tmp/users.db")
    c = conn.cursor()
    # VULNERABLE: direct string interpolation — classic SQL injection
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    try:
        c.execute(query)
        user = c.fetchone()
    except Exception as e:
        conn.close()
        return render_template_string(INDEX_HTML, error=f"Database error: {e}")
    conn.close()

    if user:
        session["username"] = user[1]
        session["role"] = user[3]
        return redirect(url_for("dashboard"))

    return render_template_string(INDEX_HTML, error="Invalid username or password")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("index"))
    flag = FLAG if session.get("role") == "admin" else None
    return render_template_string(
        DASHBOARD_HTML,
        username=session["username"],
        role=session["role"],
        flag=flag,
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
