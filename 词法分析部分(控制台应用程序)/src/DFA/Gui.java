package DFA;
import java.awt.EventQueue;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JLabel;
import java.awt.Font;
import javax.swing.JTextField;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.SystemColor;

public class Gui extends JFrame {

    private JPanel framePanel;
    private JTextField inputRE;
    public static void main(String[] args) {
        EventQueue.invokeLater(new Runnable() {
            public void run() {
                try {
                    Gui frame = new Gui();
                    frame.setVisible(true);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
    }
    public Gui() {
        setTitle("\u4ECE\u6B63\u5219\u8868\u8FBE\u5F0F\u5230\u6700\u5C0F\u5316DFA  power by \u9AD8\u8C26");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setBounds(100, 100, 1277, 738);
        framePanel = new JPanel();
        framePanel.setBorder(new EmptyBorder(5, 5, 5, 5));
        setContentPane(framePanel);
        framePanel.setLayout(null);

        JPanel inputPanel = new JPanel();
        inputPanel.setBounds(21, 24, 1152, 124);
        framePanel.add(inputPanel);
        inputPanel.setLayout(null);

        JLabel inputLabel = new JLabel("\u8F93\u5165\u6B63\u5219\u8868\u8FBE\u5F0F");
        inputLabel.setBounds(0, 10, 118, 20);
        inputPanel.add(inputLabel);
        inputLabel.setFont(new Font("宋体", Font.PLAIN, 17));

        inputRE = new JTextField();
        inputRE.setFont(new Font("宋体", Font.PLAIN, 21));
        inputRE.setBounds(0, 37, 560, 38);
        inputPanel.add(inputRE);
        inputRE.setColumns(10);

        JLabel RE = new JLabel("正则表达式：");
        RE.setFont(new Font("Dialog", Font.PLAIN, 17));
        RE.setBounds(0, 81, 809, 33);
        inputPanel.add(RE);

        JButton inputButton = new JButton("\u8BCD\u6CD5\u5206\u6790");
        inputButton.setFont(new Font("宋体", Font.PLAIN, 17));
        inputButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String val=inputRE.getText();
                if(val.equals("".toString()))
                {
                    RE.setText("您没有进行输入，无法解析");
                }
                else
                {
                    RE.setText("正在解析："+val);
                }
            }
        });
        inputButton.setBounds(584, 38, 118, 38);
        inputPanel.add(inputButton);

        JPanel NFAPanel = new JPanel();
        NFAPanel.setBackground(SystemColor.inactiveCaptionBorder);
        NFAPanel.setBounds(21, 216, 270, 445);
        framePanel.add(NFAPanel);

        JLabel NFALabel = new JLabel("NFA");
        NFALabel.setFont(new Font("宋体", Font.PLAIN, 17));
        NFALabel.setBounds(21, 177, 58, 29);
        framePanel.add(NFALabel);

        JLabel setDFALabel = new JLabel("\u96C6\u5408DFA");
        setDFALabel.setFont(new Font("宋体", Font.PLAIN, 17));
        setDFALabel.setBounds(301, 177, 90, 29);
        framePanel.add(setDFALabel);

        JPanel setDFAPanel = new JPanel();
        setDFAPanel.setBackground(SystemColor.inactiveCaptionBorder);
        setDFAPanel.setBounds(301, 216, 333, 445);
        framePanel.add(setDFAPanel);

        JPanel symbleDFAPanel = new JPanel();
        symbleDFAPanel.setBackground(SystemColor.inactiveCaptionBorder);
        symbleDFAPanel.setBounds(644, 216, 278, 445);
        framePanel.add(symbleDFAPanel);

        JLabel symbleDFALabel = new JLabel("\u5316\u7B80\u540E\u7684DFA");
        symbleDFALabel.setFont(new Font("宋体", Font.PLAIN, 17));
        symbleDFALabel.setBounds(644, 177, 121, 28);
        framePanel.add(symbleDFALabel);

        JPanel resDFAPanel = new JPanel();
        resDFAPanel.setBackground(SystemColor.inactiveCaptionBorder);
        resDFAPanel.setBounds(932, 216, 321, 445);
        framePanel.add(resDFAPanel);

        JLabel resDFALabel = new JLabel("\u6700\u5C0F\u5316DFA");
        resDFALabel.setFont(new Font("宋体", Font.PLAIN, 17));
        resDFALabel.setBounds(932, 177, 95, 29);
        framePanel.add(resDFALabel);
    }
}
