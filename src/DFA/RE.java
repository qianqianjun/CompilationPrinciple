package DFA;
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
class DFAStatus{
    public static Integer amount=0;
    public Integer symble;
    public TreeSet<Integer> closure;
    public Boolean isAcceptable;
    public static ArrayList<Integer> AcceptStatusNum=new ArrayList<Integer>();
    public DFAStatus(TreeSet<Integer> tree)
    {
        this.closure=tree;
        this.isAcceptable=false;
    }
    //如果是一个没有的全新的状态，那么就创造一个新的状态标号。
    public void initSymble()
    {
        this.symble=amount++;
    }
    //如果这个状态已经有了，那么就直接将状态标号赋给这个状态
    public void setSymble(Integer sym)
    {
        this.symble=sym;
    }
    //判断两个状态是否相同。
    public Boolean isEqual(DFAStatus temp)
    {
        TreeSet<Integer> t1=this.closure;
        TreeSet<Integer> t2=temp.closure;
        if(t1.size()!=t2.size())
            return false;
        Iterator it1=t1.iterator();
        Iterator it2=t2.iterator();
        while(it1.hasNext())
        {
            String temp1=it1.next().toString();
            String temp2=it2.next().toString();
            if(!temp1.equals(temp2))
                return false;
        }
        return true;
    }
    public Boolean judgeAcceptable(Integer end)
    {
        Iterator it=this.closure.iterator();
        while(it.hasNext())
        {
            Integer temp=Integer.parseInt(it.next().toString());
            if(temp==end)
            {
                this.isAcceptable=true;
                //AcceptStatusNum=this.symble;
                Integer tem=this.symble;
                AcceptStatusNum.add(tem);
                return true;
            }
        }
        return false;
    }
}
class SimpleDFA{
    public Boolean isAccept;
    public Integer symble;
    public SimpleDFA(Integer s,ArrayList<Integer> arr)
    {
        if(arr.contains(s))
            isAccept=true;
        else
            isAccept=false;
        symble=s;
    }
    //获得当前状态在哪一个区域中。
    public Integer getBlocknum(ArrayList<Block> blocks)
    {
        for(int i=0;i<blocks.size();i++)
        {
            for(int j=0;j<blocks.get(i).statusSet.size();j++)
            {
                if(symble==blocks.get(i).statusSet.get(j)[0].symble)
                {
                    return blocks.get(i).num;
                }
            }
        }
        return -1;
    }
}
class Block{
    public static Integer number=0;
    public Integer num;
    public ArrayList<SimpleDFA []> statusSet;
    //检查这一个区中是否含有要查找的状态
    public Boolean isHave(Integer temp)
    {
        for(int i=0;i<statusSet.size();i++)
        {
            if(statusSet.get(i)[0].symble==temp)
            {
                return true;
            }
        }
        return false;
    }
    public void addStatus(SimpleDFA [] temp)
    {
        this.statusSet.add(temp);
    }
    public void deleteStatus(Integer index)
    {
        this.statusSet.remove(index);
    }
    public Block()
    {
        num=number++;
        statusSet=new ArrayList<SimpleDFA []>();
    }
    //输出这个区的所有状态：调试用：
    public void PrintBlock()
    {
        for(int i=0;i<this.statusSet.size();i++)
        {
            for(int j=0;j<this.statusSet.get(i).length;j++)
            {
                System.out.printf("%4d ",statusSet.get(i)[j].symble);
            }
            System.out.println();
        }
        System.out.println("-----------------------------------");
    }
}
public class RE {
    public static Boolean [][] visit;
    public static ArrayList<String> Head;
    private static Integer statusNum;
    public static TreeSet<Integer> [][] Form;
    public static ArrayList<DFAStatus []> DFAFORM;
    //获得的状态集合简化后的DFA,其实和DFAFORM 没有什么不同，只是结构上做了一些调整和优化。
    public static SimpleDFA [][] simpleDFA;
    public Boolean used=false;
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
    //确定可以引起状态转移的输入符号，这里定义字母和数字。
    public Boolean isInput(char s)
    {
        if(s>='a'&&s<='z')
            return true;
        return  false;
    }
    public void initVisit()
    {
        if(visit==null) {
            visit = new Boolean[Node.number + 2][Node.number + 2];
            for (int i = 0; i <= Node.number; i++) {
                for (int j = 0; j <= Node.number; j++) {
                    visit[i][j] = false;
                }
            }
        }
        else {
            for (int i = 0; i <= Node.number; i++) {
                for (int j = 0; j <= Node.number; j++)
                    visit[i][j] = false;
            }
        }
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
            if(isInput(s.charAt(i)))
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
            if(isInput(s.charAt(i)))
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
                    newline3.tranval="ε".toString();
                    newline4.next=newnode2;
                    newline4.tranval="ε".toString();
                    node1.right.line.add(newline3);
                    node2.right.line.add(newline4);
                    //左边相连：
                    newline1.next=node1.left;
                    newline1.tranval="ε".toString();
                    newline2.next=node2.left;
                    newline2.tranval="ε".toString();
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
                    newline.tranval="ε".toString();
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
                    newline.tranval="ε".toString();
                    node.right.line.add(newline);
                    Node newnode1=new Node();
                    Node newnode2=new Node();
                    newline1.next=node.left;
                    newline1.tranval="ε".toString();
                    newnode1.line.add(newline1);
                    newline2.next=newnode2;
                    newline2.tranval="ε".toString();
                    node.right.line.add(newline2);
                    newline3.next=newnode2;
                    newline3.tranval="ε".toString();
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
        initVisit();
        dfs(head);
    }
    //确定输入包括的所有字符：
    public ArrayList<String> getInputHead(String s)
    {
        Set<String> set=new HashSet<String>();
        for(int i=0;i<s.length();i++)
        {
            if(isInput(s.charAt(i)))
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
        arr.add("ε".toString());
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
        setStatusNum(bottom);
        Form=new TreeSet[statusNum+2][Head.size()];
        for(int i=0;i<=statusNum+1;i++)
        {
            for(int j=0;j<Head.size();j++)
            {
                Form[i][j]=new TreeSet<Integer>();
            }
        }
        initVisit();
        deep(head);
        System.out.printf("%6s ","Status".toString());
        for(int i=0;i<Head.size();i++)
        {
            System.out.printf("%20s ",Head.get(i));
        }
        System.out.println();
        for(int i=0;i<=statusNum;i++)
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
    //设置状态数字。
    public void setStatusNum(Node temp)
    {
        statusNum=temp.num;
        return ;
    }
    //判断特定的输入可以转到的状态，包括空边合并后的结果：
    public void Closure(Integer row,String tranval,TreeSet<Integer> temp)
    {
        Integer col=Head.indexOf(tranval);
        TreeSet<Integer> par=Form[row][col];
        Iterator it=par.iterator();
        if(!used) {
            while (it.hasNext()) {
                Integer newnum = Integer.parseInt(it.next().toString());
                if (!visit[row][newnum]) {
                    visit[row][newnum] = true;
                    used = true;
                    temp.add(newnum);
                    Closure(newnum, tranval, temp);
                }
            }
            used=false;
        }
        col=Head.indexOf("ε".toString());
        par=Form[row][col];
        it =par.iterator();
        while (it.hasNext())
        {
            Integer newnum=Integer.parseInt(it.next().toString());
            if(!visit[row][newnum])
            {
                visit[row][newnum]=true;
                temp.add(newnum);
                Closure(newnum,tranval,temp);
            }
        }
    }
    //返回ε闭包
    public void Closure(Integer row,TreeSet<Integer> temp)
    {
        Integer col=Head.indexOf("ε".toString());
        TreeSet<Integer> par=Form[row][col];
        Iterator it =par.iterator();
        while (it.hasNext())
        {
            Integer newnum=Integer.parseInt(it.next().toString());
            if(!visit[row][newnum])
            {
                visit[row][newnum]=true;
                temp.add(newnum);
                Closure(newnum,temp);
            }
        }
    }
    public void getClosure(Integer row,String tranval,TreeSet<Integer> temp)
    {
        initVisit();
        Closure(row,tranval,temp);
    }
    public void getClosure(Integer row,TreeSet<Integer> temp)
    {
        initVisit();
        Closure(row,temp);
    }
    public void getSimpleDfaArray()
    {
        simpleDFA=new SimpleDFA[DFAFORM.size()][Head.size()];
        for(int i=0;i<DFAFORM.size();i++)
        {
            for(int j=0;j<Head.size();j++)
            {
                SimpleDFA temp=new SimpleDFA(DFAFORM.get(i)[j].symble,DFAStatus.AcceptStatusNum);
                simpleDFA[i][j]=temp;
            }
        }
    }
    public ArrayList<DFAStatus []> getDFA(Node head,Node bottom)
    {
        //首先，找到起始状态的ε闭包，作为一个新的起点。
        TreeSet<Integer> Start=new TreeSet<Integer>();
        getClosure(head.num,Start);
        Start.add(head.num);
        DFAStatus start=new DFAStatus(Start);
        start.initSymble();
        DFAStatus [] row=new DFAStatus[Head.size()+1];
        row[0]=start;
        ArrayList<DFAStatus []> DFAform=new ArrayList<DFAStatus[]>();
        DFAform.add(row);
        for(int i=0;i<DFAform.size();i++)
        {
            for(int j=0;j<Head.size()-1;j++)
            {
                TreeSet<Integer> elem=new TreeSet<Integer>();
                //找到当前状态开始。
                Iterator it=DFAform.get(i)[0].closure.iterator();
                while(it.hasNext())
                {
                    Integer newnum=Integer.parseInt(it.next().toString());
                    getClosure(newnum,Head.get(j),elem);
                }
                if(elem.size()==0) {
                    TreeSet<Integer> Null=new TreeSet<Integer>();
                    DFAStatus NULL=new DFAStatus(Null);
                    NULL.setSymble(-1);
                    DFAform.get(i)[j + 1]=NULL;
                }
                else
                {
                    DFAStatus status=new DFAStatus(elem);
                    Boolean flag=true;
                    for(int k=0;k<DFAform.size();k++)
                    {
                        if(DFAform.get(k)[0].isEqual(status))
                        {
                            status.setSymble(DFAform.get(k)[0].symble);
                            DFAform.get(i)[j+1]=status;
                            flag=false;
                            break;
                        }
                    }
                    if(flag)
                    {
                        status.initSymble();
                        DFAform.get(i)[j+1]=status;
                        DFAStatus [] newrow=new DFAStatus[Head.size()+1];
                        newrow[0]=status;
                        DFAform.add(newrow);
                    }
                }
            }
        }
        for(int i=0;i<DFAform.size();i++)
        {
            DFAform.get(i)[0].judgeAcceptable(bottom.num);
        }
        DFAFORM=DFAform;
        getSimpleDfaArray();
        getSimpleDfaArray();
        return DFAform;
    }
    //输出集合表示的DFA（未化简状态的DFA）
    public void PrintSetDFA()
    {
        for(int i=0;i<DFAFORM.size();i++)
        {
            for(int j=0;j<Head.size();j++)
            {
                Iterator it=DFAFORM.get(i)[j].closure.iterator();
                StringBuffer sb=new StringBuffer();
                sb.append("{".toString());
                while(it.hasNext())
                {
                    sb.append(it.next().toString());
                    sb.append(",");
                }
                Integer index=sb.lastIndexOf(",");
                if(index!=-1)
                    sb.deleteCharAt(index);
                sb.append("}");
                System.out.printf("%20s ",sb.toString());
            }
            System.out.println();
        }
    }
    //输出状态化简后的DFA（将集合表示的状态改用某一个标号）
    public void PrintSymbleDFA()
    {
        for(int i=0;i<DFAFORM.size();i++)
        {
            for(int j=0;j<Head.size();j++)
            {
                if(DFAStatus.AcceptStatusNum.contains(DFAFORM.get(i)[j].symble))
                    System.out.printf("%20d*",DFAFORM.get(i)[j].symble);
                else
                    System.out.printf("%20d ",DFAFORM.get(i)[j].symble);
            }
            System.out.println();
        }
    }
    public void PrintBlock(ArrayList<Block> Blocks)
    {
        for(int i=0;i<Blocks.size();i++)
        {
            Blocks.get(i).PrintBlock();
        }
    }
    public ArrayList<Block> getMinDFA() {
        //将原始的集合划分为可接受集合和不可接受集合：
        Block block1=new Block();
        Block block2=new Block();
        for(int i=0;i<DFAFORM.size();i++) {
            if (simpleDFA[i][0].isAccept) {
                block2.addStatus(simpleDFA[i]);
            }
            else {
                block1.addStatus(simpleDFA[i]);
            }
        }
        //初始化列表，只有两个区，可接受区和不可接受区域。
        ArrayList<Block> BlockSet=new ArrayList<Block>();
        BlockSet.add(block1);
        BlockSet.add(block2);
        int i=0;
        while(i<BlockSet.size())
        {
            if(BlockSet.get(i).statusSet.size()==1)
            {
                i++;
                continue;
            }
            else
            {
                Integer index=1;
                StringBuffer sb=new StringBuffer();
                SimpleDFA [] begin=BlockSet.get(i).statusSet.get(0);
                for(int j=1;j<begin.length;j++)
                {
                    sb.append(begin[j].getBlocknum(BlockSet).toString());
                }
                for(int j=1;j<BlockSet.get(i).statusSet.size();j++)
                {
                    SimpleDFA [] row= BlockSet.get(i).statusSet.get(j);
                    StringBuffer sb2=new StringBuffer();
                    for(int k=1;k<row.length;k++)
                    {
                        sb2.append(row[k].getBlocknum(BlockSet).toString());
                    }
                    if(sb.toString().equals(sb2.toString()))
                    {
                        index++;
                        continue;
                    }
                    else
                    {
                        break;
                    }
                }
                if(index==BlockSet.get(i).statusSet.size())
                {
                    i++;
                }
                else
                {
                    Block newblock=new Block();
                    for(int m=0;m<index;m++)
                    {
                        newblock.addStatus(BlockSet.get(i).statusSet.get(m));
                        BlockSet.get(i).deleteStatus(m);
                    }
                    ArrayList<SimpleDFA []> newstatusset=new ArrayList<SimpleDFA []>();
                    for(int m=index;m<BlockSet.get(i).statusSet.size();m++)
                    {
                        newstatusset.add(BlockSet.get(i).statusSet.get(m));
                    }
                    BlockSet.get(i).statusSet=newstatusset;
                    BlockSet.add(newblock);
                    i=0;
                }
            }
        }
        PrintBlock(BlockSet);
        return BlockSet;
    }

}
