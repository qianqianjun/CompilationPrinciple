package DFA;
import javax.swing.*;
import javax.swing.table.DefaultTableCellRenderer;
import java.awt.*;
import java.util.*;
import java.io.*;
//ε
public class Main {

    public static void main(String[] args)
    {
        RE re=new RE();
        Scanner cin=new Scanner(new BufferedInputStream(System.in));
        String s=cin.next();
        String temp=re.getRE(s);
        String postfix=re.getPostfix(temp);
        stackNode node=re.getNFA(postfix);
        Node head=node.left;
        Node bottom=node.right;
        re.getNfaForm(head,s,bottom);
        System.out.println("SetDFA");
        re.getDFA(head,bottom);
        re.PrintSetDFA();
        System.out.println("SymbleDFA");
        re.PrintSymbleDFA();
        //最小化DFA
        System.out.println("最小化DFA是：");
        re.getMinDFA();
        cin.close();
    }
}
