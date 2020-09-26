from pygame import rect
import settings
import ControlClass

class Shader(ControlClass.Control):

    def __init__(self, rangel, ranger, length):
        self.range = (rangel, ranger)
        
        _tempRect = rect.Rect(settings.drawing_area[0][0]+int(((rangel)/length) *
                                  (settings.drawing_area[1][0]-settings.drawing_area[0][0])) - settings.numbers_gap,
                              settings.drawing_area[0][1],
                              int((settings.drawing_area[1][0] - settings.drawing_area[0][0])/length) *
                                  (ranger - rangel + 1),
                              (settings.drawing_area[1][1]-settings.drawing_area[0][1]))
        super().__init__(_tempRect)
