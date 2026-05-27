package controller;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import java.io.IOException;

public class LoginServlet extends HttpServlet {
    protected void doPost(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
        String u = req.getParameter("username");
        String p = req.getParameter("password");
        if("staff".equals(u) && "staff2024".equals(p)){
            HttpSession s = req.getSession(true);
            s.setAttribute("username","staff");
            s.setAttribute("role","staff");
            res.sendRedirect("dashboard.jsp");
        } else {
            res.sendRedirect("index.jsp?error=1");
        }
    }
}
