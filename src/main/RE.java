package main;
import java.lang.reflect.Array;
import java.util.*;
class Line{
    public String tranval;
    public Node next;
}
class Node{
    public Integer num;
    public ArrayList<Line> line;
    public static Integer number=0;
    public Node()
    {
        this.num=number++;
        this.line=new ArrayList<Line>();
    }
}
class stackNode{
    public Node left=null;
    public Node right=null;
}
public class RE {
    public static Integer maxsize=400;
    public static Boolean [][] visit=new Boolean[maxsize+1][maxsize+1];
    public static ArrayList<String> Head;
    public static TreeSet<Integer> [][] Form;
    //得到完整正则表达式的判断函数：
    public Boolean isleft(char s)
    {
        if(s==')'||s>='a'&&s<='z'||s=='*')
        {
            return true;
        }
        return false;
    }
    public Boolean isright(char s)
    {
        if(s>='a'&&s<='z'||s=='(')
        {
            return true;
        }
        return false;
    }
    //得到包括"."的正则表达式：
    public String getRE(String s)
    {
        StringBuffer res=new StringBuffer();
        res.append(s.substring(0, 1));
        for(int i=1;i<s.length();i++)
        {
            if(isleft(s.charAt(i-1))&&isright(s.charAt(i)))
            {
                res.append(".".toString());
                res.append(s.substring(i,i+1));
            }
            else
                res.append(s.substring(i,i+1));
        }
        return res.toString();
    }
    //求后缀表达式的比较函数：
    public int adv(char s)
    {
        if(s=='(')
            return -1;
        if(s=='*')
            return 4;
        if(s=='.')
            return 2;
        if(s=='|')
            return 0;
        return -1;
    }
    //获得后缀表达式
    public String getPostfix(String s)
    {
        StringBuffer res =new StringBuffer();
        Stack<String> stack=new Stack<String>();
        for(int i=0;i<s.length();i++)
        {
            if(s.charAt(i)>='a'&&s.charAt(i)<='z')
            {
                res.append(s.substring(i, i+1));
            }
            else
            {
                if(s.charAt(i)=='(')
                {
                    stack.push(s.substring(i,i+1));
                    continue;
                }
                if(s.charAt(i)==')')
                {
                    String temp=stack.peek();
                    while(!temp.equals("("))
                    {
                        res.append(temp);
                        stack.pop();
                        if(stack.empty())
                            break;
                        temp=stack.peek();
                    }
                    stack.pop();
                    continue;
                }
                if(stack.empty())
                {
                    stack.push(s.substring(i,i+1));
                }
                else
                {
                    String temp=stack.peek();
                    while(adv(temp.charAt(0))>=adv(s.charAt(i)))
                    {
                        res.append(temp);
                        stack.pop();
                        if(stack.empty())
                            break;
                        temp=stack.peek();
                    }
                    stack.push(s.substring(i,i+1));
                }
            }
        }
        while(!stack.empty())
        {
            String temp=stack.peek();
            res.append(temp);
            stack.pop();
        }
        return res.toString();
    }
    public stackNode getNFA(String s) {
        Stack<stackNode> stack=new Stack<stackNode>();
        for(int i=0;i<s.length();i++)
        {
            //构造单个字母的状态转换图
            if(s.charAt(i)>='a'&&s.charAt(i)<='z')
            {
                Node a;
                stackNode stacknode;
                a = new Node();
                stacknode=new stackNode();
                stacknode.left=a;
                Node b=new Node();
                Line newline=new Line();
                newline.next=b;
                newline.tranval=s.substring(i, i+1);
                a.line.add(newline);
                stacknode.right=b;
                stack.push(stacknode);
            }
            else
            {
                if(s.charAt(i)=='|')
                {
                    //要进行 "|"运算的两个NFA;
                    stackNode node1=stack.pop();
                    stackNode node2=stack.pop();
                    //两个新的状态
                    Node newnode1=new Node();
                    Node newnode2=new Node();
                    //四条新边
                    Line newline1=new Line();
                    Line newline2=new Line();
                    Line newline3=new Line();
                    Line newline4=new Line();
                    //右边相连
                    newline3.next=newnode2;
                    newline3.tranval="&".toString();
                    newline4.next=newnode2;
                    newline4.tranval="&".toString();
                    node1.right.line.add(newline3);
                    node2.right.line.add(newline4);
                    //左边相连：
                    newline1.next=node1.left;
                    newline1.tranval="&".toString();
                    newline2.next=node2.left;
                    newline2.tranval="&".toString();
                    newnode1.line.add(newline1);
                    newnode1.line.add(newline2);
                    //创造新的压栈元素，并压栈。
                    stackNode newstacknode=new stackNode();
                    newstacknode.left=newnode1;
                    newstacknode.right=newnode2;
                    stack.push(newstacknode);
                    continue;
                }
                if(s.charAt(i)=='.')
                {
                    //这里的顺序要搞清楚。
                    stackNode node2=stack.pop();
                    stackNode node1=stack.pop();
                    for(int j=0;j<node2.left.line.size();j++)
                    {
                        Line newline=new Line();
                        newline.next=node2.left.line.get(j).next;
                        newline.tranval=node2.left.line.get(j).tranval;
                        node1.right.line.add(newline);
                    }
                    /*Line newline=new Line();
                    newline.next=node2.left;
                    newline.tranval="&".toString();
                    node1.right.line.add(newline);*/
                    node1.right=node2.right;
                    stack.push(node1);
                    continue;
                }
                if(s.charAt(i)=='*')
                {
                    stackNode node=stack.pop();
                    Line newline=new Line();
                    Line newline1=new Line();
                    Line newline2=new Line();
                    Line newline3=new Line();
                    newline.next=node.left;
                    newline.tranval="&".toString();
                    node.right.line.add(newline);
                    Node newnode1=new Node();
                    Node newnode2=new Node();
                    newline1.next=node.left;
                    newline1.tranval="&".toString();
                    newnode1.line.add(newline1);
                    newline2.next=newnode2;
                    newline2.tranval="&".toString();
                    node.right.line.add(newline2);
                    newline3.next=newnode2;
                    newline3.tranval="&".toString();
                    newnode1.line.add(newline3);
                    node.left=newnode1;
                    node.right=newnode2;
                    stack.push(node);
                }
            }
        }
        stackNode node =stack.pop();
        return node;
    }
    //用来Debug使用的深度遍历图方法：
    private void dfs(Node temp)
    {
        System.out.println("************************************");
        System.out.println(temp.num);
        for(int i=0;i<temp.line.size();i++)
        {
            System.out.println(temp.line.get(i).tranval+" "+temp.line.get(i).next.num);
        }
        System.out.println("___________________________________");
        for(int i=0;i<temp.line.size();i++)
        {
            if(!visit[temp.num][temp.line.get(i).next.num])
            {
                visit[temp.num][temp.line.get(i).next.num]=true;
                dfs(temp.line.get(i).next);
            }
        }
    }
    //用来输出NFA，检查是否有错误的方法：
    public void Debag(Node head)
    {
        for(int i=0;i<=Node.number;i++)
        {
            for(int j=0;j<=Node.number;j++)
            {
                visit[i][j]=false;
            }
        }
        dfs(head);
    }
    //确定输入包括的所有字符：
    public ArrayList<String> getInputHead(String s)
    {
        Set<String> set=new HashSet<String>();
        for(int i=0;i<s.length();i++)
        {
            if(s.charAt(i)>='a'&&s.charAt(i)<='z')
            {
                set.add(s.substring(i,i+1));
            }
        }
        //System.out.println(set.size());
        ArrayList<String> arr=new ArrayList<String>();
        Iterator it=set.iterator();
        while(it.hasNext())
        {
            arr.add(it.next().toString());
        }
        arr.add("&".toString());
        return arr;
    }
    //配合getNfaForm函数来进行NFA表格化输出的函数：
    private void deep(Node temp)
    {
        for(int i=0;i<temp.line.size();i++)
        {
            Integer col=Head.indexOf(temp.line.get(i).tranval);
            Integer row=temp.num;
            Integer val=temp.line.get(i).next.num;
            Form[row][col].add(val);
        }
        for(int i=0;i<temp.line.size();i++)
        {
            if(!visit[temp.num][temp.line.get(i).next.num])
            {
                visit[temp.num][temp.line.get(i).next.num]=true;
                deep(temp.line.get(i).next);
            }
        }
    }
    //输出表格形式的NFA:
    public void getNfaForm(Node head,String s,Node bottom)
    {
        Head=getInputHead(s);
        Form=new TreeSet[maxsize][Head.size()];
        for(int i=0;i<maxsize;i++)
        {
            for(int j=0;j<Head.size();j++)
            {
                Form[i][j]=new TreeSet<Integer>();
            }
        }
        for(int i=0;i<=Node.number;i++)
        {
            for(int j=0;j<=Node.number;j++)
            {
                visit[i][j]=false;
            }
        }
        deep(head);
        System.out.printf("%6s ","Status".toString());
        for(int i=0;i<Head.size();i++)
        {
            System.out.printf("%20s ",Head.get(i));
        }
        System.out.println();
        for(int i=0;i<=bottom.num;i++)
        {
            System.out.printf("%6d ",i);
            for(int j=0;j<Head.size();j++)
            {
                StringBuffer sb=new StringBuffer();
                sb.append("{".toString());
                Iterator it=Form[i][j].iterator();
                while(it.hasNext())
                {
                    String temp=it.next().toString();
                    //System.out.print(temp+" ".toString());
                    sb.append(temp);
                    sb.append(",".toString());
                }
                Integer index=sb.lastIndexOf(",".toString());
                if(index!=-1)
                    sb.deleteCharAt(index);
                sb.append("}".toString());
                System.out.printf("%20s ",sb.toString());
            }
            System.out.println();
        }
    }
}
