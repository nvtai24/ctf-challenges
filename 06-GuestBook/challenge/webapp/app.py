from flask import Flask, request, Response
import html as html_lib
import os

app = Flask(__name__)

FLAG = os.environ.get("FLAG", "CTF{placeholder}")
POSTS = [
    {"author": "Alice", "msg": "Great website!"},
    {"author": "Bob",   "msg": "Hello everyone :)"},
]

STYLE = """<style>
body{font-family:Arial,sans-serif;background:#fff8e7;padding:32px;max-width:800px;margin:auto}
h1{color:#d4540a}
.post{background:#fff;border-left:4px solid #d4540a;padding:12px 16px;margin:10px 0;border-radius:4px;box-shadow:0 1px 3px rgba(0,0,0,.1)}
.author{font-weight:bold;color:#d4540a}.msg{color:#333;margin-top:4px}
input[type=text]{width:200px;padding:8px;border:1px solid #ccc;border-radius:4px;margin:4px}
textarea{width:100%;height:80px;padding:8px;border:1px solid #ccc;border-radius:4px;box-sizing:border-box}
button{padding:8px 20px;background:#d4540a;color:#fff;border:none;border-radius:4px;cursor:pointer}
.secret{background:#fff3cd;border:1px solid #ffc107;padding:12px;border-radius:4px;margin:12px 0;font-family:monospace}
.hint{color:#888;font-size:13px}</style>"""

def render_page(search="", search_result=None, extra=""):
    posts_html = ""
    for p in POSTS:
        posts_html += f'<div class="post"><div class="author">{html_lib.escape(p["author"])}</div><div class="msg">{html_lib.escape(p["msg"])}</div></div>'
    # VULNERABLE: search term reflected without escaping
    search_display = f'<p>Search results for: <b>{search}</b></p>' if search else ""
    return f"""<!DOCTYPE html><html><head><title>GuestBook</title>{STYLE}
<script>
// Admin bot reads all cookies for monitoring (simulated)
document.cookie = "admin_flag={FLAG}; path=/";
</script>
</head><body>
<h1>📖 GuestBook</h1>
<p class="hint">Hint: The admin bot visits flagged posts. Steal the admin's cookie!</p>
<div class="secret">Your task: Perform XSS to steal the <b>admin_flag</b> cookie.</div>
{extra}
<h3>Search posts</h3>
<form method="GET" action="/search">
  <input name="q" value="{html_lib.escape(search)}" placeholder="Search...">
  <button type="submit">Search</button>
</form>
{search_display}
<h3>Leave a message</h3>
<form method="POST" action="/post">
  Name: <input name="author"><br><br>
  Message:<br><textarea name="msg"></textarea><br>
  <button type="submit">Post</button>
</form>
<h3>Recent posts</h3>
{posts_html}
</body></html>"""

@app.route("/")
def index():
    return Response(render_page(), content_type="text/html")

@app.route("/search")
def search():
    q = request.args.get("q","")
    # VULNERABLE: q injected directly into HTML
    search_display = f'<p>Search results for: <b>{q}</b></p>'
    posts_html = ""
    for p in POSTS:
        if q.lower() in p["author"].lower() or q.lower() in p["msg"].lower():
            posts_html += f'<div class="post"><div class="author">{html_lib.escape(p["author"])}</div><div class="msg">{html_lib.escape(p["msg"])}</div></div>'
    body = render_page(search=q).replace(f'<p>Search results for: <b>{html_lib.escape(q)}</b></p>', search_display)
    return Response(body, content_type="text/html")

@app.route("/post", methods=["POST"])
def post():
    author = request.form.get("author","Anonymous")
    msg    = request.form.get("msg","")
    POSTS.append({"author": author, "msg": msg})
    return Response(render_page(extra='<p style="color:green">✅ Posted!</p>'), content_type="text/html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
