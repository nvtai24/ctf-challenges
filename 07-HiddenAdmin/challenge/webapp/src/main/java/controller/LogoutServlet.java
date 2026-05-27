package controller;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import java.io.IOException;
public class LogoutServlet extends HttpServlet {
    protected void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
        req.getSession().invalidate();
        res.sendRedirect("index.jsp");
    }
}
