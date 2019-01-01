def getReduce(productionSet,firstPro,tset,table,i):
    for r in productionSet:
        if productionSet[r][0]==firstPro.left and productionSet[r][1]==firstPro.right:
            if r==0:
                table[i+1][len(tset)]="ACC"
            else:
                col=1
                while col <=len(tset):
                    if table[i+1][col]!="":
                        raise RuntimeError("存在冲突，不能进行分析表生成")
                    table[i+1][col]="r"+str(r)
                    col+=1
                break
def getshift(currentstatus,head,table,i):
    for j in currentstatus.line:
        val=j.tranval
        nextid=j.next.static_id
        if val!="ε":
            index=head.index(val)
            table[i+1][index]="s"+str(nextid)
def getTable2(resultSet,tset,nset,productionSet):
    head=["status"]
    for i in tset:
        if i=='ε':
            continue
        head.append(i)
    head.append("$")
    for i in nset[1:]:
        head.append(i)
    table=[]
    table.append(head)
    for i in resultSet:
        newrow=[i.static_id]
        for j in head[1:]:
            newrow.append("")
        table.append(newrow)
    i=0
    length=len(resultSet)
    while i<length:
        currentstatus=resultSet[i]
        Set=currentstatus.productionSet
        firstPro=currentstatus.productionSet[0]
        HaveNull=False
        lefttemp=""
        for pro in Set:
            if pro.right[0]=="ε":
                HaveNull=True
                lefttemp=pro.left
            elif pro.index==pro.maxindex:
                getReduce(productionSet,pro,tset,table,i)
            else:
                getshift(currentstatus,head,table,i)
        # 这是一条完成式，就要使用相应的产生式进行规约
        if HaveNull:
            for r in productionSet:
                if productionSet[r][0] == lefttemp and productionSet[r][1][0] =="ε" :
                    if r == 0:
                        table[i + 1][len(tset)] = "ACC"
                        break
                    else:
                        col = 1
                        while col <= len(tset):
                            if table[i + 1][col] != "":
                                if table[i + 1][col][0] == "r":
                                    raise RuntimeError("存在规约的冲突，不能生成分析表：")
                                col += 1
                                continue
                            table[i + 1][col] = "r" + str(r)
                            col += 1
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