<%@ page contentType="text/html; charset=UTF-8" %>
<%@ page import="java.util.*" %>
<!DOCTYPE html><html><head><title>Dashboard</title>
<style>body{font-family:monospace;background:#1e1e1e;color:#ddd;padding:40px;max-width:700px;margin:auto}
h1{color:#ffd700}.flag{color:#00ff88;font-size:20px;font-weight:bold;background:#1a3a2a;padding:16px;border-radius:6px;margin:16px 0}
.card{background:#2d2d2d;border-radius:8px;padding:20px;margin:12px 0}.err{color:#ff5555}
a{color:#ffd700}.badge{background:#ffd700;color:#000;border-radius:4px;padding:2px 8px;font-size:12px;font-weight:bold}</style>
</head><body>
<h1>🔒 Staff Portal</h1>
<%
  String user = (String) session.getAttribute("username");
  String role = request.getParameter("role");
  if(role == null) role = (String) session.getAttribute("role");
  if(user == null){ response.sendRedirect("index.jsp"); return; }
%>
<div class="card">
  <p>Welcome, <b><%= user %></b> <span class="badge"><%= role %></span></p>
  <% if("admin".equals(role)){ %>
    <div class="flag">🚩 <%= System.getenv("FLAG") != null ? System.getenv("FLAG") : "CTF{placeholder}" %></div>
  <% } else { %>
    <p class="err">You are a regular staff member. Admins only section is hidden.</p>
    <p style="color:#888">Hint: What if you could change your role?</p>
  <% } %>
</div>
<a href="logout">Logout</a>
</body></html>
