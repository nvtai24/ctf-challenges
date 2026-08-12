from flask import Flask, request, render_template_string, abort
app = Flask(__name__)
import os

USERS = {
  "1": {"name": "Alice (Admin)", "bio": "System administrator.", "secret": True,  "flag": os.environ.get("FLAG", "CTF{placeholder}")},
  "2": {"name": "Bob",           "bio": "Sales team member.",    "secret": False, "flag": ""},
  "3": {"name": "Carol",         "bio": "Marketing lead.",       "secret": False, "flag": ""},
}

BASE = """<!DOCTYPE html><html><head><title>RobotsSecret</title>
<style>body{font-family:Arial,sans-serif;background:#f5f5f5;padding:32px;max-width:800px;margin:auto}
h1{color:#333}.card{background:#fff;border-radius:8px;padding:20px;margin:12px 0;box-shadow:0 1px 4px rgba(0,0,0,.1)}
a{color:#1a73e8;text-decoration:none}.flag{color:green;font-weight:bold;font-size:18px}
.hint{background:#fff3cd;border:1px solid #ffc107;padding:10px;border-radius:4px;font-size:13px}</style>
</head><body>"""

@app.route("/")
def index():
    return BASE + """<h1>👥 Staff Directory</h1>
    <div class="hint">💡 Hint: Websites often hide pages in <code>robots.txt</code>.</div>
    <div class="card">Browse our public staff profiles: 
    <a href="/user/2">Bob</a> | <a href="/user/3">Carol</a></div>
    </body></html>"""

@app.route("/robots.txt")
def robots():
    # Leaks hidden admin path
    return "User-agent: *\nDisallow: /admin-panel\nDisallow: /user/1\nDisallow: /backup/\n", 200, {"Content-Type": "text/plain"}

@app.route("/user/<uid>")
def user(uid):
    u = USERS.get(uid)
    if not u: abort(404)
    flag_html = f'<p class="flag">🚩 {u["flag"]}</p>' if u["secret"] else ""
    return BASE + f"""<h1>{u['name']}</h1>
    <div class="card"><p>{u['bio']}</p>{flag_html}</div>
    <a href="/">← Back</a></body></html>"""

@app.route("/admin-panel")
def admin_panel():
    return BASE + """<h1>🔒 Admin Panel</h1>
    <div class="card">Access restricted. Check individual user profiles for sensitive info.</div>
    <a href="/">← Back</a></body></html>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
