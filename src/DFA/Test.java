package DFA;
import DFA.RE;
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
    public static void main(String[] args)
    {
        JFrame frame=new JFrame("测试");
        frame.setBounds(100,100,1000,900);
        frame.setLayout(null);
        JTextField textField=new JTextField();
        textField.setColumns(100);
        textField.setBounds(10,10,750,40);
        textField.setFont(new Font("宋体", Font.PLAIN, 20));
        JPanel panel=new JPanel();
        panel.setLayout(null);
        panel.setBounds(0,0,1000,900);
        panel.add(textField);
        frame.add(panel);
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
                panel.remove(jspanel);
                JPanel jspanel=new JPanel();
                jspanel.setBounds(10,60,900,850);
                panel.add(jspanel);
                jspanel.add(js);
            }
        });
        frame.setVisible(true);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
}
