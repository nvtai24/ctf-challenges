const express = require('express');
const { createHandler } = require('graphql-http/lib/use/express');
const { buildSchema } = require('graphql');
const session = require('express-session');
const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(session({ secret: 'graph-ctf', resave: false, saveUninitialized: true }));

const users = {
  1: { id:1, username:'alice', role:'admin', email:'alice@corp.com', secret:'FCTF{gr4phql_1d0r_n0_4uth}' },
  2: { id:2, username:'bob',   role:'user',  email:'bob@corp.com',   secret:'' },
  3: { id:3, username:'carol', role:'user',  email:'carol@corp.com', secret:'' },
};

const schema = buildSchema(`
  type User { id: Int, username: String, role: String, email: String, secret: String }
  type Query {
    me: User
    user(id: Int!): User
    users: [User]
  }
`);

// VULNERABLE: user(id) has no authorization check
const root = {
  me: (args, ctx) => {
    const uid = ctx?.session?.uid;
    return uid ? users[uid] : null;
  },
  user: ({ id }) => users[id] || null,   // no auth check!
  users: () => Object.values(users).map(u => ({ ...u, secret: '' })), // hides secret in listing
};

const style = `<style>body{font-family:monospace;background:#0d1117;color:#c9d1d9;padding:32px;max-width:900px;margin:auto}
h1{color:#58a6ff}.card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:20px;margin:12px 0}
input{padding:8px;background:#21262d;border:1px solid #30363d;color:#c9d1d9;border-radius:4px;margin:4px;width:220px}
button{padding:8px 20px;background:#238636;border:none;border-radius:4px;color:#fff;cursor:pointer;font-weight:bold}
textarea{width:100%;height:120px;background:#21262d;color:#c9d1d9;border:1px solid #30363d;border-radius:4px;padding:10px;font-family:monospace}
pre{background:#0d1117;padding:12px;border-radius:6px;overflow-x:auto;color:#3fb950}
.flag{color:#3fb950;font-weight:bold;font-size:16px}.hint{color:#6e7681;font-size:13px}
a{color:#58a6ff}</style>`;

app.get('/', (req,res) => res.send(`<!DOCTYPE html><html><head><title>GraphAdmin</title>${style}</head><body>
  <h1>🔮 GraphAdmin</h1>
  <div class="card"><p>Login as <b>bob</b> to access the GraphQL API.</p>
  <form method="POST" action="/login">
    <input name="username" placeholder="Username"><input name="password" type="password" placeholder="Password"><br>
    <button>Login</button>
  </form><p class="hint">Credentials: bob / bob123</p></div></body></html>`));

app.post('/login',(req,res)=>{
  const {username,password}=req.body;
  const creds={bob:'bob123',alice:'alice999'};
  const uid=Object.values(users).find(u=>u.username===username)?.id;
  if(uid&&creds[username]===password){req.session.uid=uid;return res.redirect('/graphql-ui');}
  res.redirect('/');
});

app.get('/graphql-ui',(req,res)=>{
  if(!req.session.uid)return res.redirect('/');
  const me=users[req.session.uid];
  res.send(`<!DOCTYPE html><html><head><title>GraphQL</title>${style}</head><body>
    <h1>🔮 GraphQL Explorer</h1>
    <div class="card"><p>Logged in as <b>${me.username}</b> (${me.role})</p>
    <p class="hint">Try querying other users by ID. The <code>secret</code> field holds sensitive data.</p>
    <form method="POST" action="/graphql-ui/query">
      <textarea name="query">{ user(id: 2) { id username role email secret } }</textarea><br>
      <button>Run Query</button>
    </form></div>
    ${req.session.result?`<div class="card"><h3>Result:</h3><pre>${req.session.result}</pre></div>`:''}
    <a href="/logout">Logout</a></body></html>`);
});

app.post('/graphql-ui/query',async(req,res)=>{
  if(!req.session.uid)return res.redirect('/');
  const query=req.body.query||'';
  try{
    const {graphql}=require('graphql');
    const result=await graphql({schema,source:query,rootValue:root,contextValue:{session:req.session}});
    req.session.result=JSON.stringify(result,null,2);
  }catch(e){req.session.result=String(e);}
  res.redirect('/graphql-ui');
});

app.use('/graphql', createHandler({ schema, rootValue: root }));
app.get('/logout',(req,res)=>{req.session.destroy();res.redirect('/');});
app.listen(3000);
