from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
FLAG = "FCTF{sst1_t3mpl4t3_1nj3ct10n}"

BASE_TMPL = """<!DOCTYPE html><html><head><title>SSTINote</title>
<style>body{font-family:monospace;background:#1b1b2f;color:#e2e2e2;padding:32px;max-width:800px;margin:auto}
h1{color:#e94560}textarea{width:100%;height:100px;background:#162447;color:#e2e2e2;border:1px solid #e94560;border-radius:6px;padding:10px;font-family:monospace}
button{padding:10px 24px;background:#e94560;color:#fff;border:none;border-radius:6px;cursor:pointer;font-weight:bold;margin-top:8px}
.preview{background:#162447;border-left:4px solid #e94560;padding:16px;margin:16px 0;border-radius:4px;min-height:50px}
.hint{color:#555;font-size:13px}a{color:#e94560}</style></head><body>
<h1>📝 SSTINote</h1>
<p>A note template renderer. Type your note with Jinja2 template syntax!</p>
<p class="hint">Hint: The server renders your input directly as a Jinja2 template. Try <code>{{7*7}}</code> first, then escalate!</p>
<form method="POST">
  <textarea name="note" placeholder="Hello {{name}}! Your score is {{7*7}}">{{ raw_input }}</textarea>
  <button>Render Note</button>
</form>
{% if rendered is not none %}
<h3>Preview:</h3>
<div class="preview">{{ rendered }}</div>
{% endif %}
</body></html>"""

@app.route("/", methods=["GET","POST"])
def index():
    raw_input = ""
    rendered = None
    if request.method == "POST":
        raw_input = request.form.get("note","")
        try:
            # VULNERABLE: user input rendered as Jinja2 template
            rendered = render_template_string(raw_input)
        except Exception as e:
            rendered = f"[Error: {e}]"
    return render_template_string(BASE_TMPL, raw_input=raw_input, rendered=rendered)

# Expose flag through config (accessible via SSTI: config['FLAG'])
app.config['FLAG'] = FLAG

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
