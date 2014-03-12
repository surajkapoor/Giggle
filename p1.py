class List(object):
    
    def __init__(self):
        self.l = []
        
class Range(object):
    
    def __init__(self):
        pass
    
    def function(self):
        for i in range(100):
            self.li = List()
            self.li.l.append(i)
        return self.li.l
        
r = Range()
print r.function()            
            
                     