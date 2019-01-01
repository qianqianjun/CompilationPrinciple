class stack(object):
    def __init__(self):
        self.datalist=[]
    def push(self,elem):
        self.datalist.append(elem)
    def pop(self):
        if len(self.datalist)==0:
            raise RuntimeError("大哥，栈是空的！")
        else:
            temp=self.datalist[len(self.datalist)-1]
            self.datalist.pop()
            return temp
    def size(self):
        return len(self.datalist)
    def empty(self):
        if len(self.datalist)==0:
            return True
        else:
            return False
    def peek(self):
        if len(self.datalist)!=0:
            return self.datalist[len(self.datalist)-1]
        else:
            raise RuntimeError("大哥，栈是空的，取个毛啊！")
class queue(object):
    def __init__(self):
        self.datalist=[]
    def push(self,elem):
        self.datalist.append(elem)
    def pop(self):
        if len(self.datalist)==0:
            raise RuntimeError("大哥，栈是空的！")
        else:
            temp=self.datalist[0]
            self.datalist=self.datalist[1:]
            return temp
    def front(self):
        if len(self.datalist)==0:
            raise RuntimeError("大哥，栈是空的！")
        else:
            return self.datalist[0]
    def empty(self):
        if len(self.datalist)==0:
            return True
        else:
            return False
    def size(self):
        return len(self.datalist)