from flask import Flask, request, render_template_string
import sqlite3, os, time

app = Flask(__name__)
DB = "/tmp/blind.db"

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, visible INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, key TEXT, value TEXT)")
    cur.execute("DELETE FROM products"); cur.execute("DELETE FROM secrets")
    cur.executemany("INSERT INTO products VALUES (?,?,?,?)", [
        (1,"Laptop","Electronics",1),(2,"Phone","Electronics",1),(3,"Shirt","Clothing",1),(4,"Jeans","Clothing",1),
    ])
    cur.execute("INSERT INTO secrets VALUES (1,'flag','FCTF{bl1nd_sql1_1s_p4t13nt}')")
    con.commit(); con.close()

TMPL = """<!DOCTYPE html><html><head><title>BlindSearch</title>
<style>body{font-family:monospace;background:#0f0f0f;color:#33ff33;padding:32px;max-width:900px;margin:auto}
h1{color:#33ff33}input{background:#000;color:#33ff33;border:1px solid #33ff33;padding:8px;width:300px;border-radius:4px}
button{padding:8px 20px;background:#33ff33;color:#000;border:none;border-radius:4px;cursor:pointer;font-weight:bold}
.res{background:#111;border:1px solid #33ff33;padding:16px;margin:12px 0;border-radius:4px}
.hint{color:#1a7a1a;font-size:13px}.err{color:#ff3333}</style></head>
<body>
<h1>🔍 BlindSearch</h1>
<p class="hint">Search for products. There are also hidden secrets in the database...</p>
<p class="hint">Hint: The search returns only "Found" or "Not found" — try Boolean-based Blind SQLi!</p>
<form method="GET">
  <input name="q" value="{{ q }}" placeholder="Search products...">
  <button>Search</button>
</form>
<div class="res">
{% if q %}
  {% if found %}
    ✅ Products found matching "{{ q }}"
  {% else %}
    ❌ No products found
  {% endif %}
{% else %}
  Enter a search term above.
{% endif %}
</div>
<p class="hint">Example payloads to try:<br>
' OR '1'='1  → always true<br>
' OR (SELECT SUBSTR(value,1,1) FROM secrets WHERE key='flag')='F  → check first char<br>
</p>
</body></html>"""

@app.route("/")
def index():
    q = request.args.get("q", "")
    found = False
    if q:
        try:
            con = sqlite3.connect(DB)
            cur = con.cursor()
            # VULNERABLE: raw string injection, but only returns boolean result
            cur.execute(f"SELECT COUNT(*) FROM products WHERE name LIKE '%{q}%' AND visible=1")
            count = cur.fetchone()[0]
            found = count > 0
            con.close()
        except:
            found = False
    return render_template_string(TMPL, q=q, found=found)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
