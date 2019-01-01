"""
write by 高谦  已完成
"""
from container import *
from public import *
from struct import *
import time
def cin():
    print("请输入文法，例如：A->a|A b,输入exit结束输入(注意,不同的符号之间要有空格:")
    gramma=[]
    while True:
        r=input()
        if r!='exit':
            r=r.split("->")
            right=[]
            for i in r[1].split("|"):
                right.append(i.split())
            temp=label(r[0],right)
            gramma.append(temp)
        else:
            break
    start=gramma[0].value
    print("解析输入文法：")
    printGramma(gramma)
    return (gramma,start)
def printGramma(gramma):
    for i in gramma:
        print((i.value,i.right))
    print("-------------------------------")
def RemoveLeftRecursion(gramma):
    print("消除左递归：")
    i=0
    length=len(gramma)
    while i<length:
        j=0
        while j<i:
            k =0
            current=gramma[i].right
            productionlen=len(current)
            newright=[]
            while k<productionlen:
                if current[k][0]==gramma[j].value:
                    for sub in gramma[j].right:
                        newright.append(sub+current[k][1:])
                else:
                    newright.append(current[k])
                k+=1
            gramma[i].right=newright
            j+=1
        a=[]
        b=[]
        for production in gramma[i].right:
            if production[0]==gramma[i].value:
                a.append(production)
            else:
                b.append(production)
        # 存在左递归
        if len(a)!=0:
            for temp in b:
                temp.append(gramma[i].value+'~')
            for temp in a:
                temp.remove(gramma[i].value)
                temp.append(gramma[i].value+'~')
            a.append(["ε"])
            newlabel=label(gramma[i].value+'~',a)
            gramma[i].right=b
            gramma.append(newlabel)
        i+=1
    gramma.sort(key=label.op)
    printGramma(gramma)
    return gramma
def judge(L,sub):
    val=L[0]
    length=len(L)
    if length==1:
        return False
    for i in L:
        if i[0:sub+1]!=val[0:sub+1]:
            return False
    return True
def RemoveLeftFactor(gramma):
    print("提取左因子：")
    rownum=0
    length=len(gramma)
    for row in gramma:
        if rownum>=length:
            break
        minlen=len(row.right[0])
        for i in row.right:
            if len(i)<minlen:
                minlen=len(i)
        ml=0
        while ml<minlen:
            if not judge(row.right,ml):
                break
            ml+=1
        if ml!=0:
            substr=row.right[0][0:ml]
            newright=[substr+[row.value+'^']]
            newelemright=[]
            for right in row.right:
                if len(right[ml:])==0:
                    newelemright.append(["ε"])
                else:
                    newelemright.append(right[ml:])
            gramma.append(label(row.value+'^',newelemright))
            gramma[rownum].right=newright
        rownum+=1
    printGramma(gramma)
    return gramma
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
def ExceptNull(arr):
    res=[]
    elem="ε"
    contain=False
    for i in arr:
        if i!=elem:
            res.append(i)
        else:
            contain=True
    return (res,contain)
def add(arr,lists):
    change=False
    for i in lists:
        if i not in arr:
            arr.append(i)
            change=True
    return arr,change
def printFirst(First,Nset):
    for i in First:
        if i in Nset:
            print(i, end=" : ")
            print(First[i])
def getFirst(gramma,tset,nset):
    print("获取First集合")
    First={}
    for i in tset:
        First[i]=[i]
    for i in nset:
        First[i]=[]
    loop=True
    while True:
        if not loop:
            break
        loop = False
        for Nlabel in gramma:
            for production in Nlabel.right:
                Continue=True
                n=len(production)
                labelindex=0
                while Continue and labelindex<n:
                    if len(First[production[labelindex]])==0:
                        Continue=False
                    else:
                        res,Continue=ExceptNull(First[production[labelindex]])
                        First[Nlabel.value],ischange=add(First[Nlabel.value],res)
                        if ischange:
                            loop=True
                    labelindex+=1
                if Continue:
                    First[Nlabel.value],ischange=add(First[Nlabel.value],["ε"])
        if not loop:
            continue
        for i in First:
            print(i,end=" : ")
            print(First[i])
        print("+++++++++++++++++++++++++++++++++")
    printFirst(First,nset)
    print("-------------------------------------")
    return First
def getFollow(gramma,tset,nset,First,start):
    print("得到Follow集合")
    Follow={}
    #初始化Follow集合：
    for i in nset:
        if i==start:
            Follow[i]=['$']
        else:
            Follow[i]=[]
    loop=True
    while True:
        if not loop:
            break
        loop=False
        for i in nset:
            for row in gramma:
                right=row.right
                for production in right:
                    labelindex=0
                    length=len(production)
                    while labelindex <length:
                        if production[labelindex]==i:
                            if labelindex==length-1:
                                # print("将产生式左端的follow集合添加到i的follow集合")
                                Follow[i],ischange=add(Follow[i],Follow[row.value])
                                if ischange:
                                    loop=True
                            else:
                                # print("将labelindex+1 的First集合减去空 添加到i 的follow集合：")
                                res,contain=ExceptNull(First[production[labelindex+1]])
                                Follow[i],ischange=add(Follow[i],res)
                                if ischange:
                                    loop=True
                                if labelindex+1==length-1 and contain:
                                    # print("将产生式左端的follow集合添加到i 的follow集合")
                                    Follow[i], ischange = add(Follow[i], Follow[row.value])
                                    if ischange:
                                        loop=True
                        labelindex+=1
    for i in Follow:
        print(i,end=" : ")
        print(Follow[i])
    print("-----------------------------------")
    return Follow
def PrintTable(table):
    print("分析表如下：")
    width=10
    print(("-"*width+"+")*len(table[0]))
    for i in table:
        for j in i:
            print("{:^10s}|".format(str(j)),end="")
        print()
        print(("-"*width+"+")*len(table[0]))
def PrintProductionSet(productionset):
    print("产生式集合编号如下所示：")
    for i in productionset:
        print("{:2d}".format(int(i))+" : ",end="")
        print(productionset[i][0]+" -> ",end="")
        res=""
        for elem in productionset[i][1]:
            res+=elem+" "
        print(res)
def getTable(follow,first,gramma,nset,tset):
    table=[]
    head=["M[N,T]"]
    for i in tset:
        if i !="ε":
            head.append(i)
    head.append("$")
    table.append(head)
    productionSet={}
    i=0
    #构造productionSet 集合：
    for row in gramma:
        for production in row.right:
            productionSet[i]=[row.value,production]
            i+=1
    for i in nset:
        newrow=[i]
        for temp in range(1,len(head)):
            newrow.append("")
        table.append(newrow)
        #遍历first集合：
        for elem in first[i]:
            # content是在表格中填的内容
            content=0
            length=len(productionSet)
            #设置是否找对应的右边是终结符的产生式编号：
            flag=False
            # 遍历所有的产生式
            while content<length:
                #如果产生式的左边和这一行的表头是一样的：
                if productionSet[content][0]==i:
                    #如果产生式右边第一个就是要找的终结符元素：
                    if productionSet[content][1][0]==elem:
                        #如果这个终结符是空串，应该引入Follow集合：
                        if not head.__contains__(elem):
                            flag=True
                            for fo in follow[i]:
                                #这里应该加一个是否不是LL1文法的条件
                                if fo != "ε":
                                    if newrow[head.index(fo)] != "":
                                        newrow[head.index(fo)] += "/" + str(content)
                                        PrintProductionSet(productionSet)
                                        PrintTable(table)
                                        exit("这不是一个LL1文法！")
                                    else:
                                        newrow[head.index(fo)] = str(content)

                        #不是空串的话，说明一下找到了，并把产生式编号填进表格：
                        else:
                            #这里应该判断一下是是不是LL1文法
                            if newrow[head.index(elem)]!="":
                                newrow[head.index(elem)] += "/"+str(content)
                                PrintTable(table)
                                PrintProductionSet(productionSet)
                                exit("这不是一个LL1文法！")
                            newrow[head.index(elem)]=str(content)
                            flag=True
                            #如果没有这个break，默认使用多个候选产生式的第一个产生式：
                            #break
                content+=1
            #如果没有找到匹配的右边是终结符的产生式。
            if not flag:
                content=0
                while content<length:
                    if productionSet[content][0]==i and \
                            productionSet[content][0] in nset and elem!="ε":
                        newrow[head.index(elem)]=str(content)
                        break
                    content+=1
    return (table,productionSet)
def ParsingResult(table,start,productionSet,tset,nset):
    while True:
        cin=input("请输入要匹配的字符串，输入exit结束输入,注意不同的输入要有空格\n")
        if cin=='exit':
            break
        parStack = stack()
        parStack.push("$")
        cin=cin.split()
        inputQue=queue()
        for i in cin:
            inputQue.push(i)
        inputQue.push("$")
        parStack.push(start)
        accept=True
        while parStack.peek()!="$":
            inputstring=inputQue.front()
            top=parStack.peek()
            if top in nset:
                column=table[0].index(inputstring)
                row=0
                i=0
                while i<len(table):
                    if table[i][0]==top:
                        row=i
                        break
                    i+=1
                target=int(table[row][column])
                print("分析栈",end=":")
                for i in parStack.datalist:
                    print(i,end=" ")
                print()
                print("输入队列",end=":")
                for i in inputQue.datalist:
                    print(i,end=" ")
                print()
                print("动作:",end="")
                print(productionSet[target][0],end="->")
                for i in productionSet[target][1]:
                    print(i,end=" ")
                print()
                print("-------------------------------")
                arr = productionSet[target][1]
                parStack.pop()
                for i in reversed(arr):
                    parStack.push(i)
            else:
                if inputstring!=top and top!="ε":
                    print("错误，不匹配！")
                    accept=False
                    break
                else:
                    print("分析栈", end=":")
                    for i in parStack.datalist:
                        print(i, end=" ")
                    print()
                    print("输入队列", end=":")
                    for i in inputQue.datalist:
                        print(i, end=" ")
                    print()
                    print("动作: 匹配")
                    print("-------------------------------")
                    if top=="ε":
                        parStack.pop()
                        continue
                    parStack.pop()
                    inputQue.pop()
                print("-------------------------------")
        if accept:
            print("分析栈", end=":")
            for i in parStack.datalist:
                print(i, end=" ")
            print()
            print("输入队列", end=":")
            for i in inputQue.datalist:
                print(i, end=" ")
            print()
            print("动作: 接受")
            print("-------------------------------")
        else:
            print("*****不能接受********")
def main():
    gramma,start=cin()
    gramma=RemoveLeftRecursion(gramma)
    gramma=RemoveLeftFactor(gramma)
    Tset,Nset=getSet(gramma)
    First=getFirst(gramma,Tset,Nset)
    Follow=getFollow(gramma,Tset,Nset,First,start)
    table,productionSet=getTable(Follow,First,gramma,Nset,Tset)
    PrintProductionSet(productionSet)
    PrintTable(table)
    ParsingResult(table,start,productionSet,Tset,Nset)
if __name__ == '__main__':
    main()

# A->B a|A a|c
# B->B b|A b|d
# exit

# A->a b|a c
# exit

# A->a b c d|a b a c
# B->c d|c d a
# exit

# Expr->Expr Addop Term|Term
# Addop->+|-
# Term->Term Mulop Factor|Factor
# Mulop->*
# Factor->( Expr )|number
# exit

# S->( S ) S|ε
# exit


# from dalao
"""
5
# E->T E'
# E'->+ T E'|ε
# T->F T'
# T'->* F T'|ε
# F->( E )|i
# exit

"""

#7.3
# S->A a|b A c|B c|b B a
# A->d
# B->d

# 7.2
# S->A a|b A c|d c|b d a
# A->d
# exit

# 7.1
# S->E
# E->T|T + E
# T->ε
# exit

# 6.3
# S->A
# A->A b|b B a
# B->a A c|a|a A b
# exit

# 6.2
# S->A a A b|B b B a
# A->ε
# B->ε

# 6.1
# S->S + a T|a T|+ a T
# T->+ a T|+ a
# exit






