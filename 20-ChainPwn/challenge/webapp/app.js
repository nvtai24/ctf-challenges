const express = require('express');
const session = require('express-session');
const Database = require('better-sqlite3');
const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(session({ secret: 'chain-ctf-hard', resave: false, saveUninitialized: true }));

// Setup DB
const db = new Database(':memory:');
db.exec(`
  CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT);
  CREATE TABLE flags (id INTEGER PRIMARY KEY, owner_id INTEGER, content TEXT);
  INSERT INTO users VALUES (1,'admin','admin_s3cr3t_pw','admin');
  INSERT INTO users VALUES (2,'bob','bob123','user');
  INSERT INTO flags VALUES (1, 1, '${process.env.FLAG || 'CTF{placeholder}'}');
`);

// Weak JWT: base64(header).base64(payload).base64(header+payload) — no real sig
function makeToken(payload) {
  const h = Buffer.from(JSON.stringify({alg:'HS256',typ:'JWT'})).toString('base64url');
  const p = Buffer.from(JSON.stringify(payload)).toString('base64url');
  const s = Buffer.from(h+'.'+p).toString('base64url'); // fake sig = concat
  return `${h}.${p}.${s}`;
}
function parseToken(token) {
  try {
    const [h,p,s] = token.split('.');
    // VULNERABLE: only checks that sig == base64(h+'.'+p) — forgeable
    const expected = Buffer.from(h+'.'+p).toString('base64url');
    if (s !== expected) return null;
    return JSON.parse(Buffer.from(p,'base64url').toString());
  } catch { return null; }
}

const style = `<style>body{font-family:monospace;background:#13111c;color:#e0def4;padding:32px;max-width:900px;margin:auto}
h1{color:#eb6f92}.card{background:#1f1d2e;border-radius:10px;padding:24px;margin:14px 0;border:1px solid #26233a}
input{padding:10px;background:#26233a;border:1px solid #403d52;color:#e0def4;border-radius:6px;margin:4px;width:240px}
button{padding:10px 22px;background:#eb6f92;color:#13111c;border:none;border-radius:6px;cursor:pointer;font-weight:bold;margin:4px}
a{color:#eb6f92}.flag{color:#31748f;font-size:18px;font-weight:bold}
pre{background:#0f0d1a;padding:12px;border-radius:6px;overflow-x:auto;font-size:13px;color:#9ccfd8}
.hint{color:#555;font-size:12px}.tag{background:#eb6f92;color:#13111c;border-radius:4px;padding:2px 8px;font-size:11px}</style>`;

// STEP 1: Login — vulnerable to SQLi
app.get('/', (req,res) => res.send(`<!DOCTYPE html><html><head><title>ChainPwn</title>${style}</head><body>
  <h1>🔗 ChainPwn</h1>
  <div class="card"><p>Multi-step challenge: SQLi → IDOR → JWT forge</p>
  <p class="hint">Step 1: Bypass login with SQL injection to get admin's JWT token.</p>
  <form method="POST" action="/login">
    <input name="username" placeholder="Username"><br>
    <input name="password" type="password" placeholder="Password"><br><br>
    <button>Login</button>
  </form>
  <p class="hint">You know bob's creds (bob/bob123). Can you get admin's token?</p></div>
</body></html>`));

app.post('/login', (req,res) => {
  const {username, password} = req.body;
  // VULNERABLE: SQLi in login
  let user;
  try {
    user = db.prepare(`SELECT * FROM users WHERE username='${username}' AND password='${password}'`).get();
  } catch(e) { return res.send(`<p style="color:red">SQL Error: ${e.message}</p><a href="/">Back</a>`); }
  if (!user) return res.send(`<!DOCTYPE html><html><head>${style.replace('<style>','<head><style>')}</head><body>
    <div class="card"><p style="color:#eb6f92">❌ Invalid credentials</p><a href="/">← Back</a></div></body></html>`);
  const token = makeToken({ uid: user.id, username: user.username, role: user.role });
  req.session.token = token;
  res.redirect('/dashboard');
});

// STEP 2: Dashboard shows token, user can view their own flag
app.get('/dashboard', (req,res) => {
  const token = req.session.token;
  if (!token) return res.redirect('/');
  const payload = parseToken(token);
  if (!payload) return res.redirect('/');
  res.send(`<!DOCTYPE html><html><head><title>Dashboard</title>${style}</head><body>
    <h1>🔗 ChainPwn - Dashboard</h1>
    <div class="card">
      <p>Logged in as: <b>${payload.username}</b> <span class="tag">${payload.role}</span></p>
      <p>Your JWT: <br><pre>${token}</pre></p>
      <p class="hint">Step 2: Use your JWT to access /api/flag?uid=YOUR_ID</p>
      <p class="hint">Step 3: Can you modify the JWT to access uid=1 (admin's flag)?</p>
      <a href="/api/flag?uid=${payload.uid}&token=${token}">→ View my flag (uid=${payload.uid})</a><br><br>
      <a href="/">← Logout</a>
    </div>
  </body></html>`);
});

// STEP 3: Flag API — IDOR + weak JWT
app.get('/api/flag', (req,res) => {
  const token = req.query.token || req.headers['authorization']?.replace('Bearer ','');
  if (!token) return res.json({error:'No token'});
  const payload = parseToken(token);
  if (!payload) return res.json({error:'Invalid token'});
  // VULNERABLE: uses uid from query param, not from token
  const uid = parseInt(req.query.uid) || payload.uid;
  const row = db.prepare('SELECT content FROM flags WHERE owner_id=?').get(uid);
  if (!row) return res.json({error:'No flag for this user'});
  // Extra: only reveal if role=admin in token OR uid matches token uid
  if (uid === 1 && payload.role !== 'admin') {
    return res.json({error:'Admin flags require admin role in JWT'});
  }
  res.json({ flag: row.content, requested_uid: uid, token_user: payload.username });
});

app.listen(3000);
