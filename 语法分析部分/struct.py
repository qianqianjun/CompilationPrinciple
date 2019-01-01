class label(object):
    def __init__(self,val,right):
        self.value=val
        self.right=right
    def op(self):
        return self.value[0]
class Item(object):
    def __init__(self,val,sets):
        #指示当前点的位置：
        self.index=0
        #指示状态中的产生式中的左边的非终结符。
        self.left=val
        #list[str] 一个字符串的列表：
        self.right=sets
        self.maxindex=len(self.right)
    #修改当前点的位置的函数，新建状态的时候会用到：
    def setIndex(self,ind):
        self.index=ind
    def equals(self,item):
        if item.left==self.left and item.index==self.index and len(item.right)==len(self.right):
            length=len(item.right)
            i=0
            while i<length:
                if item.right[i]!=self.right[i]:
                    return False
                i+=1
            return True
        return False
class Status(object):
    id=0
    def __init__(self):
        #line
        self.line=[]
        #Item
        self.productionSet=[]
        self.static_id=0
    def initid(self):
        self.static_id=Status.id
        Status.id += 1
    def addline(self,singleline):
        for l in self.line:
            if l.tranval==singleline.tranval and l.next.static_id==singleline.next.static_id:
                return False
        self.line.append(singleline)
        return True
    def addProduction(self,production):
        self.productionSet.append(production)
    def setStatusid(self,ids):
        self.static_id=ids
    def isendStatus(self):
        if len(self.productionSet)!=1:
            return False
        else:
            if self.productionSet[0].index==self.productionSet[0].maxindex:
                return True
        return False
class Line(object):
    def __init__(self,tranval,next):
        self.next=next
        self.tranval=tranval