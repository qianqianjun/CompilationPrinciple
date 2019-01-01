from LR0 import cin
from LL1 import getFirst
from LL1 import getFollow
from LL1 import getSet
from LR0 import PrintProductionSet
from LR0 import getProductionSet
from LR0 import PrintTable
from struct import Item
from struct import Line
from container import *
class Status(object):
    id=0
    def __init__(self):
        #line
        self.line=[]
        #Item
        self.productionSet=[]
        self.static_id=0
        self.fin_pro=[]
        self.unfin_pro=[]
    def initid(self):
        self.static_id=Status.id
        Status.id += 1
    def addline(self,singleline):
        self.line.append(singleline)
    #判断这个产生式是不是结束的产生式。
    def isendStatus(self):
        if len(self.productionSet)!=1:
            return False
        else:
            if self.productionSet[0].index==self.productionSet[0].maxindex:
                return True
        return False
    #整理当前状态有哪些产生式是完成状态的，有哪些产生式不是完成状态:
    def zip(self):
        for i in self.productionSet:
            if i.index==i.maxindex:
                self.fin_pro.append(i)
            else:
                if i.right[0]!="ε":
                    self.unfin_pro.append(i)
                else:
                    self.fin_pro.append(i)
def contain(arr,elem):
    for i in arr:
        if i.equals(elem):
            return True
    return False
def checkRepeat(resultSet,productionSet,pro_index,gramma,nset,tset):
    newset = []
    newtemp = []
    #这里有一个坑，注意，产生式可能包括相同的符号，初始的状态可能不是只有一条产生式：
    #需要遍历产生式的集合，找到所有点后面是相同终结符号的产生式，将它们加到新的状态集合中
    #不这样做的话会导致生成的DFA可能会成为NFA
    currentlabel=productionSet[pro_index].right[productionSet[pro_index].index]
    for item in productionSet:
        if item.index==item.maxindex:
            continue
        if item.right[item.index]==currentlabel and item.index<item.maxindex:
            newitem=Item(item.left,item.right)
            newitem.setIndex(item.index+1)
            newset.append(newitem)
            newtemp.append((newitem.left, newitem.right, newitem.index))
    #下面的过程继续得到状态的产生式的集合，这里特别需要注意的是要防止循环将一个相同的产生式的左端重复加到集合中导致电脑蓝屏
    #实际上消除左递归可以避免上面的情况。
    for i in newset:
        #如果是一个完成的状态，那么久不用加进去了。
        if i.index==i.maxindex:
            continue
        if i.right[i.index] in nset:
            for row in gramma:
                if row.value==i.right[i.index]:
                    for k in row.right:
                        if not contain(newset,Item(row.value,k)):
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
            for k in newtemp:
                if k not in oldtemp:
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
        #如果当前的产生式是一个完成产生式，就不用再进行新状态的产生了，直接下一步
        if status.productionSet[i].index==status.productionSet[i].maxindex:
            i+=1
            continue
        #如果当前产生式的右端是一个空串，那就不用进行操作了
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
            newstatus.zip()
            #添加到最终的结果集合
            resultSet.append(newstatus)
            #创建指向新状态的边：
            L1=Line(status.productionSet[i].right[status.productionSet[i].index],newstatus)
            status.line.append(L1)
            getNextStatus(newstatus,tset,nset,gramma,resultSet)
        else:
            #如果是一个终结符号：
            if status.productionSet[i].right[status.productionSet[i].index] in tset:
                L1=Line(status.productionSet[i].right[status.productionSet[i].index],nextstatus)
                status.line.append(L1)
            else:
            # 如果是一个非终结符号：
            #如果当前的状态出边集合中没有值为此非终结符的边
            # 创建指向自己的一个边：
                flag=True
                for singleline in status.line:
                    if singleline.tranval==status.productionSet[i].right[status.productionSet[i].index]:
                        flag=False
                        break
                if flag:
                    L1=Line(status.productionSet[i].right[status.productionSet[i].index],nextstatus)
                    status.line.append(L1)
        i+=1
def getDFA(productionset,tset,nset,gramma):
    start=Status()
    start.productionSet.append(Item(productionset[0][0],productionset[0][1]))
    #创造开始状态的所有产生式：
    for i in start.productionSet:  #遍历item
        if i.right[i.index] in nset:
            for row in gramma:
                if row.value==i.right[i.index]:
                    for k in row.right:
                        if not contain(start.productionSet,Item(row.value,k)):
                            start.productionSet.append(Item(row.value,k))
    start.initid()
    start.zip()
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
def getTable(resultSet,tset,nset,productionSet,follow):
    #初始化表头：
    head=["status"]
    for i in tset:
        if i=='ε':
            continue
        head.append(i)
    head.append("$")
    for i in nset[1:]:
        head.append(i)
    #建立一个新表：
    table=[]
    table.append(head)
    for i in resultSet:
        newrow=[i.static_id]
        for j in head[1:]:
            newrow.append("")
        table.append(newrow)
    #开始在表中填内容：
    i=0
    length=len(resultSet)
    while i<length:
        currentstatus=resultSet[i]
        Set=currentstatus.productionSet
        firstPro=Set[0]
        #如果当前状态产生式的左端有多个产生式，则要具体区分两种情况：
        #1.没有完成项，只有未完成项，也就是点的位置没有到最后的项
        #2.有完成项和未完成项，贼烦，要考虑有没有移进和规约的冲突，还要考虑所有完成式之间有没有规约冲突
        #详见ppt3.2   32页
        if len(Set) !=1:
            if len(currentstatus.fin_pro) ==0:
                #没有完成项目：直接shift就好，不会有冲突：
                for j in currentstatus.line:
                    val=j.tranval
                    nextid=j.next.static_id
                    index=head.index(val)
                    table[i+1][index]="s"+str(nextid)
            else:
                #检查是不是有移进和规约的冲突:
                for ufin in currentstatus.unfin_pro:
                    if ufin.right[ufin.index] in tset:
                        for fin in currentstatus.fin_pro:
                            if ufin.right[ufin.index] in follow[fin.left]:
                                raise RuntimeError("存在移进和规约的冲突，程序正常停止")
                #检查是不是有规约的冲突：
                w=0
                n=0
                while w<len(currentstatus.fin_pro):
                    while n<len(currentstatus.fin_pro):
                        if w==n:
                            n+=1
                            continue
                        else:
                            for elem in follow[currentstatus.fin_pro[w].left]:
                                if elem in follow[currentstatus.fin_pro[n].left]:
                                    raise RuntimeError("存在规约的冲突，两个完成式左端非终结符的follow集合有交集！")
                        n+=1
                    w+=1
                #程序运行到这里，说明没有移进和规约的冲突，也没有规约的冲突,可以开始填表了：
                for fin in currentstatus.fin_pro:
                    for r in productionSet:
                        if productionSet[r][0]==fin.left and productionSet[r][1]==fin.right:
                            if r == 0:
                                table[i + 1][len(tset)] = "ACC"
                            else:
                                col=1
                                while col<=len(tset):
                                    if head[col] in follow[fin.left]:
                                        table[i+1][col]="r"+str(r)
                                    col+=1
                            break
                #shift操作：
                for j in currentstatus.line:
                    val = j.tranval
                    nextid = j.next.static_id
                    index = head.index(val)
                    table[i + 1][index] = "s" + str(nextid)
        #如果一个状态只包含一个产生式
        else:
            if firstPro.index!=firstPro.maxindex:
                #如果产生式的右端不是空的，那么就说明要进行移进的操作了。
                if firstPro.right[0]!="ε":
                    for j in currentstatus.line:
                        val=j.tranval
                        nextid=j.next.static_id
                        index=head.index(val)
                        table[i+1][index]="s"+str(nextid)
                #否则要进行的操作是进行规约操作:
                else:
                    for r in productionSet:
                        # 找到对应的状态的id ，r就是id ，这里要注意的是当r=0的时候是开始状态，应该把ACC填到这一行的
                        #  $ 符号对应的位置上。
                        # print(productionSet[r])
                        if productionSet[r][0] == firstPro.left and productionSet[r][1] == firstPro.right:
                            if r == 0:
                                table[i + 1][len(tset)] = "ACC"
                            else:
                                col = 1
                                while col <= len(tset):
                                    # 在当前产生式的左端的follow集合中填入这个规约条件：
                                    if head[col] in follow[firstPro.left]:
                                        table[i + 1][col] = "r" + str(r)
                                    col += 1
                            break
            # 这个产生式一定是一个完成产生式，只能进行规约操作
            # 根据Follow集合填表，不再和LR0算法一样，暴力全填上。
            else:
                for r in productionSet:
                    #找到对应的状态的id ，r就是id ，这里要注意的是当r=0的时候是开始状态，应该把ACC填到这一行的
                    #  $ 符号对应的位置上。
                    # print(productionSet[r])
                    if productionSet[r][0]==firstPro.left and productionSet[r][1]==firstPro.right:
                        if r==0:
                            table[i+1][len(tset)]="ACC"
                        else:
                            col=1
                            while col <=len(tset):
                                #在当前产生式的左端的follow集合中填入这个规约条件：
                                if head[col] in follow[firstPro.left]:
                                    table[i+1][col]="r"+str(r)
                                col+=1
                        break
        i+=1
    PrintTable(table)
    return table
def Parsing(resultset,tset,nset,productionset,table):
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
    tset,nset=getSet(gramma)
    if "ε" not in tset:
        tset.append("ε")
    First=getFirst(gramma,tset,nset)
    Follow=getFollow(gramma,tset,nset,First,start)
    productionSet=getProductionSet(gramma)
    resultSet,start= getDFA(productionSet, tset, nset, gramma)
    PrintProductionSet(productionSet)
    table=getTable(resultSet,tset,nset,productionSet,Follow)
    Parsing(resultSet,tset,nset,productionSet,table)
if __name__ == '__main__':
    main()

# E->E + T|T
# T->T * F|F
# F->( E )|id
# exit

# E->E + n|n
# exit

# S->( S ) S|ε
# exit

