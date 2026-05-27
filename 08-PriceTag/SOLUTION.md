# Challenge 08: PriceTag - Solution

## Vulnerability Type
**Price Manipulation / Client-Side Trust**

## Description
The application trusts the price value sent from the client-side form, allowing users to purchase items at arbitrary prices.

## Vulnerable Code
```javascript
// VULNERABLE: trusts client-supplied price
app.post('/buy', (req,res) => {
  const id = parseInt(req.body.id);
  const paid = parseFloat(req.body.price);
  // ... uses 'paid' without verifying against actual product price
```

## Exploitation Steps

1. You start with $10 balance
2. The FLAG TOKEN costs $999.99
3. Inspect the "Buy" button HTML for FLAG TOKEN:
   ```html
   <input type="hidden" name="price" value="999.99">
   ```
4. Use browser DevTools to edit the hidden field to `0.01` or `1.00`
5. Click "Buy" - you'll purchase the FLAG TOKEN for the modified price
6. Click "Checkout" to get the flag

## Method 1: Browser DevTools
1. Right-click the "Buy" button for FLAG TOKEN
2. Inspect Element
3. Find `<input type="hidden" name="price" value="999.99">`
4. Change value to `1.00`
5. Click Buy

## Method 2: Intercept with Burp Suite
```
POST /buy HTTP/1.1
...
id=4&price=0.01
```

## Flag
```
FCTF{pr1c3_t4mp3r1ng_ch34ts}
```

## How It Works
- The form sends both `id` and `price` to the server
- Server trusts the client-supplied price instead of looking it up
- Attacker can set any price they want

## Mitigation
- Never trust client-supplied prices
- Always look up the price server-side:
  ```javascript
  const product = products.find(p => p.id === id);
  const actualPrice = product.price; // Use this, not req.body.price
  ```
- Only send the product ID from client
- Validate all financial transactions server-side
- Implement integrity checks
- Log all price-related operations for audit
