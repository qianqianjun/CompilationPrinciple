package main;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import javax.servlet.ServletException;
import javax.servlet.ServletOutputStream;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.swing.*;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
@WebServlet("/Machine")
public class Machine extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println("这是post方法");
        String s = request.getParameter("string");
        System.out.println(s);
        RE re = new RE();
        String temp = re.getRE(s);
        String postfix = re.getPostfix(temp);
        stackNode node = re.getNFA(postfix);
        Node head = node.left;
        Node bottom = node.right;
        re.getNfaForm(head, s, bottom);
        re.getDFA(head, bottom);
        re.PrintSetDFA();
        re.PrintSymbleDFA();
        //最小化DFA
        ArrayList<Block> blocks = re.getMinDFA();
        String[] title = new String[re.Head.size()];
        for (int i = 0; i < re.Head.size() - 1; i++) {
            title[i + 1] = re.Head.get(i);
        }
        title[0] = "ST";
        String[][] arr = new String[blocks.size()][re.Head.size()];
        for (int i = 0; i < blocks.size(); i++) {
            for (int j = 0; j < re.Head.size(); j++) {
                if (blocks.get(i).statusSet.get(0)[j].isAccept) {
                    arr[i][j] = blocks.get(i).statusSet.get(0)[j].getBlocknum(blocks).toString() + "*".toString();
                } else {
                    arr[i][j] = blocks.get(i).statusSet.get(0)[j].getBlocknum(blocks).toString();
                }
            }
        }
        for (int i = 0; i < title.length; i++) {
            System.out.printf("%20s ", title[i]);
        }
        System.out.println();
        for (int i = 0; i < arr.length; i++) {
            for (int j = 0; j < arr[i].length; j++) {
                System.out.printf("%20s ", arr[i][j]);
            }
            System.out.println();
        }
        Object[] res = new Object[3];
        //将每一个类的静态成员变量恢复到零：
        res[0] = arr;
        res[1] = re.NFA;
        res[2] = title;
        Object DfaArr = JSONObject.toJSON(res);
        Node.number = 0;
        DFAStatus.amount = 0;
        DFAStatus.AcceptStatusNum.clear();
        Block.number = 0;
        RE.statusNum = 0;
        Object DfaReturn = JSONArray.toJSON(DfaArr);
        PrintWriter printWriter = response.getWriter();
        printWriter.println(DfaReturn);
        printWriter.flush();
        printWriter.close();
    }
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println("这是get方法");
    }
}
