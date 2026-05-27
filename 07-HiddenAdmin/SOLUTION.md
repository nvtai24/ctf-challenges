# Challenge 07: HiddenAdmin - Solution

## Vulnerability Type
**Parameter Tampering / Broken Access Control**

## Description
The application checks the user's role from a URL parameter instead of the server-side session, allowing users to escalate privileges by manipulating the URL.

## Vulnerable Code
```jsp
<%
  String role = request.getParameter("role");
  if(role == null) role = (String) session.getAttribute("role");
  // ...
  if("admin".equals(role)){ 
    // Show flag
  }
%>
```

## Exploitation Steps

1. Login with credentials: `staff` / `staff2024`
2. You'll be redirected to `dashboard.jsp` as a regular staff member
3. The role is checked from URL parameter first, then session
4. Add `?role=admin` to the URL: `/dashboard.jsp?role=admin`
5. The application displays the admin content with the flag

## Direct URL
```
http://[host]/dashboard.jsp?role=admin
```

## Flag
```
FCTF{r0l3_param_byp4ss_ez}
```

## How It Works
- The code first checks `request.getParameter("role")` (URL parameter)
- Only if that's null, it falls back to `session.getAttribute("role")`
- This allows any authenticated user to override their role via URL

## Mitigation
- Never trust client-supplied parameters for authorization decisions
- Always use server-side session for role information:
  ```jsp
  String role = (String) session.getAttribute("role");
  // Don't check request parameters for security-critical data
  ```
- Implement proper access control checks
- Use a security framework (Spring Security, Apache Shiro)
- Validate authorization on every protected resource
- Follow principle of least privilege
