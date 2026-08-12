const express = require('express');
const session = require('express-session');
const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(session({ secret: 'ctf-secret', resave: false, saveUninitialized: false }));

const users = {
  1: { username: 'alice', password: 'alice123', role: 'admin' },
  2: { username: 'bob',   password: 'bob456',   role: 'user'  },
  3: { username: 'carol', password: 'carol789', role: 'user'  },
};
const notes = {
  1: { owner: 2, title: 'Shopping List',   content: 'Milk, Eggs, Bread' },
  2: { owner: 2, title: 'Meeting Notes',   content: 'Q3 review at 3pm' },
  3: { owner: 1, title: '🚩 Admin Secret', content: process.env.FLAG || 'CTF{placeholder}' },
  4: { owner: 3, title: 'My Diary',        content: 'Today was a good day' },
  5: { owner: 2, title: 'Gym Plan',        content: 'Monday: legs, Tuesday: chest' },
};

const html = (title, body) => `<!DOCTYPE html><html><head><title>${title}</title>
<style>body{font-family:monospace;background:#0d1117;color:#c9d1d9;padding:32px;max-width:800px;margin:auto}
h1,h2{color:#58a6ff}a{color:#58a6ff;text-decoration:none}a:hover{text-decoration:underline}
.card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;margin:12px 0}
.flag{color:#3fb950;font-size:18px;font-weight:bold}
input,button{padding:8px 14px;border-radius:4px;border:1px solid #30363d;background:#21262d;color:#c9d1d9;margin:4px}
button{background:#238636;border-color:#2ea043;cursor:pointer;color:#fff}
.err{color:#f85149}.tag{background:#1f6feb;color:#fff;border-radius:4px;padding:2px 8px;font-size:12px}</style></head>
<body>${body}</body></html>`;

app.get('/', (req, res) => {
  if (req.session.user) return res.redirect('/notes');
  res.send(html('Login', `<h1>📓 SecretNote</h1>
    <p>A private note-taking app. Login to view your notes.</p>
    <form method="POST" action="/login">
      <input name="username" placeholder="Username"><br>
      <input name="password" type="password" placeholder="Password"><br>
      <button type="submit">Login</button>
    </form>
    <p style="color:#666">Hint: You are logged in as <b>bob</b>. Find the admin's secret note.</p>`));
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  const user = Object.entries(users).find(([,u]) => u.username===username && u.password===password);
  if (user) {
    req.session.user = { id: parseInt(user[0]), ...user[1] };
    return res.redirect('/notes');
  }
  res.send(html('Login', `<h1>📓 SecretNote</h1><p class="err">Invalid credentials</p><a href="/">Back</a>`));
});

app.get('/notes', (req, res) => {
  if (!req.session.user) return res.redirect('/');
  const myNotes = Object.entries(notes)
    .filter(([,n]) => n.owner === req.session.user.id)
    .map(([id,n]) => `<div class="card"><a href="/note/${id}"><b>${n.title}</b></a></div>`).join('');
  res.send(html('My Notes', `<h1>📓 My Notes</h1>
    <p>Hello, <b>${req.session.user.username}</b> <span class="tag">${req.session.user.role}</span></p>
    ${myNotes || '<p>No notes yet.</p>'}
    <br><a href="/logout">Logout</a>`));
});

// VULNERABLE: no ownership check
app.get('/note/:id', (req, res) => {
  if (!req.session.user) return res.redirect('/');
  const note = notes[req.params.id];
  if (!note) return res.send(html('Not Found', '<h2>Note not found</h2><a href="/notes">Back</a>'));
  const isFlag = req.params.id === '3';
  res.send(html(note.title, `<h2>${note.title}</h2>
    <div class="card">${isFlag ? `<p class="flag">${note.content}</p>` : `<p>${note.content}</p>`}</div>
    <a href="/notes">← Back to my notes</a>`));
});

app.get('/logout', (req, res) => { req.session.destroy(); res.redirect('/'); });
app.listen(3000, () => console.log('Running on :3000'));
