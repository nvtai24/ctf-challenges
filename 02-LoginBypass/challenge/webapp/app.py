from flask import Flask, request, session, redirect, url_for, render_template_string
import sqlite3, os, hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)

DB = "/app/users.db"

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT, password TEXT, role TEXT, flag TEXT)""")
    cur.execute("DELETE FROM users")
    cur.executemany("INSERT INTO users VALUES (?,?,?,?,?)", [
        (1, "alice",   hashlib.md5(b"sup3rS3cr3t").hexdigest(), "admin", os.environ.get("FLAG", "CTF{placeholder}")),
        (2, "bob",     hashlib.md5(b"password123").hexdigest(), "user",  ""),
        (3, "charlie", hashlib.md5(b"qwerty").hexdigest(),      "user",  ""),
    ])
    con.commit(); con.close()

LOGIN_PAGE = """<!DOCTYPE html><html><head><title>Staff Login</title>
<style>body{font-family:monospace;background:#1a1a2e;color:#eee;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}
.box{background:#16213e;padding:40px;border-radius:8px;width:320px;box-shadow:0 0 20px rgba(0,150,255,.3)}
h2{color:#0f9;margin-bottom:24px}input{width:100%;padding:10px;margin:8px 0 16px;background:#0f3460;border:1px solid #0f9;color:#eee;border-radius:4px;box-sizing:border-box}
button{width:100%;padding:12px;background:#0f9;color:#000;border:none;border-radius:4px;cursor:pointer;font-weight:bold;font-size:15px}
.err{color:#f55;margin-top:12px}.hint{color:#888;font-size:12px;margin-top:16px}</style></head>
<body><div class="box"><h2>🔐 Staff Portal</h2>
<form method="POST">
<label>Username</label><input name="username" placeholder="username">
<label>Password</label><input name="password" type="password" placeholder="password">
<button type="submit">Login</button>
</form>
{% if error %}<div class="err">{{ error }}</div>{% endif %}
<div class="hint">Hint: Only admins can view the flag.</div>
</div></body></html>"""

FLAG_PAGE = """<!DOCTYPE html><html><head><title>Admin Panel</title>
<style>body{font-family:monospace;background:#1a1a2e;color:#eee;padding:40px}
.flag{background:#0f3460;border:2px solid #0f9;padding:20px;border-radius:8px;font-size:20px;color:#0f9;margin:20px 0}
a{color:#0f9}</style></head>
<body><h2>👑 Admin Panel</h2>
<p>Welcome, <b>{{ username }}</b>!</p>
<div class="flag">🚩 {{ flag }}</div>
<a href="/logout">Logout</a></body></html>"""

@app.route("/", methods=["GET","POST"])
def login():
    error = ""
    if request.method == "POST":
        u = request.form.get("username","")
        p = request.form.get("password","")
        # VULNERABLE: raw string concat
        query = f"SELECT * FROM users WHERE username='{u}' AND password='{hashlib.md5(p.encode()).hexdigest()}'"
        try:
            con = sqlite3.connect(DB)
            cur = con.cursor()
            cur.execute(query)
            row = cur.fetchone()
            con.close()
            if row:
                session["user"] = row[1]; session["role"] = row[3]; session["flag"] = row[4]
                return redirect("/dashboard")
            else:
                error = "Invalid credentials"
        except Exception as e:
            error = f"DB Error: {e}"
    return render_template_string(LOGIN_PAGE, error=error)

@app.route("/dashboard")
def dashboard():
    if "user" not in session: return redirect("/")
    if session.get("role") != "admin":
        return "<h3 style='color:red;font-family:monospace'>Access denied. Admins only.</h3><a href='/'>Back</a>"
    return render_template_string(FLAG_PAGE, username=session["user"], flag=session["flag"])

@app.route("/logout")
def logout():
    session.clear(); return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
