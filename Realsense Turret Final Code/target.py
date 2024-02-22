from polyreg import Point, Points

class Target:
    self.pos = None
    self.uid = None
    self.max_pos = None

    def __init__(self, uid, pos=None, max_pos=None):
        if pos != None and type(pos) == Points:
            self.pos = pos
        elif pos == type(Point):
            self.pos = Points([Point])
        else:
            self.pos = Points([])

        self.max_pos = max_pos
        self.uid = uid

    def pop(self, index=0):
        #removes and returns the first position pos[0] unless index is specified

        if len(self.pos) != 0:
            return self.pos.pop()
        else:
            return None

    def append(self, position):
        self.pos.append(position)


class Targets:
    self.targets = {}
    
    def __init__(self, tar_list):
        for t in tar_list:
            self.targets[t.uid] = t


    def add(self, tar):
        if tar.uid not in self.targets.keys():
            self.targets_l[tar.uid] = tar
    
    def remove(self, uid):
        if tar.uid in self.targets.keys():
            del self.targets[uid]



        

