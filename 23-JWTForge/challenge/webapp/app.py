import os
import json
import base64
import hmac
import hashlib
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{placeholder}")

# VULNERABLE: weak secret, brute-forceable with common wordlists
JWT_SECRET = "supersecret"


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def b64url_decode(s: str) -> bytes:
    s += "=" * (4 - len(s) % 4)
    return base64.urlsafe_b64decode(s)


def create_token(payload: dict) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    h = b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    p = b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{h}.{p}".encode()
    sig = hmac.new(JWT_SECRET.encode(), signing_input, hashlib.sha256).digest()
    return f"{h}.{p}.{b64url_encode(sig)}"


def verify_token(token: str):
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None, "Malformed token: expected 3 parts"
        header = json.loads(b64url_decode(parts[0]))
        payload = json.loads(b64url_decode(parts[1]))
        alg = header.get("alg", "")

        # VULNERABLE: accepts algorithm "none" — skips signature verification
        if alg == "none":
            return payload, None

        if alg == "HS256":
            signing_input = f"{parts[0]}.{parts[1]}".encode()
            expected = hmac.new(JWT_SECRET.encode(), signing_input, hashlib.sha256).digest()
            provided = b64url_decode(parts[2])
            if hmac.compare_digest(expected, provided):
                return payload, None
            return None, "Signature verification failed"

        return None, f"Unsupported algorithm: {alg}"
    except Exception as e:
        return None, f"Parse error: {e}"


INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>JWT Cafe</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Courier New', monospace;
      background: #1e1e2e; color: #cdd6f4;
      min-height: 100vh;
    }
    header {
      background: #313244; border-bottom: 2px solid #45475a;
      padding: 18px 40px; display: flex; align-items: center; gap: 14px;
    }
    header h1 { font-size: 22px; color: #cba6f7; }
    header p { font-size: 13px; color: #6c7086; }
    main { max-width: 820px; margin: 40px auto; padding: 0 20px; }
    .card {
      background: #313244; border: 1px solid #45475a;
      border-radius: 12px; padding: 24px; margin-bottom: 20px;
    }
    .card h3 { color: #cba6f7; margin-bottom: 14px; font-size: 15px; }
    .token-display {
      background: #1e1e2e; border: 1px solid #45475a; border-radius: 8px;
      padding: 14px; font-size: 13px; color: #a6e3a1;
      word-break: break-all; line-height: 1.6;
    }
    .token-part-header { color: #89b4fa; }
    .token-part-payload { color: #fab387; }
    .token-part-sig { color: #a6e3a1; }
    label { display: block; font-size: 12px; color: #6c7086; margin-bottom: 8px; margin-top: 16px; }
    input[type=text] {
      width: 100%; padding: 11px 14px;
      background: #1e1e2e; color: #cdd6f4;
      border: 1px solid #45475a; border-radius: 8px;
      font-family: 'Courier New', monospace; font-size: 13px;
    }
    input:focus { outline: none; border-color: #cba6f7; }
    button {
      margin-top: 14px; padding: 10px 24px;
      background: #cba6f7; color: #1e1e2e; border: none;
      border-radius: 8px; font-size: 14px; font-weight: 700;
      cursor: pointer; font-family: 'Courier New', monospace;
    }
    button:hover { background: #b4befe; }
    #result { margin-top: 16px; padding: 14px; border-radius: 8px; font-size: 14px; display: none; }
    .result-ok  { background: rgba(166,227,161,0.1); border: 1px solid #a6e3a1; color: #a6e3a1; }
    .result-err { background: rgba(243,139,168,0.1); border: 1px solid #f38ba8; color: #f38ba8; }
    .hint {
      background: rgba(203,166,247,0.07); border: 1px solid rgba(203,166,247,0.2);
      border-radius: 8px; padding: 16px 20px; font-size: 13px; color: #6c7086; line-height: 1.7;
    }
    .hint code { background: #45475a; padding: 2px 6px; border-radius: 4px; color: #cba6f7; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    td { padding: 8px 12px; border-bottom: 1px solid #45475a; }
    td:first-child { color: #6c7086; width: 120px; }
    td:last-child { color: #cdd6f4; }
    .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }
    .dot-green { background: #a6e3a1; }
    .dot-blue  { background: #89b4fa; }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>&#9749; JWT Cafe</h1>
      <p>Stateless authentication service</p>
    </div>
  </header>
  <main>
    <div class="card">
      <h3>&#128272; Your Access Token</h3>
      <p style="font-size:13px;color:#6c7086;margin-bottom:14px">You are authenticated as a <strong style="color:#89b4fa">guest</strong> user. The flag is only accessible to <strong style="color:#a6e3a1">admin</strong>.</p>
      <div class="token-display" id="rawToken">{{ token }}</div>
      <div style="margin-top:14px">
        <table>
          <tr><td>Algorithm</td><td><span class="dot dot-blue"></span>HS256</td></tr>
          <tr><td>Subject</td><td>guest</td></tr>
          <tr><td>Role</td><td><span style="color:#89b4fa">user</span></td></tr>
        </table>
      </div>
    </div>

    <div class="card">
      <h3>&#127937; Get Flag</h3>
      <p style="font-size:13px;color:#6c7086;margin-bottom:4px">
        Endpoint: <code style="background:#1e1e2e;padding:2px 8px;border-radius:4px;color:#cba6f7">GET /flag</code>
        &nbsp;Header: <code style="background:#1e1e2e;padding:2px 8px;border-radius:4px;color:#cba6f7">Authorization: Bearer &lt;token&gt;</code>
      </p>
      <label>Token</label>
      <input type="text" id="tokenInput" value="{{ token }}">
      <button onclick="sendFlag()">&#8594; Send Request</button>
      <div id="result"></div>
    </div>

    <div class="hint">
      &#128161; <strong>Challenge:</strong> The server validates your JWT and checks the <code>role</code> claim.
      Only tokens with <code>role: "admin"</code> unlock the flag.
      Can you craft a valid admin token without knowing the secret?
      <br><br>
      <strong>Hint:</strong> Some JWT libraries have historically trusted the algorithm specified in the token header...
    </div>
  </main>
  <script>
    async function sendFlag() {
      const token = document.getElementById('tokenInput').value.trim();
      const res = await fetch('/flag', {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      const data = await res.json();
      const div = document.getElementById('result');
      div.style.display = 'block';
      if (data.flag) {
        div.className = 'result-ok';
        div.innerHTML = '&#127881; ' + data.flag;
      } else {
        div.className = 'result-err';
        div.innerHTML = '&#10060; ' + (data.error || 'Unknown error');
        if (data.role) div.innerHTML += ' (your role: ' + data.role + ')';
      }
    }
  </script>
</body>
</html>"""


@app.route("/")
def index():
    token = create_token({"sub": "guest", "role": "user", "iat": 1700000000})
    return render_template_string(INDEX_HTML, token=token)


@app.route("/flag")
def get_flag():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "Missing Authorization header"})

    token = auth[7:].strip()
    payload, err = verify_token(token)

    if err:
        return jsonify({"error": err})

    if payload.get("role") == "admin":
        return jsonify({"flag": FLAG, "message": "Welcome, admin!"})

    return jsonify({
        "error": "Access denied — admin only",
        "role": payload.get("role", "unknown"),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
