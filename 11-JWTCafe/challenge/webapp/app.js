const express = require('express');
const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Manual JWT decode - VULNERABLE: accepts "none" algorithm
function base64urlDecode(str) {
  str = str.replace(/-/g,'+').replace(/_/g,'/');
  while(str.length % 4) str += '=';
  return Buffer.from(str, 'base64').toString('utf8');
}
function parseJWT(token) {
  try {
    const parts = token.split('.');
    const header  = JSON.parse(base64urlDecode(parts[0]));
    const payload = JSON.parse(base64urlDecode(parts[1]));
    return { header, payload, valid: true };
  } catch(e) { return { valid: false }; }
}
function base64urlEncode(str) {
  return Buffer.from(str).toString('base64').replace(/\+/g,'-').replace(/\//g,'_').replace(/=/g,'');
}
function createJWT(payload) {
  const header = { alg: 'HS256', typ: 'JWT' };
  const h = base64urlEncode(JSON.stringify(header));
  const p = base64urlEncode(JSON.stringify(payload));
  // fake sig for demo
  const sig = base64urlEncode('valid-signature-' + JSON.stringify(payload));
  return `${h}.${p}.${sig}`;
}

const style = `<style>body{font-family:monospace;background:#1e1e2e;color:#cdd6f4;padding:40px;max-width:800px;margin:auto}
h1{color:#cba6f7}.card{background:#313244;border-radius:10px;padding:24px;margin:16px 0}
input{padding:10px;margin:6px;background:#45475a;border:1px solid #585b70;color:#cdd6f4;border-radius:6px;width:280px}
button{padding:10px 24px;background:#cba6f7;color:#1e1e2e;border:none;border-radius:6px;cursor:pointer;font-weight:bold}
a{color:#cba6f7}.flag{color:#a6e3a1;font-size:18px;font-weight:bold}
.token{word-break:break-all;background:#181825;padding:12px;border-radius:6px;color:#89b4fa;font-size:13px}
.err{color:#f38ba8}.hint{color:#6c7086;font-size:13px}</style>`;

app.get('/', (req,res) => res.send(`<!DOCTYPE html><html><head><title>JWTCafe</title>${style}</head><body>
  <h1>☕ JWTCafe</h1>
  <div class="card"><p>A coffee ordering system using JWT authentication.</p>
  <p>Login as <b>guest</b> to get a JWT. Then try to become <b>admin</b>.</p>
  <form method="POST" action="/login">
    <input name="username" placeholder="Username"><br>
    <input name="password" type="password" placeholder="Password"><br><br>
    <button>Login</button>
  </form>
  <p class="hint">Credentials: guest / guest123</p></div></body></html>`));

app.post('/login', (req,res) => {
  const {username, password} = req.body;
  if (username === 'guest' && password === 'guest123') {
    const token = createJWT({ sub: 'guest', role: 'guest', iat: Date.now() });
    return res.send(`<!DOCTYPE html><html><head><title>JWTCafe</title>${style}</head><body>
      <h1>☕ JWTCafe</h1><div class="card">
      <p>✅ Logged in as <b>guest</b>. Your JWT:</p>
      <div class="token">${token}</div>
      <p class="hint">🔍 Hint: Decode this JWT. What algorithm is used? What if you change it to <b>"none"</b>?</p>
      <br><a href="/menu?token=${token}">→ Go to Menu</a></div></body></html>`);
  }
  res.redirect('/');
});

app.get('/menu', (req,res) => {
  const token = req.query.token || req.headers['authorization']?.split(' ')[1];
  if (!token) return res.redirect('/');
  const parsed = parseJWT(token);
  if (!parsed.valid) return res.send(`<p class="err">Invalid token</p>`);
  const { header, payload } = parsed;
  // VULNERABLE: if alg=none, skip signature check
  const role = payload.role;
  const isAdmin = role === 'admin';
  res.send(`<!DOCTYPE html><html><head><title>Menu</title>${style}</head><body>
    <h1>☕ JWTCafe Menu</h1><div class="card">
    <p>User: <b>${payload.sub}</b> | Role: <b>${role}</b> | Alg: <b>${header.alg}</b></p>
    ${isAdmin
      ? `<p class="flag">🚩 FCTF{jwt_n0n3_4lg_byp4ss}</p><p>Here's your secret admin menu ☕</p>`
      : `<p class="err">Guest menu only. Admins get the special menu with the flag.</p>
         <p class="hint">Hint: Try setting alg to "none" and role to "admin" in the JWT payload.</p>`}
    </div>
    <p class="hint">Current token: <span class="token">${token}</span></p>
    <br><a href="/">← Back</a></body></html>`);
});

app.listen(3000);
