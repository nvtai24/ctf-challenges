from flask import Flask, request, render_template_string, session, redirect
import os

app = Flask(__name__)
app.secret_key = "ctf_file_viewer"

FILES_DIR = "/tmp/files"
os.makedirs(FILES_DIR, exist_ok=True)

# Write public files
with open(f"{FILES_DIR}/readme.txt","w") as f: f.write("Welcome to FileViewer! You can read public documents here.")
with open(f"{FILES_DIR}/help.txt","w") as f: f.write("Use ?file=readme.txt to view files.\nAvailable: readme.txt, help.txt, about.txt")
with open(f"{FILES_DIR}/about.txt","w") as f: f.write("FileViewer v1.0 - A simple document viewer for the office.")
# Hidden flag
os.makedirs("/tmp/secret", exist_ok=True)
with open("/tmp/secret/flag.txt","w") as f: f.write(os.environ.get("FLAG", "CTF{placeholder}"))

TMPL = """<!DOCTYPE html><html><head><title>FileViewer</title>
<style>body{font-family:monospace;background:#fafafa;padding:32px;max-width:900px;margin:auto}
h1{color:#333}nav a{margin-right:12px;color:#0066cc;text-decoration:none}
.viewer{background:#fff;border:1px solid #ddd;border-radius:6px;padding:20px;margin-top:20px;white-space:pre-wrap;min-height:100px}
.err{color:red}.files a{display:inline-block;margin:4px 8px 4px 0;padding:4px 10px;background:#e8f0fe;border-radius:4px;color:#1a73e8;text-decoration:none}
input{padding:8px;width:300px;border:1px solid #ccc;border-radius:4px}button{padding:8px 16px;background:#1a73e8;color:#fff;border:none;border-radius:4px;cursor:pointer}</style></head>
<body>
<h1>📄 FileViewer</h1>
<nav>
  <a href="/">Home</a>
  <a href="/?file=readme.txt">readme.txt</a>
  <a href="/?file=help.txt">help.txt</a>
  <a href="/?file=about.txt">about.txt</a>
</nav>
<hr>
<form method="GET"><input name="file" value="{{ filename }}" placeholder="filename.txt"> <button>View</button></form>
{% if content %}
<div class="viewer">{{ content }}</div>
{% elif error %}
<p class="err">{{ error }}</p>
{% endif %}
</body></html>"""

@app.route("/")
def index():
    filename = request.args.get("file","")
    content = error = ""
    if filename:
        # VULNERABLE: path join without sanitization
        path = os.path.join(FILES_DIR, filename)
        try:
            with open(path) as f:
                content = f.read()
        except FileNotFoundError:
            error = f"File not found: {filename}"
        except Exception as e:
            error = str(e)
    return render_template_string(TMPL, filename=filename, content=content, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
