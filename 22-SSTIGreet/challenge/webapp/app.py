import os
from flask import Flask, request, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{placeholder}")
# Store flag in app config so SSTI can reach it via {{config['FLAG']}}
app.config["FLAG"] = FLAG

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>NoteForge — Template Renderer</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #0d1117; color: #c9d1d9;
      min-height: 100vh;
    }
    header {
      background: #161b22; border-bottom: 1px solid #30363d;
      padding: 16px 40px; display: flex; align-items: center; gap: 12px;
    }
    header h1 { font-size: 20px; color: #58a6ff; }
    header span { font-size: 13px; color: #6e7681; }
    main { max-width: 860px; margin: 40px auto; padding: 0 20px; }
    .intro { margin-bottom: 28px; }
    .intro h2 { color: #e6edf3; margin-bottom: 8px; }
    .intro p { color: #8b949e; font-size: 14px; line-height: 1.6; }
    .editor-panel {
      background: #161b22; border: 1px solid #30363d;
      border-radius: 12px; overflow: hidden; margin-bottom: 24px;
    }
    .editor-header {
      background: #21262d; padding: 10px 16px;
      display: flex; align-items: center; gap: 8px;
      border-bottom: 1px solid #30363d;
    }
    .editor-header span { font-size: 12px; color: #8b949e; }
    .dot { width: 12px; height: 12px; border-radius: 50%; }
    .dot-red { background: #ff5f56; }
    .dot-yellow { background: #ffbd2e; }
    .dot-green { background: #27c93f; }
    textarea {
      width: 100%; min-height: 140px; padding: 16px;
      background: #0d1117; color: #c9d1d9;
      border: none; font-family: 'Courier New', monospace;
      font-size: 14px; resize: vertical;
    }
    textarea:focus { outline: none; }
    .actions { padding: 12px 16px; background: #161b22; border-top: 1px solid #30363d; text-align: right; }
    button {
      background: #238636; color: white; border: none;
      padding: 8px 20px; border-radius: 6px; font-size: 14px;
      cursor: pointer; font-weight: 600;
    }
    button:hover { background: #2ea043; }
    .output-panel {
      background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    }
    .output-header {
      background: #21262d; padding: 10px 16px;
      border-bottom: 1px solid #30363d; font-size: 12px; color: #8b949e;
    }
    .output-body { padding: 20px; min-height: 60px; font-size: 15px; line-height: 1.7; }
    .hint-box {
      margin-top: 28px; background: rgba(88,166,255,0.08);
      border: 1px solid rgba(88,166,255,0.2);
      border-radius: 8px; padding: 16px 20px;
    }
    .hint-box p { font-size: 13px; color: #8b949e; line-height: 1.6; }
    .hint-box code { background: #21262d; padding: 2px 6px; border-radius: 4px; color: #58a6ff; font-size: 13px; }
    .example-list { margin-top: 10px; display: flex; gap: 10px; flex-wrap: wrap; }
    .chip {
      background: #21262d; border: 1px solid #30363d;
      padding: 4px 12px; border-radius: 20px; font-size: 12px;
      color: #79c0ff; cursor: pointer; font-family: monospace;
    }
    .chip:hover { border-color: #58a6ff; }
  </style>
</head>
<body>
  <header>
    <h1>&#128221; NoteForge</h1>
    <span>Powered by Jinja2 Template Engine</span>
  </header>
  <main>
    <div class="intro">
      <h2>Template Renderer</h2>
      <p>Write your notes using Jinja2 syntax for dynamic content. Variables, filters, and expressions are fully supported.</p>
    </div>

    <div class="editor-panel">
      <div class="editor-header">
        <span class="dot dot-red"></span>
        <span class="dot dot-yellow"></span>
        <span class="dot dot-green"></span>
        <span style="margin-left:8px">template.j2</span>
      </div>
      <form method="POST" action="/render">
        <textarea name="template" placeholder="Write your template here...&#10;&#10;Example: Hello {{ '{{' }} name {{ '}}' }}!">{{ prev_input | e }}</textarea>
        <div class="actions">
          <button type="submit">&#9654; Render</button>
        </div>
      </form>
    </div>

    {% if output is not none %}
    <div class="output-panel">
      <div class="output-header">&#128196; Rendered Output</div>
      <div class="output-body">{{ output | safe }}</div>
    </div>
    {% endif %}

    <div class="hint-box">
      <p>&#9881; <strong>Available Jinja2 features:</strong> expressions <code>{{ '{{' }} ... {{ '}}' }}</code>, filters <code>{{ '{{' }} var | upper {{ '}}' }}</code>, built-in globals like <code>config</code>, <code>request</code>, and more.</p>
      <div class="example-list">
        <span class="chip" onclick="setTemplate(this)">{{ '{{' }} 7 * 7 {{ '}}' }}</span>
        <span class="chip" onclick="setTemplate(this)">{{ '{{' }} 'hello' | upper {{ '}}' }}</span>
        <span class="chip" onclick="setTemplate(this)">{{ '{{' }} config {{ '}}' }}</span>
      </div>
    </div>
  </main>
  <script>
    function setTemplate(el) {
      document.querySelector('textarea[name=template]').value = el.textContent.trim();
    }
  </script>
</body>
</html>"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(INDEX_HTML, prev_input="", output=None)


@app.route("/render", methods=["POST"])
def render():
    user_template = request.form.get("template", "")
    try:
        # VULNERABLE: user input rendered directly as Jinja2 template
        output = render_template_string(user_template)
    except Exception as e:
        output = f"<span style='color:#f85149'>&#10060; Template Error: {e}</span>"
    return render_template_string(INDEX_HTML, prev_input=user_template, output=output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
