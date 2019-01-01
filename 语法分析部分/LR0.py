"""
write by 高谦  已经完成

底下注释非常详细，因为我健忘，怕给老师讲的时候自己忘了当初自己咋想的了
"""
from container import *
from struct import *
from public import *
import time
def printGramma(gramma):
    for i in gramma:
        print((i.value,i.right))
    print("-------------------------------")
def cin():
    print("请输入文法，例如：A->a|A b,输入exit结束输入(注意,不同的符号之间要有空格:")
    gramma = []
    while True:
        r = input()
        if r != 'exit':
            r = r.split("->")
            right = []
            for i in r[1].split("|"):
                right.append(i.split())
            temp = label(r[0], right)
            gramma.append(temp)
        else:
            break
    start = gramma[0].value
    right=[]
    right.append([start])
    temp = label(start + "*", right)
    gramma.insert(0, temp)
    print("解析输入文法：")
    printGramma(gramma)
    return (gramma, start)
def getSet(gramma):
    Tset=[]
    Nset=[]
    for i in gramma:
        Nset.append(i.value)
        for j in i.right:
            for k in j:
                if isTerminal(k):
                    Tset.append(k)
    Tset=set(Tset)
    Tset=list(Tset)
    Tset.sort()
    return (Tset,Nset)
def getProductionSet(gramma):
    productionset={}
    i = 0
    # 构造productionSet 集合：
    for row in gramma:
        for production in row.right:
            productionset[i] = [row.value, production]
            i += 1
    return productionset
def PrintProductionSet(productionset):
    print("拓广文法并给产生式编号：")
    for i in productionset:
        print("{:2d}".format(int(i))+" : ",end="")
        print(productionset[i][0]+" -> ",end="")
        res=""
        for elem in productionset[i][1]:
            res+=elem+" "
        print(res)
def checkRepeat(resultSet,productionSet,pro_index,gramma,nset,tset):
    newset = []
    newtemp = []
    #这里有一个坑，注意，产生式可能包括相同的符号，初始的状态可能不是只有一条产生式：
    currentlabel=productionSet[pro_index].right[productionSet[pro_index].index]
    for item in productionSet:
        if item.right[item.index]==currentlabel:
            newitem=Item(item.left,item.right)
            newitem.setIndex(item.index+1)
            newset.append(newitem)
            newtemp.append((newitem.left, newitem.right, newitem.index))
    for i in newset:
        if i.index==i.maxindex:
            continue
        if i.right[i.index] in nset:
            for row in gramma:
                if row.value==i.right[i.index]:
                    for k in row.right:
                        newset.append(Item(row.value, k))
                        newtemp.append((row.value, k, 0))
    m=0
    for i in resultSet:
        oldtemp = []
        for j in i.productionSet:
            oldtemp.append((j.left,j.right,j.index))
        flag=True
        if len(oldtemp)!=len(newtemp):
            flag=False
        else:
            for i in newtemp:
                if i not in oldtemp:
                    flag=False
        if flag:
            return (True,newset,resultSet[m])
        m+=1
    return (False,newset,[])
def getNextStatus(status,tset,nset,gramma,resultSet):
    # 首先判断是不是终止状态：status 的production中只有一个产生式，并且产生式的点在最右端
    # 是终止状态直接返回
    length=len(status.productionSet)
    currentpro=status.productionSet[0]
    if length == 1 and currentpro.index == currentpro.maxindex:
        return
    # 遍历当前状态productionSet中的所有item
    # 根据点的位置创造出下一个状态
    # 用一条边将当前状态和下一个状态连接在一起（边的next指向下一个状态，边的值就是当前index所指的符号的值）
    # 将边添加到当前状态的出边集合中
    # 这里特别需要注意的是判断一下新的状态是不是可能就是当前状态，是的话就别创建了，如果不想stackoverflow的话
    i=0
    plength=len(status.productionSet)
    while i<plength:
        if status.productionSet[i].right[status.productionSet[i].index]=='ε':
            i+=1
            continue
        isrepeat,newset,nextstatus=checkRepeat(resultSet,status.productionSet,i,gramma,nset,tset)
        #如果不是重复的话：
        if not isrepeat:
            #创建新的状态：
            newstatus=Status()
            newstatus.productionSet=newset
            newstatus.initid()
            #添加到最终的结果集合
            resultSet.append(newstatus)
            #创建指向新状态的边：
            L1=Line(status.productionSet[i].right[status.productionSet[i].index],newstatus)
            # status.line.append(L1)
            status.addline(L1)
            getNextStatus(newstatus,tset,nset,gramma,resultSet)
        else:
            #如果是一个终结符号：
            if status.productionSet[i].right[status.productionSet[i].index] in tset:
                L1=Line(status.productionSet[i].right[status.productionSet[i].index],nextstatus)
                # status.line.append(L1)
                status.addline(L1)
            else:
            # 如果是一个非终结符号：
            # 创建指向自己的一个边：
                L1=Line(status.productionSet[i].right[status.productionSet[i].index],nextstatus)
                # status.line.append(L1)
                status.addline(L1)
        i+=1
def getDFA(productionset,tset,nset,gramma):
    start=Status()
    start.productionSet.append(Item(productionset[0][0],productionset[0][1]))
    #创造开始状态的所有产生式：
    for i in start.productionSet:  #遍历item
        if i.right[i.index] in nset:
            #修复了产生式不断添加到productionSet 的bug，防止电脑蓝屏：
            godown=True
            for temp in start.productionSet:
                if temp.left==i.right[i.index]:
                    godown=False
            if not godown:
                continue
            for row in gramma:
                if row.value==i.right[i.index]:
                    for k in row.right:
                        start.productionSet.append(Item(row.value,k))
    start.initid()
    resultSet=[]
    resultSet.append(start)
    getNextStatus(start,tset,nset,gramma,resultSet)
    print("识别文法活前缀的DFA状态集合：")
    print("———————————————————————————————")
    for i in resultSet:
        print("状态id："+str(i.static_id))
        print("状态产生式集合以及点所处的位置")
        for j in i.productionSet:
            print((j.left,j.right,j.index))
        print("状态的出边和所指向的状态标号")
        for k in i.line:
            print((k.tranval,k.next.static_id))
        print("---------------------------")
    return (resultSet,start)
def PrintTable(table):
    print("分析表如下：")
    width=10
    print(("-"*width+"+")*len(table[0]))
    for i in table:
        for j in i:
            print("{:^10s}|".format(str(j)),end="")
        print()
        print(("-"*width+"+")*len(table[0]))
def getreduce2(productionSet,table,row,pro):
    if row==2:
        if table[row][table[0].index("$")]!="":
            time.sleep(1)
            PrintTable(table)
            exit("存在冲突")
        else:
            table[row][table[0].index("$")]="ACC"
        return
    index=-1
    for j in range(len(productionSet)):
        if productionSet[j][0]==pro.left and productionSet[j][1]==pro.right:
            index=j
    for i in range(1,len(table[row])):
        if table[row][i]!="":
            table[row][i]=str(table[row][i])+"/reduce"+str(index)
            PrintTable(table)
            time.sleep(1)
            exit("存在冲突，程序停止运行！")
    for i in range(1,table[0].index("$")+1):
        table[row][i]="r"+str(index)
def getshift2(status,table,row,index):
    val=status.line[index].tranval
    nextid=status.line[index].next.static_id
    if table[row][table[0].index(val)]!="":
        table[row][table[0].index(val)]=str(table[row][table[0].index(val)])+"/s"+str(nextid)
        PrintTable(table)
        time.sleep(1)
        exit("存在冲突，程序停止！")
    else:
        table[row][table[0].index(val)]="s"+str(nextid)
def getTable(resultSet,tset,nset,productionSet):
    head = ["status"]
    for i in tset:
        if i == 'ε':
            continue
        head.append(i)
    head.append("$")
    for i in nset[1:]:
        head.append(i)
    table = []
    table.append(head)
    for i in resultSet:
        newrow = [i.static_id]
        for j in head[1:]:
            newrow.append("")
        table.append(newrow)
    # 遍历所有的状态
    row=1
    for status in resultSet:
        for index in range(len(status.line)):
            getshift2(status, table, row, index)
        for pro in status.productionSet:
            if pro.index==pro.maxindex or pro.right[0]=="ε":
                getreduce2(productionSet,table,row,pro)
        row+=1
    PrintTable(table)
    return table

def Parsing(productionset,table):
    start=productionset[0][0]
    while True:
        parStack = stack()
        inputstring = queue()
        cin=input("请输入要进行分析的字符串: \n")
        if cin=='exit':
            break
        cin=cin.split()
        for i in cin:
            inputstring.push(i)
        inputstring.push("$")
        parStack.push("$")
        parStack.push("s0")
        isaccept=True
        #开始进行分析:
        # print(start)
        print("开始分析：")
        print("-----------------------------")
        while parStack.peek()!=start and parStack.size()>1:
            #获得当前状态的标号：
            row=int(parStack.peek()[1:])
            currentlabel=inputstring.front()
            print("分析栈：",end="")
            for i in parStack.datalist:
                print(i,end=" ")
            print()
            print("输入队列：",end="")
            for i in inputstring.datalist:
                print(i,end=" ")
            print()
            print("动作：",end="")
            column = table[0].index(currentlabel)
            op = table[row + 1][column]
            oper=op
            if op!="":
                oper = op[0:1]
                if oper=="s":
                    parStack.push(currentlabel)
                    parStack.push("s" + op[1:])
                    inputstring.pop()
                    print("shift")
                    print("-----------------------------------")
                else:
                    #print("进行规约操作")
                    print("reduce: ", end="")
                    reduceindex=0
                    if op !='ACC':
                        reduceindex=int(op[1:])
                    print(productionset[reduceindex][0],end="->")
                    for item in productionset[reduceindex][1]:
                        print(item,end="")
                    print()
                    if productionset[reduceindex][1][0]!="ε":
                        loop=len(productionset[reduceindex][1])*2
                        for l in range(loop):
                            parStack.pop()
                    # 要新加入分析栈中的非终结符号：
                    currentelem = productionset[reduceindex][0]
                    # 该非终结符号所在分析表的列数：
                    # 修复了输入队列子串是可以接受的串导致后面无法进行分析的错误
                    if currentelem == start and inputstring.size() == 1:
                        # 可以判断为接受
                        break
                    if currentelem == start:
                        continue
                    column = table[0].index(currentelem)
                    # 获取当前分析栈顶的状态标号：
                    currentrow = int(parStack.peek()[1:])
                    nextstatus = table[currentrow + 1][column]
                    parStack.push(currentelem)
                    parStack.push(nextstatus)
                    print("-----------------------------------")
            else:
                print("op 异常:分析表中这个位置是空的")
                isaccept = False
                break
        if isaccept:
            print("-----------------------------------")
            print("分析栈：", end="")
            for i in parStack.datalist:
                print(i, end=" ")
            print()
            print("输入队列：", end="")
            for i in inputstring.datalist:
                print(i, end=" ")
            print()
            print("动作：接受")
            print("-----------------------------------")
        else:
            print("不可以接受！")

def main():
    gramma,start=cin()
    productionSet=getProductionSet(gramma)
    tset,nset=getSet(gramma)
    if "ε" not in tset:
        tset.append("ε")
    resultSet, start =getDFA(productionSet,tset,nset,gramma)
    PrintProductionSet(productionSet)
    table=getTable(resultSet,tset,nset,productionSet)
    Parsing(productionSet,table)
if __name__ == '__main__':
    main()

# S->a A
# A->c A|d
# exit

# S->a A|b B
# A->c A|d
# B->c B|d
# exit

# S->A|B
# A->a A b|c
# B->a B d|d
# exit

# S->( S ) S|ε
# exit