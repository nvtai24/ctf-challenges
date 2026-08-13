from flask import Flask, request, render_template_string, redirect, send_from_directory
import os, uuid

app = Flask(__name__)
UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
FLAG = os.environ.get("FLAG", "CTF{placeholder}")

# Write a secret file only accessible via code execution
with open("/tmp/flag.txt", "w") as f:
    f.write(FLAG)

ALLOWED_EXTS = {'.jpg', '.jpeg', '.png', '.gif'}

TMPL = """<!DOCTYPE html><html><head><title>ImageShare</title>
<style>body{font-family:Arial,sans-serif;background:#f0f2f5;padding:32px;max-width:800px;margin:auto}
h1{color:#1877f2}.card{background:#fff;border-radius:10px;padding:24px;margin:16px 0;box-shadow:0 2px 8px rgba(0,0,0,.1)}
input[type=file]{padding:8px;border:2px dashed #1877f2;border-radius:6px;width:100%;box-sizing:border-box}
button{padding:10px 28px;background:#1877f2;color:#fff;border:none;border-radius:6px;cursor:pointer;font-weight:bold;margin-top:12px}
.err{color:#e41e3f;background:#ffeef0;padding:10px;border-radius:6px}
.ok{color:#1d7d37;background:#e8f5e9;padding:10px;border-radius:6px}
.hint{color:#65676b;font-size:13px}
.files a{display:block;color:#1877f2;margin:4px 0}
pre{background:#111;color:#0f0;padding:16px;border-radius:6px;overflow-x:auto}</style></head>
<body>
<h1>🖼 ImageShare</h1>
<div class="card">
  <p>Upload profile images (JPG, PNG, GIF only).</p>
  <p class="hint">⚠️ Hint: The server checks file extension, but what about MIME type and content? Try uploading a .php or .py file disguised as an image.</p>
  <form method="POST" action="/upload" enctype="multipart/form-data">
    <input type="file" name="file"><br>
    <button type="submit">Upload</button>
  </form>
  {% if msg %}<p class="{{ 'ok' if success else 'err' }}">{{ msg }}</p>{% endif %}
</div>
{% if uploaded %}
<div class="card">
  <p>Uploaded file: <a href="/uploads/{{ uploaded }}">{{ uploaded }}</a></p>
  {% if output %}<p>Output:</p><pre>{{ output }}</pre>{% endif %}
</div>
{% endif %}
{% if files %}
<div class="card"><h3>Uploaded Files</h3>
  <div class="files">{% for f in files %}<a href="/uploads/{{ f }}">{{ f }}</a>{% endfor %}</div>
</div>
{% endif %}
</body></html>"""

@app.route("/", methods=["GET"])
def index():
    files = os.listdir(UPLOAD_DIR)
    return render_template_string(TMPL, msg=None, success=False, uploaded=None, output=None, files=files)

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f or f.filename == "":
        return render_template_string(TMPL, msg="No file selected", success=False, uploaded=None, output=None, files=os.listdir(UPLOAD_DIR))
    ext = os.path.splitext(f.filename)[1].lower()
    # VULNERABLE: only checks extension, not content; also allows double extension bypass
    if ext not in ALLOWED_EXTS:
        return render_template_string(TMPL, msg=f"❌ Extension '{ext}' not allowed. Only: {', '.join(ALLOWED_EXTS)}", success=False, uploaded=None, output=None, files=os.listdir(UPLOAD_DIR))
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    f.save(path)
    return render_template_string(TMPL, msg=f"✅ Uploaded as {filename}", success=True, uploaded=filename, output=None, files=os.listdir(UPLOAD_DIR))

@app.route("/uploads/<filename>")
def serve_upload(filename):
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        return "Not found", 404
    # VULNERABLE: executes .py files as server-side code
    if filename.endswith(".py"):
        try:
            result = {}
            with open(path) as src:
                exec(compile(src.read(), filename, 'exec'), result)
            output = result.get("output", "(no output variable set)")
            return render_template_string(TMPL, msg="Executed!", success=True, uploaded=filename, output=str(output), files=os.listdir(UPLOAD_DIR))
        except Exception as e:
            return render_template_string(TMPL, msg=f"Error: {e}", success=False, uploaded=filename, output=None, files=os.listdir(UPLOAD_DIR))
    return send_from_directory(UPLOAD_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
