import ControlClass

class SlideBar(ControlClass.Control):
    def __init__(self, minnum, maxnum, minpos, maxpos, initnum=-1):
        super().__init__(((min(minpos[0],maxpos[0]),
                           min(minpos[1],maxpos[1]-5)),
                          (max(minpos[0],maxpos[0]),
                           max(minpos[1],maxpos[1])+5)))
        self.maxnum = maxnum
        self.minnum = minnum
        self.maxpos = maxpos
        self.minpos = minpos
        if initnum == -1:
            self.num = (minnum + maxnum) // 2
            self.pos = ((minpos[0] + maxpos[0]) // 2,
                        (minpos[1] + maxpos[1]) // 2)
        else:
            if initnum < minnum:
               initnum = minnum
            elif initnum > maxnum:
                initnum = maxnum
            self.num = initnum
            self.UpdateNumber(self.num)

    def UpdateNumber(self, pos):
        if pos[0] <= self.minpos[0]:
            self.num = self.minnum
        elif pos[0] >= self.maxpos[0]:
            self.num = self.maxnum
        else:
            if self.maxpos[0] == self.minpos[0]:
                self.num = self.minnum
            else:
                self.num = int((pos[0] - self.minpos[0]) / (self.maxpos[0] - self.minpos[0]) \
                    * (self.maxnum - self.minnum)) + self.minnum
        self.UpdatePosition(self.num)

    def UpdatePosition(self, num):
        self.pos = (int((num - self.minnum) / (self.maxnum - self.minnum) \
                    * (self.maxpos[0] - self.minpos[0])) + self.minpos[0],
                    int((num - self.minnum) / (self.maxnum - self.minnum) \
                    * (self.maxpos[1] - self.minpos[1])) + self.minpos[1])
