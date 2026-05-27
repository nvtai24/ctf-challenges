package controller;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import org.w3c.dom.*;
import javax.xml.parsers.*;
import java.io.*;

public class XXEServlet extends HttpServlet {
    private static final String FLAG_PATH = "/app/flag.txt";

    protected void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
        res.setContentType("text/html; charset=UTF-8");
        res.getWriter().write(getHomePage("", ""));
    }

    protected void doPost(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
        res.setContentType("text/html; charset=UTF-8");
        String xmlInput = req.getParameter("xml");
        String result = "", error = "";
        if (xmlInput != null && !xmlInput.isEmpty()) {
            try {
                // VULNERABLE: XXE enabled (no secure factory)
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder builder = factory.newDocumentBuilder();
                Document doc = builder.parse(new ByteArrayInputStream(xmlInput.getBytes("UTF-8")));
                doc.getDocumentElement().normalize();
                NodeList nodes = doc.getElementsByTagName("name");
                StringBuilder sb = new StringBuilder();
                for (int i = 0; i < nodes.getLength(); i++) {
                    sb.append(nodes.item(i).getTextContent()).append("\n");
                }
                result = sb.toString().isEmpty() ? "(no <name> elements found)" : sb.toString();
            } catch (Exception e) {
                error = "Parse error: " + e.getMessage();
            }
        }
        res.getWriter().write(getHomePage(result, error));
    }

    private String getHomePage(String result, String error) {
        String resultHtml = "";
        if (!result.isEmpty()) resultHtml = "<div class='res'><b>Result:</b><pre>" + escHtml(result) + "</pre></div>";
        if (!error.isEmpty())  resultHtml = "<div class='err'>" + escHtml(error) + "</div>";
        return "<!DOCTYPE html><html><head><title>XXEReader</title>" +
            "<style>body{font-family:monospace;background:#1a1a1a;color:#f8f8f2;padding:32px;max-width:900px;margin:auto}" +
            "h1{color:#ff79c6}textarea{width:100%;height:180px;background:#282a36;color:#f8f8f2;border:1px solid #6272a4;border-radius:6px;padding:10px;font-family:monospace}" +
            "button{padding:10px 24px;background:#ff79c6;color:#282a36;border:none;border-radius:6px;cursor:pointer;font-weight:bold;margin-top:8px}" +
            ".res{background:#282a36;border-left:4px solid #50fa7b;padding:12px;margin:12px 0;border-radius:4px}" +
            "pre{margin:0;white-space:pre-wrap;color:#50fa7b}.err{color:#ff5555;margin:12px 0}" +
            ".hint{color:#6272a4;font-size:13px}</style></head><body>" +
            "<h1>📄 XXEReader</h1>" +
            "<p>Submit XML to extract product names.</p>" +
            "<p class='hint'>Hint: Try defining an external entity that reads <code>/app/flag.txt</code></p>" +
            "<form method='POST'><textarea name='xml'>" +
            "&lt;?xml version=\"1.0\"?&gt;\n&lt;products&gt;\n  &lt;name&gt;Laptop&lt;/name&gt;\n  &lt;name&gt;Phone&lt;/name&gt;\n&lt;/products&gt;" +
            "</textarea><br><button type='submit'>Parse XML</button></form>" +
            resultHtml + "</body></html>";
    }

    private String escHtml(String s) {
        return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;");
    }
}
