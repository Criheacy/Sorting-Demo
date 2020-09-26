import ControlClass

class ButtonClass(ControlClass.Control):
    """description of class"""
    def __init__(self, rect, text=""):
        self.text = text
        self.centerPos = ((rect[0][0]+rect[1][0])//2, (rect[0][1]+rect[1][1])//2)
        super().__init__(rect)

