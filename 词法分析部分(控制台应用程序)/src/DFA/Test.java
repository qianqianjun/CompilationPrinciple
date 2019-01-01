package DFA;
import javax.swing.*;
import javax.swing.table.DefaultTableCellRenderer;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

public class Test {
    public static JScrollPane GetProcessTable(Object[][] Data,String[] Title,int width,int height)
    {
        JTable table = new JTable(Data, Title);
        table.setRowHeight(40);
        table.getTableHeader().setPreferredSize(new Dimension(0, 40));
        DefaultTableCellRenderer tcr = new DefaultTableCellRenderer();
        tcr.setHorizontalAlignment(JLabel.CENTER);
        table.setPreferredScrollableViewportSize(new Dimension(width, height));
        JScrollPane scrollPane = new JScrollPane(table);
        scrollPane.setSize(new Dimension(width, height));
        return scrollPane;
    }
    public static JPanel panel=new JPanel();
    public static JFrame frame;
    public static void startup()
    {
        frame=new JFrame("正则表达式到DFA，write by 高谦");
        frame.setBounds(100,100,1000,900);
        frame.setLayout(null);
        frame.add(panel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
    public static void drowPanel()
    {
        panel.setLayout(null);
        panel.setBounds(0,0,1000,900);
        JTextField textField=new JTextField();
        textField.setColumns(100);
        textField.setBounds(10,10,750,40);
        textField.setFont(new Font("宋体", Font.PLAIN, 20));
        panel.add(textField);
        JPanel jspanel=new JPanel();
        jspanel.setBounds(10,60,900,850);
        panel.add(jspanel);
        JButton button =new JButton("输入正则表达式");
        button.setFont(new Font("宋体", Font.PLAIN, 15));
        button.setBounds(770,10,150,40);
        panel.add(button);
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String s=textField.getText();
                textField.setText("");
                RE re=new RE();
                String temp=re.getRE(s);
                String postfix=re.getPostfix(temp);
                System.out.println("后缀表达式是：");
                System.out.println(postfix);
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
                ArrayList<Block> blocks=re.getMinDFA();
                String [] title=new String [re.Head.size()];
                for(int i=0;i<re.Head.size()-1;i++)
                {
                    title[i+1]=re.Head.get(i);
                }
                title[0]="初始状态";
                String [][] arr=new String [blocks.size()][re.Head.size()];
                for(int i=0;i<blocks.size();i++)
                {
                    for(int j=0;j<re.Head.size();j++)
                    {
                        if(blocks.get(i).statusSet.get(0)[j].isAccept)
                        {
                            arr[i][j]=blocks.get(i).statusSet.get(0)[j].getBlocknum(blocks).toString()+"*".toString();
                        }
                        else
                        {
                            arr[i][j]=blocks.get(i).statusSet.get(0)[j].getBlocknum(blocks).toString();
                        }
                    }
                }
                JScrollPane js=GetProcessTable(arr,title,900,800);
                panel.removeAll();
                JPanel jspanel=new JPanel();
                jspanel.setBounds(10,60,900,850);
                jspanel.add(js);
                panel.add(jspanel);
                drowPanel();
                panel.repaint();
                //将每一个类的静态成员变量恢复到零：
                Node.number=0;
                DFAStatus.amount=0;
                DFAStatus.AcceptStatusNum.clear();
                Block.number=0;
                RE.statusNum=0;
            }
        });
        frame.setVisible(true);
    }
    public static void main(String[] args)
    {
        startup();
        drowPanel();
    }
}
