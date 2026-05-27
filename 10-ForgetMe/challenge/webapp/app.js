const express = require('express');
const session = require('express-session');
const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(session({ secret: 'forgetme-ctf', resave: false, saveUninitialized: true }));

const users = {
  alice: { password: 'supersecret!', email: 'alice@corp.com', flag: 'FCTF{br0k3n_p4ssw0rd_r3s3t}' },
  bob:   { password: 'bob123',       email: 'bob@corp.com',   flag: '' },
};
// Predictable reset tokens: username + "2024"
const resetTokens = { alice: 'alice2024', bob: 'bob2024' };

const style = `<style>body{font-family:monospace;background:#1a1a2e;color:#eee;padding:40px;max-width:700px;margin:auto}
h1{color:#e94560}.card{background:#16213e;border-radius:8px;padding:24px;margin:16px 0}
input{padding:10px;margin:6px 0;background:#0f3460;border:1px solid #e94560;color:#eee;border-radius:4px;width:260px}
button{padding:10px 24px;background:#e94560;color:#fff;border:none;border-radius:4px;cursor:pointer;font-weight:bold}
a{color:#e94560;text-decoration:none}.flag{color:#0f9;font-size:18px;font-weight:bold}
.err{color:#f55}.ok{color:#0f9}</style>`;

app.get('/', (req,res) => res.send(`<!DOCTYPE html><html><head><title>ForgetMe</title>${style}</head><body>
  <h1>🔑 Staff Login</h1><div class="card">
  <form method="POST" action="/login">
    <input name="username" placeholder="Username"><br>
    <input name="password" type="password" placeholder="Password"><br><br>
    <button>Login</button>
  </form>
  <p><a href="/forgot">Forgot password?</a></p>
  <p style="color:#555;font-size:13px">Target: alice's account</p></div></body></html>`));

app.post('/login', (req,res) => {
  const {username, password} = req.body;
  const user = users[username];
  if (user && user.password === password) {
    req.session.user = username;
    return res.redirect('/dashboard');
  }
  req.session.msg = '❌ Invalid credentials';
  res.redirect('/');
});

app.get('/dashboard', (req,res) => {
  if (!req.session.user) return res.redirect('/');
  const user = users[req.session.user];
  res.send(`<!DOCTYPE html><html><head><title>Dashboard</title>${style}</head><body>
    <h1>🔑 Dashboard</h1><div class="card">
    <p>Welcome, <b>${req.session.user}</b>!</p>
    ${user.flag ? `<p class="flag">🚩 ${user.flag}</p>` : '<p>No special access.</p>'}
    </div><a href="/logout">Logout</a></body></html>`);
});

app.get('/forgot', (req,res) => res.send(`<!DOCTYPE html><html><head><title>Reset</title>${style}</head><body>
  <h1>🔑 Password Reset</h1><div class="card">
  <form method="POST" action="/forgot">
    <p>Enter your username to receive a reset token.</p>
    <input name="username" placeholder="Username"><br><br>
    <button>Send Token</button>
  </form></div></body></html>`));

app.post('/forgot', (req,res) => {
  const {username} = req.body;
  if (!users[username]) return res.redirect('/forgot');
  // VULNERABLE: token is shown directly in response + is predictable
  const token = resetTokens[username];
  res.send(`<!DOCTYPE html><html><head><title>Reset</title>${style}</head><body>
    <h1>🔑 Password Reset</h1><div class="card">
    <p class="ok">✅ Token generated! (In a real system, this would be emailed.)</p>
    <p style="color:#555">For demo purposes your token is: <b style="color:#e94560">${username.charAt(0)}****</b></p>
    <p>Enter your token below:</p>
    <form method="POST" action="/reset">
      <input name="username" value="${username}" type="hidden">
      <input name="token" placeholder="Reset token"><br>
      <input name="newpassword" type="password" placeholder="New password"><br><br>
      <button>Reset Password</button>
    </form></div></body></html>`);
});

app.post('/reset', (req,res) => {
  const {username, token, newpassword} = req.body;
  // VULNERABLE: predictable token
  if (resetTokens[username] === token) {
    users[username].password = newpassword;
    req.session.user = username;
    return res.redirect('/dashboard');
  }
  res.send(`<!DOCTYPE html><html><head><title>Reset</title>${style}</head><body>
    <h1>🔑 Reset Failed</h1><div class="card"><p class="err">❌ Invalid token.</p>
    <p style="color:#888">Hint: Tokens follow a predictable pattern...</p>
    <a href="/forgot">Try again</a></div></body></html>`);
});

app.get('/logout', (req,res) => { req.session.destroy(); res.redirect('/'); });
app.listen(3000);
