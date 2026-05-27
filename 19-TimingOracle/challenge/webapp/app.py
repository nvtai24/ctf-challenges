from flask import Flask, request, render_template_string
import time, os

app = Flask(__name__)

# Secret API key - players must extract char by char via timing
SECRET_KEY = "deadbeef42"
FLAG = "FCTF{t1m1ng_4tt4ck_p4t13nc3}"

TMPL = """<!DOCTYPE html><html><head><title>TimingOracle</title>
<style>body{font-family:monospace;background:#0d0d0d;color:#00ff41;padding:32px;max-width:900px;margin:auto}
h1{color:#00ff41}input{background:#000;color:#00ff41;border:1px solid #00ff41;padding:10px;width:300px;border-radius:4px;font-family:monospace}
button{padding:10px 24px;background:#00ff41;color:#000;border:none;border-radius:4px;cursor:pointer;font-weight:bold;font-family:monospace}
.res{border:1px solid #00ff41;padding:16px;margin:16px 0;border-radius:4px}
.hint{color:#007a1f;font-size:13px}.flag{color:#00ff41;font-size:18px;font-weight:bold}
pre{margin:0}</style></head>
<body>
<h1>⏱ TimingOracle API</h1>
<p class="hint">This API validates a 10-character hex key. Correct prefix = longer response time.</p>
<p class="hint">Method: Compare response time when submitting different first characters. The correct one takes ~50ms longer per correct char.</p>
<form method="POST">
  <input name="key" value="{{ key }}" placeholder="Enter API key (10 hex chars)"><br><br>
  <button>Validate Key</button>
</form>
{% if result is not none %}
<div class="res">
  <pre>Status  : {{ result.status }}</pre>
  <pre>Time    : {{ result.elapsed }}ms</pre>
  {% if result.flag %}<p class="flag">🚩 {{ result.flag }}</p>{% endif %}
</div>
{% endif %}
<p class="hint">
Tip: Send many requests and measure timing differences.<br>
Example with curl:<br>
<code>for c in 0 1 2 3 4 5 6 7 8 9 a b c d e f; do
  time curl -s -X POST -d "key=${c}000000000" http://target/
done</code>
</p>
</body></html>"""

def vulnerable_compare(a, b):
    """VULNERABLE: early-exit comparison leaks timing info"""
    if len(a) != len(b):
        return False
    for ca, cb in zip(a, b):
        if ca != cb:
            return False
        time.sleep(0.05)  # 50ms per correct character
    return True

@app.route("/", methods=["GET","POST"])
def index():
    key = ""
    result = None
    if request.method == "POST":
        key = request.form.get("key","").strip()
        start = time.time()
        valid = vulnerable_compare(key, SECRET_KEY)
        elapsed = round((time.time() - start) * 1000, 1)
        result = {
            "status": "✅ VALID KEY" if valid else "❌ INVALID KEY",
            "elapsed": elapsed,
            "flag": FLAG if valid else ""
        }
    return render_template_string(TMPL, key=key, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
