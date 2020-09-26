import math
import settings
import ControlClass
import AnimationClass as anim
import ColorClass as colr
from pygame import rect

class Number(ControlClass.Control):
    def __init__(self, number, index, length, use_custom_color=False, customColor=(0,0,0)):
        if use_custom_color:
            self.mode = "custom"
        else:
            self.mode = "unsolved"
        self.selected = False
        self.number = number
        self.preNumber = None
        self.customColor = customColor
        self.starting_pos = rect.Rect(0, 0, 0, 0)
        self.destination = rect.Rect(0, 0, 0, 0)
        self.animation = anim.Animation()
        self.colorAnimation = None
        self.UpdateNumberRect(index, length)

    def UpdateNumberRect(self, index, length):
        self.rect = rect.Rect(settings.drawing_area[0][0]+int(((index)/length) *
                                (settings.drawing_area[1][0]-settings.drawing_area[0][0])),
                            settings.drawing_area[1][1]-int((self.number/settings.random_range[1]) *
                                (settings.drawing_area[1][1]-settings.drawing_area[0][1])),
                            int((settings.drawing_area[1][0]-settings.drawing_area[0][0])/length)-settings.numbers_gap,
                            int((self.number/settings.random_range[1]) *
                                (settings.drawing_area[1][1]-settings.drawing_area[0][1])))
        

    def NumberAnimationStart(self, animation_time, deltaPos):
        self.starting_pos = self.rect
        _tempRect = self.rect.copy()
        _tempRect.center = (_tempRect.center[0]+deltaPos[0], _tempRect.center[1]+deltaPos[1])
        self.destination = _tempRect
        self.animation.SetAnimation(animation_time)

    def NumberAnimationPause(self):
        if not(self.animation.in_animation): return
        self.animation.PauseAnimation()

    def NumberAnimationContinue(self):
        if not(self.animation.in_animation): return
        self.animation.ContinueAnimation()

    def NumberAnimationUpdate(self, index, length, accel_mode=0):
        if not(self.animation.in_animation): return
        animation_rate = self.animation.Flash(accel_mode)
        if animation_rate == 1.0:
            self.UpdateNumberRect(index, length)
            return
        self.rect = rect.Rect(int(self.starting_pos.left * (1-animation_rate) + self.destination.left * animation_rate),
                              int(self.starting_pos.top * (1-animation_rate) + self.destination.top * animation_rate),
                              int(self.starting_pos.width * (1-animation_rate) + self.destination.width * animation_rate),
                              int(self.starting_pos.height * (1-animation_rate) + self.destination.height * animation_rate))
        