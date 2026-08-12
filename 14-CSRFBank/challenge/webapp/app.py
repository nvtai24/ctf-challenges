from flask import Flask, request, render_template_string, session, redirect
import os

app = Flask(__name__)
app.secret_key = "csrfbank-ctf-secret"

accounts = {
    "alice": {"password": "alice123", "balance": 10000, "flag": os.environ.get("FLAG", "CTF{placeholder}")},
    "bob":   {"password": "bob123",   "balance": 500,   "flag": ""},
}
transfer_log = []

STYLE = """<style>body{font-family:monospace;background:#0a2342;color:#e8eaf6;padding:32px;max-width:800px;margin:auto}
h1{color:#90caf9}.card{background:#0d47a1;border-radius:8px;padding:20px;margin:12px 0}
input{padding:8px;background:#1565c0;border:1px solid #42a5f5;color:#fff;border-radius:4px;margin:4px;width:200px}
button{padding:10px 24px;background:#42a5f5;color:#0a2342;border:none;border-radius:4px;cursor:pointer;font-weight:bold}
a{color:#90caf9}.flag{color:#69f0ae;font-size:18px;font-weight:bold}
.err{color:#ef5350}.ok{color:#69f0ae}
table{width:100%;border-collapse:collapse}td,th{padding:8px;border-bottom:1px solid #1565c0}th{color:#90caf9}</style>"""

@app.route("/")
def index():
    if "user" in session:
        return redirect("/dashboard")
    return render_template_string(f"""<!DOCTYPE html><html><head><title>CSRFBank</title>{STYLE}</head><body>
    <h1>🏦 CSRFBank</h1>
    <div class="card"><p>Login to your account.</p>
    <form method="POST" action="/login">
      <input name="username" placeholder="Username"><br>
      <input name="password" type="password" placeholder="Password"><br><br>
      <button>Login</button>
    </form>
    <p style="color:#555">Credentials: bob / bob123</p></div></body></html>""")

@app.route("/login", methods=["POST"])
def login():
    u, p = request.form.get("username"), request.form.get("password")
    if u in accounts and accounts[u]["password"] == p:
        session["user"] = u
        return redirect("/dashboard")
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if "user" not in session: return redirect("/")
    u = session["user"]
    acc = accounts[u]
    logs = "".join(f"<tr><td>{l['from']}</td><td>{l['to']}</td><td>${l['amount']}</td></tr>" for l in transfer_log[-5:])
    flag_html = f'<p class="flag">🚩 {acc["flag"]}</p>' if acc["balance"] >= 9000 and acc["flag"] else ""
    hint = "" if acc["flag"] else '<p style="color:#555;font-size:13px">Hint: Alice has lots of money. Can you trick Alice\'s browser into sending a transfer to Bob?</p>'
    return render_template_string(f"""<!DOCTYPE html><html><head><title>Dashboard</title>{STYLE}</head><body>
    <h1>🏦 CSRFBank</h1>
    <div class="card"><p>Welcome, <b>{u}</b> | Balance: <b>${acc['balance']}</b></p>
    {flag_html}{hint}
    <h3>Transfer Money</h3>
    <!-- VULNERABLE: No CSRF token -->
    <form method="POST" action="/transfer">
      To: <input name="to" placeholder="Username"><br>
      Amount: <input name="amount" type="number" placeholder="Amount"><br><br>
      <button>Transfer</button>
    </form></div>
    <div class="card"><h3>Recent Transfers</h3>
    <table><tr><th>From</th><th>To</th><th>Amount</th></tr>{logs}</table></div>
    <a href="/logout">Logout</a></body></html>""")

# VULNERABLE: No CSRF token, no Referer check, accepts cross-origin POST
@app.route("/transfer", methods=["POST"])
def transfer():
    if "user" not in session: return redirect("/")
    frm = session["user"]
    to  = request.form.get("to","")
    try: amount = int(request.form.get("amount", 0))
    except: amount = 0
    msg = ""
    if to not in accounts:
        msg = "❌ Recipient not found"
    elif amount <= 0:
        msg = "❌ Invalid amount"
    elif accounts[frm]["balance"] < amount:
        msg = "❌ Insufficient funds"
    else:
        accounts[frm]["balance"] -= amount
        accounts[to]["balance"]  += amount
        transfer_log.append({"from": frm, "to": to, "amount": amount})
        msg = f"✅ Transferred ${amount} to {to}"
    return render_template_string(f"""<!DOCTYPE html><html><head><title>Transfer</title>{STYLE}</head><body>
    <h1>🏦 CSRFBank</h1><div class="card"><p>{msg}</p><a href="/dashboard">← Back</a></div></body></html>""")

# Simulated "Alice visits this page" endpoint - for demo
@app.route("/alice-visits")
def alice_visits():
    """Simulate admin/alice visiting a malicious page that auto-submits a form"""
    session["user"] = "alice"  # simulate alice's session
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear(); return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
