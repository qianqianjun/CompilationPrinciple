package main;

import java.io.*;
import java.util.*;

public class Test {
    public static void main(String[] args)
    {
        Scanner s=new Scanner(new BufferedInputStream(System.in));
        TreeSet<String> arr=new TreeSet<String>();
        for(Integer i=0;i<10;i++)
        {
            arr.add("0".toString());
        }
        for(int i=0;i<arr.size();i++)
        {
            Iterator it=arr.iterator();
            while (it.hasNext())
                System.out.println(it.next().toString());
        }
    }
}
