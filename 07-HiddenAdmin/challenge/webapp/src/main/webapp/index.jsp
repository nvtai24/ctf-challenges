<%@ page contentType="text/html; charset=UTF-8" %>
<!DOCTYPE html><html><head><title>HiddenAdmin</title>
<style>body{font-family:monospace;background:#1e1e1e;color:#ddd;padding:40px;max-width:700px;margin:auto}
h1{color:#ffd700}a{color:#ffd700;text-decoration:none}.card{background:#2d2d2d;border-radius:8px;padding:20px;margin:16px 0}
input{padding:8px;margin:4px;background:#3d3d3d;border:1px solid #555;color:#ddd;border-radius:4px;width:200px}
button{padding:8px 20px;background:#ffd700;color:#000;border:none;border-radius:4px;cursor:pointer;font-weight:bold}</style>
</head><body>
<h1>🔒 Staff Portal</h1>
<div class="card">
<p>Login to access the portal.</p>
<form method="POST" action="login">
  <input name="username" placeholder="Username"><br>
  <input name="password" type="password" placeholder="Password"><br><br>
  <button type="submit">Login</button>
</form>
<p style="color:#888;font-size:13px">Credentials: staff / staff2024</p>
</div>
</body></html>
