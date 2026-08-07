class MyStack:
    def __init__(self):
        self.l = []
    
    def push(self, i):
        self.l.append(i)
        
    def pop(self):
        if len(self.l) == 0:
            return None
        else:
            return self.l.pop()
            
    def is_empty(self):
        if len(self.l) == 0:
            return True
        else:
            return False

class H_Table:
    def __init__(self, size=100):
        self.sz = size
        self.t = []
        for i in range(self.sz):
            self.t.append([])
            
    def hashFunc(self, k):
        val = 0
        for c in k:
            val = (val * 31 + ord(c)) % self.sz
        return val
        
    def insert(self, k, v):
        idx = self.hashFunc(k)
        for x in self.t[idx]:
            if x[0] == k:
                x[1] = v
                return
        self.t[idx].append([k, v])
        
    def get(self, k):
        idx = self.hashFunc(k)
        for x in self.t[idx]:
            if x[0] == k:
                return x[1]
        return None
        
    def check_exist(self, k):
        if self.get(k) != None:
            return True
        return False

class maxHeap:
    def __init__(self):
        self.h = []
        
    def insert(self, user, sc):
        flag = False
        for i in range(len(self.h)):
            if self.h[i]["username"] == user:
                self.h[i]["score"] = sc
                self.up(i)
                flag = True
                return
        if flag == False:
            self.h.append({"username": user, "score": sc})
            self.up(len(self.h) - 1)
            
    def up(self, i):
        p = (i - 1) // 2
        if i > 0:
            if self.h[i]["score"] > self.h[p]["score"]:
                temp = self.h[i]
                self.h[i] = self.h[p]
                self.h[p] = temp
                self.up(p)
                
    def get_sorted(self):
        return sorted(self.h, key=lambda x: x["score"], reverse=True)

class graphObj:
    def __init__(self):
        self.nodes = {}
        
    def add(self, u, v, w):
        u = str(u)
        v = str(v)
        if u not in self.nodes:
            self.nodes[u] = []
        if v not in self.nodes:
            self.nodes[v] = []
        self.nodes[u].append((v, w))
        self.nodes[v].append((u, w))
        
    def get_adj(self, u):
        if str(u) in self.nodes:
            return self.nodes[str(u)]
        else:
            return []