from typing import List
from struct import label
from LL1 import cin
from LL1 import getSet
from LL1 import getFirst
from LL1 import printGramma
import time
from LL1 import PrintTable
from container import *
class Line(object):
    def __init__(self,tranval,next):
        self.tranval=tranval
        self.next=next
    def same(self,other):
        return self.tranval==other.tranval and self.next==other.next
class Production(object):
    def __init__(self,left,right,lookahead):
        self.left=left
        self.right=right
        self.index=0
        self.maxindex=len(right)
        self.lookahead=lookahead
        self.prelookahead=[]
    def setindex(self,index):
        self.index=index
    def sameHeartPro(self,other):
        return self.right==other.right and self.index==other.index and self.left==other.left
class Status(object):
    staticnum=0
    def __init__(self):
        self.productionSet=[]
        self.staticid=0
        self.line=[]
        self.infotemp=[]
        self.simpleinfo=[]
    def init_status(self):
        self.staticid=Status.staticnum
        Status.staticnum+=1
    def add(self,production):
        temp=(production.left,production.right,production.index,production.maxindex,sorted(production.lookahead))
        if temp not in self.infotemp:
            self.productionSet.append(production)
            self.infotemp.append((production.left,production.right,production.index,production.maxindex,sorted(production.lookahead)))
            self.simpleinfo.append((production.left,production.right,production.index,production.maxindex))
    def same(self,other)->bool:
        #如果两个状态的产生式集合的长度都不一样的话，可以直接判定两个状态不可能相同
        if len(self.productionSet)!=len(other.productionSet):
            return False
        #遍历两个状态的产生式的集合，只有其中一个集合中的产生式另外一个集合中没有，则可以认定两个状态不相同
        for i in self.infotemp:
            if i not in other.infotemp:
                return False
        return True
    def sameHeart(self,other):
        for i in self.simpleinfo:
            if i not in other.simpleinfo:
                return False
        for i in other.simpleinfo:
            if i not in self.simpleinfo:
                return False
        return True
    def addline(self,line):
        for i in self.line:
            if i.same(line):
                return False
        self.line.append(line)
        return True
    def getStringFirst(self,pro,first):
        Continue=True
        index=pro.index+1
        maxindex=pro.maxindex
        res=[]
        flag=True
        while Continue and index<maxindex:
            Continue=False
            if 'ε' in first[pro.right[index]]:
                Continue=True
            if 'ε' not in first[pro.right[index]]:
                flag=False
            for i in first[pro.right[index]]:
                res.append(i)
            index+=1
        if flag:
            res+=pro.lookahead[0:]
        return res
    def getLookAhead(self,pro,first):
        index=pro.index
        #如果当前终结符后面没有产生的符号，则继承展望符就好：
        if index==pro.maxindex-1:
            return pro.lookahead
        else:
            return self.getStringFirst(pro,first)
    def getClosure(self,proSets,first,nset):
        for i in self.productionSet:
            if i.index==i.maxindex:
                continue
            if i.right[i.index] in nset:
                add=True
                #检查当前的集合中是否已经有了这个产生式：
                for j in self.productionSet:
                    look = self.getLookAhead(i, first)
                    if j.index == 0 and j.left == i.right[i.index] and set(look).issubset(set(j.lookahead)):
                        add = False
                        break
                if add:
                    for item in proSets:
                        if item[0]==i.right[i.index]:
                            lookahead=self.getLookAhead(i,first)
                            self.productionSet.append(Production(item[0],item[1],lookahead))
    def zipline(self):
        L=[]
        res=[]
        for i in self.line:
            temp=(i.tranval,i.next)
            if temp not in res:
                res.append(temp)
                L.append(i)
        self.line=L

def getStringFirst(pro,first):
    Continue=True
    index=pro.index+1
    maxindex=pro.maxindex
    res=[]
    flag=True
    while Continue and index<maxindex:
        Continue=False
        if 'ε' in first[pro.right[index]]:
            Continue=True
        if 'ε' not in first[pro.right[index]]:
            flag=False
        for i in first[pro.right[index]]:
            res.append(i)
        index+=1
    if flag:
        res+=pro.lookahead[0:]
    return res
def out_getLookahead(pro,first):
    index = pro.index
    # 如果当前终结符后面没有产生的符号，则继承展望符就好：
    if index == pro.maxindex - 1:
        return pro.lookahead
    else:
        return getStringFirst(pro, first)
def getNextStatus(resultSet,status,proSet,first,nset):
    Set=status.productionSet
    #遍历所有产生式
    try:
        for i in range(len(Set)):
            #如果这是一个终止产生式，啥也不用做。
            if Set[i].index==Set[i].maxindex or Set[i].right==['ε']:
                continue
            #如果不是终止产生式，则要进行下一个状态的构造：
            tranval=Set[i].right[Set[i].index]
            newstatus=Status()
            newproduction=Production(Set[i].left,Set[i].right,Set[i].lookahead)
            newproduction.setindex(Set[i].index+1)
            newstatus.add(newproduction)
            #查找当前集合中是不是还有其他产生式经过一个相同的符号会转移
            for j in range(len(Set)):
                if i==j:
                    continue
                if Set[j].index==Set[j].maxindex:
                    continue
                if Set[j].right[Set[j].index]!=tranval:
                    continue
                newproduction=Production(Set[j].left,Set[j].right,Set[j].lookahead)
                newproduction.setindex(Set[j].index+1)
                newstatus.add(newproduction)
            #状态得到闭包：
            newstatus.getClosure(proSet,first,nset)
            #假设状态会增加
            add=True
            for s in range(len(resultSet)):
                # if resultSet[s].same(newstatus):
                #     add=False
                #     nextstatus=resultSet[s]
                #     getUnionLook(nextstatus.productionSet,newstatus.productionSet)
                #     line=Line(tranval,nextstatus)
                #     status.addline(line)
                #     break
                if resultSet[s].same(newstatus):
                    add = False
                    nextstatus = resultSet[s]
                    line = Line(tranval, nextstatus)
                    status.addline(line)
            if add:
                newstatus.init_status()
                line=Line(tranval,newstatus)
                status.addline(line)
                resultSet.append(newstatus)
                getNextStatus(resultSet,newstatus,proSet,first,nset)
    except Exception as e:
        exit(str(e))
def getLR1DFA(gramma,first,nset):
    productionset=[]
    for i in gramma:
        for j in i.right:
            productionset.append([i.value,j])
    S=Status()
    S.add(Production(productionset[0][0],productionset[0][1],['$']))
    S.getClosure(productionset,first,nset)
    S.init_status()
    resultSet=[]
    resultSet.append(S)
    getNextStatus(resultSet,S,productionset,first,nset)
    print("识别文法活前缀的LR1 DFA状态集合：")
    print("———————————————————————————————")
    for i in resultSet:
        print("状态id：" + str(i.staticid))
        print("状态产生式集合以及点所处的位置")
        for j in i.productionSet:
            print((j.left, j.right, j.index, j.lookahead))
        print("状态的出边和所指向的状态标号")
        for k in i.line:
            print((k.tranval, k.next.staticid))
        print("---------------------------")
    return (resultSet,productionset)
def getUnionLook(status,Set):
    for i in Set:
        status.add(i)
def fixline(resultSet,c,j):
    delete=resultSet[j]
    for i in range(len(resultSet)):
        fixelem=resultSet[i]
        if fixelem==delete:
            continue
        for l in range(len(fixelem.line)):
            if fixelem.line[l].next==delete:
                fixelem.line[l].next=resultSet[c]
        fixelem.zipline()
def getLALRDFA(resultSet):
    result=[]
    delete =[]
    print("找到的可以合并的同心项如下：")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    for i in range(len(resultSet)):
        if resultSet[i].staticid in delete:
            continue
        for j in range(len(resultSet)):
            if i==j:
                continue
            if resultSet[j].staticid in delete:
                continue
            if resultSet[i].sameHeart(resultSet[j]):
                print((i,j))
                delete.append(resultSet[j].staticid)
                proSet=resultSet[j].productionSet
                getUnionLook(resultSet[i],proSet)
                fixline(resultSet,i,j)
    print("识别文法活前缀的LALR DFA状态集合：")
    print("———————————————————————————————")
    for i in resultSet:
        if i.staticid in delete:
            continue
        result.append(i)
        print("状态id：" + str(i.staticid))
        print("状态产生式集合以及点所处的位置")
        for j in i.productionSet:
            print((j.left, j.right, j.index, j.lookahead))
        print("状态的出边和所指向的状态标号")
        for k in i.line:
            print((k.tranval, k.next.staticid))
        print("---------------------------")
    return result
def getReduceIndex(productionSet,pro):
    for i in range(len(productionSet)):
        if productionSet[i][0]==pro.left and productionSet[i][1]==pro.right:
            return i
def getLR1Table(resultSet,productionSet,tset,nset,start):
    table=[]
    head=[]
    head.append("STATUS")
    if 'ε' not in tset:
        tset.append('ε')
    for i in tset:
        if i!='ε':
            head.append(i)
    head.append("$")
    for i in nset:
        head.append(i)
    table.append(head)
    for i in resultSet:
        temp=[]
        temp.append(i.staticid)
        for j in head[1:]:
            temp.append("")
        table.append(temp)
    for i in range(len(productionSet)):
        print(i,':',productionSet[i][0],"->",productionSet[i][1])
    for i in range(len(resultSet)):
        cStatus=resultSet[i]
        for line in cStatus.line:
            if table[i+1][head.index(line.tranval)]=="":
                table[i+1][head.index(line.tranval)]="s"+str(line.next.staticid)
            else:
                print("存在冲突，请修改文法！")
                table[i + 1][head.index(line.tranval)] += "/s" + str(line.next.staticid)
                PrintTable(table)
                exit(0)
        for pro in cStatus.productionSet:
            if pro.index==pro.maxindex or pro.right==['ε']:
                for look in pro.lookahead:
                    if table[i+1][head.index(look)]!="":
                        print("存在冲突，请修改文法：")
                        table[i + 1][head.index(look)] += "/r" + str(getReduceIndex(productionSet, pro))
                        PrintTable(table)
                        exit(0)
                    table[i+1][head.index(look)]="r"+str(getReduceIndex(productionSet,pro))
    for i in range(len(resultSet)):
        for pro in resultSet[i].productionSet:
            if pro.left==start+"*" and pro.maxindex==pro.index:
                table[i+1][len(tset)]="ACC"
                break
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
        print("开始分析：")
        print("-----------------------------")
        while parStack.peek()!=start and parStack.size()>1:
            #获得当前状态的标号：
            row=int(parStack.peek()[1:])
            for k in range(len(table)):
                if str(table[k][0])==str(row):
                    row=k
                    break
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
            op = table[row][column]
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