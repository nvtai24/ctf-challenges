const express = require('express');
const session = require('express-session');
const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(session({ secret: 'race-ctf', resave: false, saveUninitialized: true }));

// In-memory accounts (shared state - vulnerable to race)
const accounts = {};
function getAccount(id) {
  if (!accounts[id]) accounts[id] = { balance: 100, redeemed: false };
  return accounts[id];
}

const FLAG = 'FCTF{r4c3_c0nd1t10n_d0ubl3_sp3nd}';
const style = `<style>body{font-family:monospace;background:#0f0e17;color:#fffffe;padding:40px;max-width:700px;margin:auto}
h1{color:#ff8906}.card{background:#1a1a2e;border-radius:10px;padding:24px;margin:16px 0}
button{padding:10px 24px;background:#ff8906;color:#0f0e17;border:none;border-radius:6px;cursor:pointer;font-weight:bold;margin:4px}
a{color:#ff8906}.flag{color:#3da9fc;font-size:18px;font-weight:bold}
.bal{font-size:24px;color:#ff8906;font-weight:bold}.hint{color:#555;font-size:13px}</style>`;

app.get('/', (req,res) => {
  if (!req.session.id_key) req.session.id_key = Math.random().toString(36).slice(2);
  const acc = getAccount(req.session.id_key);
  res.send(`<!DOCTYPE html><html><head><title>RaceCondition</title>${style}</head><body>
    <h1>⚡ CouponShop</h1>
    <div class="card">
      <p>Balance: <span class="bal">$${acc.balance}</span></p>
      <p>Coupon redeemed: <b>${acc.redeemed}</b></p>
      <p class="hint">Each account gets ONE $50 coupon. The FLAG costs $200. Can you redeem faster?</p>
      <form method="POST" action="/redeem"><button>Redeem $50 Coupon</button></form>
      <form method="POST" action="/buy-flag"><button>Buy FLAG ($200)</button></form>
    </div>
    ${acc.balance >= 200 ? '' : ''}
    ${req.session.flag ? `<div class="card"><p class="flag">🚩 ${req.session.flag}</p></div>` : ''}
    <a href="/reset">Reset account</a>
  </body></html>`);
});

// VULNERABLE: check-then-act race condition (no mutex)
app.post('/redeem', async (req,res) => {
  const acc = getAccount(req.session.id_key);
  if (acc.redeemed) {
    req.session.msg = '❌ Coupon already used';
    return res.redirect('/');
  }
  // Artificial delay simulating DB operation - race window
  await new Promise(r => setTimeout(r, 50));
  acc.redeemed = true;
  acc.balance += 50;
  res.redirect('/');
});

app.post('/buy-flag', (req,res) => {
  const acc = getAccount(req.session.id_key);
  if (acc.balance >= 200) {
    acc.balance -= 200;
    req.session.flag = FLAG;
  }
  res.redirect('/');
});

app.get('/reset', (req,res) => {
  if (req.session.id_key) delete accounts[req.session.id_key];
  req.session.destroy();
  res.redirect('/');
});
app.listen(3000);
