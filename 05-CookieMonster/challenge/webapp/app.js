const express = require('express');
const cookieParser = require('cookie-parser');
const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

const html = (body) => `<!DOCTYPE html><html><head><title>CookieMonster</title>
<style>body{font-family:monospace;background:#2b2b2b;color:#f8f8f2;padding:40px;max-width:700px;margin:auto}
h1{color:#f1fa8c}a{color:#8be9fd;text-decoration:none}.card{background:#44475a;border-radius:8px;padding:20px;margin:16px 0}
.flag{color:#50fa7b;font-size:20px;font-weight:bold}.err{color:#ff5555}
input,button{padding:10px;border-radius:4px;border:none;margin:4px;font-size:14px}
input{background:#6272a4;color:#fff;width:200px}button{background:#bd93f9;color:#282a36;cursor:pointer;font-weight:bold}</style></head>
<body>${body}</body></html>`;

app.get('/', (req,res) => {
  res.send(html(`<h1>🍪 CookieMonster</h1>
    <p>A members-only site. Login as <b>guest</b> to get started.</p>
    <form method="POST" action="/login">
      <input name="username" placeholder="Username"><input name="password" type="password" placeholder="Password"><br>
      <button type="submit">Login</button>
    </form>
    <p style="color:#6272a4">Credentials: guest / guest123</p>`));
});

app.post('/login', (req,res) => {
  const {username, password} = req.body;
  if (username === 'guest' && password === 'guest123') {
    // VULNERABLE: role stored in plain cookie
    res.cookie('username', 'guest');
    res.cookie('role', 'guest');
    return res.redirect('/dashboard');
  }
  res.send(html(`<h1>🍪 CookieMonster</h1><p class="err">Wrong credentials</p><a href="/">Back</a>`));
});

app.get('/dashboard', (req,res) => {
  const role = req.cookies.role;
  const username = req.cookies.username || 'stranger';
  if (!role) return res.redirect('/');
  if (role === 'admin') {
    res.send(html(`<h1>🍪 CookieMonster</h1>
      <div class="card"><p>Welcome back, <b>${username}</b>! You have admin access.</p>
      <p class="flag">🚩 ${process.env.FLAG || 'CTF{placeholder}'}</p></div>
      <a href="/logout">Logout</a>`));
  } else {
    res.send(html(`<h1>🍪 CookieMonster</h1>
      <div class="card"><p>Hello <b>${username}</b>! You are a <b>${role}</b>.</p>
      <p class="err">Only admins can see the flag. Hint: Check your cookies 👀</p></div>
      <a href="/logout">Logout</a>`));
  }
});

app.get('/logout', (req,res) => { res.clearCookie('username'); res.clearCookie('role'); res.redirect('/'); });
app.listen(3000, () => console.log(':3000'));
