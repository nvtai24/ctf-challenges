const express = require('express');
const session = require('express-session');
const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(session({ secret: 'pricetag-ctf', resave: false, saveUninitialized: true }));

const products = [
  { id: 1, name: 'Basic VPN Plan',    price: 9.99  },
  { id: 2, name: 'Pro VPN Plan',      price: 29.99 },
  { id: 3, name: 'Enterprise Plan',   price: 99.99 },
  { id: 4, name: '🚩 FLAG TOKEN',     price: 999.99 },
];
const FLAG = process.env.FLAG || 'CTF{placeholder}';

const style = `<style>
body{font-family:monospace;background:#0a192f;color:#ccd6f6;padding:32px;max-width:900px;margin:auto}
h1{color:#64ffda}table{width:100%;border-collapse:collapse}th{background:#112240;color:#64ffda;padding:10px}
td{padding:10px;border-bottom:1px solid #1d3461}tr:hover{background:#112240}
.btn{padding:6px 14px;background:#64ffda;color:#0a192f;border:none;border-radius:4px;cursor:pointer;font-weight:bold}
.cart{background:#112240;border-radius:8px;padding:20px;margin:20px 0}
.flag{color:#64ffda;font-size:18px;font-weight:bold}.bal{color:#ffd700;font-size:18px}
.err{color:#ff6b6b}</style>`;

function cartTotal(cart) {
  return cart.reduce((s,i) => s + i.paid, 0).toFixed(2);
}

app.get('/', (req,res) => {
  if (!req.session.balance) req.session.balance = 10.00;
  if (!req.session.cart) req.session.cart = [];
  const rows = products.map(p =>
    `<tr><td>${p.name}</td><td>$${p.price}</td><td>
      <form method="POST" action="/buy" style="display:inline">
        <input type="hidden" name="id" value="${p.id}">
        <input type="hidden" name="price" value="${p.price}">
        <button class="btn" type="submit">Buy</button>
      </form></td></tr>`).join('');
  const cartRows = req.session.cart.map(i =>
    `<tr><td>${i.name}</td><td>$${i.paid}</td></tr>`).join('') || '<tr><td colspan="2">Empty</td></tr>';
  res.send(`<!DOCTYPE html><html><head><title>PriceTag Shop</title>${style}</head><body>
    <h1>🏪 PriceTag Shop</h1>
    <p>Your balance: <span class="bal">$${req.session.balance.toFixed(2)}</span></p>
    <p style="color:#888">Hint: You only have $10. The FLAG TOKEN costs $999.99. Find a way to buy it cheap.</p>
    <table><tr><th>Product</th><th>Price</th><th>Action</th></tr>${rows}</table>
    <div class="cart"><h3>🛒 Cart</h3>
    <table><tr><th>Item</th><th>Paid</th></tr>${cartRows}</table>
    <p>Total paid: $${cartTotal(req.session.cart)}</p>
    <form method="POST" action="/checkout"><button class="btn">Checkout</button></form></div>
    ${req.session.msg ? `<p class="${req.session.msg.startsWith('❌')?'err':'flag'}">${req.session.msg}</p>` : ''}
    <form method="POST" action="/reset"><button class="btn" style="background:#ff6b6b">Reset</button></form>
  </body></html>`);
});

// VULNERABLE: trusts client-supplied price
app.post('/buy', (req,res) => {
  const id = parseInt(req.body.id);
  const paid = parseFloat(req.body.price);
  const product = products.find(p => p.id === id);
  if (!product) { req.session.msg = '❌ Product not found'; return res.redirect('/'); }
  if (req.session.balance < paid) { req.session.msg = '❌ Insufficient balance'; return res.redirect('/'); }
  req.session.balance = parseFloat((req.session.balance - paid).toFixed(2));
  req.session.cart.push({ name: product.name, paid: paid, id: id });
  req.session.msg = `✅ Added "${product.name}" to cart for $${paid}`;
  res.redirect('/');
});

app.post('/checkout', (req,res) => {
  const hasFlag = req.session.cart.some(i => i.id === 4);
  req.session.msg = hasFlag
    ? `🚩 ${FLAG}`
    : '❌ You need to buy the FLAG TOKEN first!';
  res.redirect('/');
});

app.post('/reset', (req,res) => { req.session.destroy(); res.redirect('/'); });
app.listen(3000);
