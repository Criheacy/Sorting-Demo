from pygame import rect as rectangle

class Control(object):
    """description of class"""
    def __init__(self, rect):
        self.rect = rect

    def InControlCheck(self, pos):
        if type(self.rect) == rectangle.Rect:
            return self.rect.collidepoint(pos)
        if pos[0] >= self.rect[0][0] and pos[0] <= self.rect[1][0] and \
           pos[1] >= self.rect[0][1] and pos[1] <= self.rect[1][1]:
            return True
        return False