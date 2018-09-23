package DFA;
import java.util.*;
import java.io.*;
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
        System.out.println("DFA");
        re.getDFA(head);
        re.PrintSetDFA();
        re.PrintSymbleDFA();
        cin.close();
    }
}
