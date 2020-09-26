import time
import math
import StepClass as stp

class Animation():

    def __init__(self, is_internal=False):
        self.in_animation = False
        self.in_pause = False
        self.internal_animation = is_internal
        self.pause_time = 0.0
        self.pause_starting_time_mark = 0.0
        self.animation_total_time = 0.0
        self.animation_now_time = 0.0
        self.animation_starting_time_mark = 0.0
        self.animation_rate = 0.0

    def Accelerate(self, mode=0):
        # mode 0: normal
        if mode == 0:
            self.animation_rate = self.animation_now_time / self.animation_total_time
        # mode 1: accending
        elif mode == 1:
            self.animation_rate = (self.animation_now_time / self.animation_total_time) ** 2
        # mode 2: decending
        elif mode == 2:
            self.animation_rate = - (self.animation_now_time / self.animation_total_time - 1) ** 2 + 1
        # mode 3: accending => decending
        elif mode == 3:
            if self.animation_now_time < self.animation_total_time / 2:
                self.animation_rate = (self.animation_now_time / self.animation_total_time) ** 2 * 2
            else:
                self.animation_rate = (-2) * ((self.animation_now_time / self.animation_total_time - 1) ** 2) + 1
        # mode 4: cliff
        elif mode == 4:
            if self.animation_now_time < self.animation_total_time:
                self.animation_rate = 0.0
            else:
                self.animaiton_rate = 1.0

    def SetAnimation(self, animation_total_time):
        self.in_animation = True
        if self.internal_animation:
            self.animation_total_time = 0.0
            self.internal_animation = True
        else:
            self.animation_total_time = animation_total_time
            self.internal_animation = False
        self.animation_now_time = 0.0
        self.animation_starting_time_mark = time.time()
        self.pause_time = 0.0

    def PauseAnimation(self):
        if not(self.in_animation): return
        if not(self.in_pause):
            self.in_pause = True
            self.pause_starting_time_mark = time.time()

    def ContinueAnimation(self):
        if not(self.in_animation):
            return
        if self.in_pause:
            self.in_pause = False
            self.pause_time += time.time() - self.pause_starting_time_mark

    def TerminateAnimation(self):
        self.animation_now_time = time.time() - self.pause_time - self.animation_starting_time_mark
        self.in_pause = False
        self.in_animation = False
        return self.animation_now_time

    def Flash(self, mode=0):
        if not(self.in_animation): return

        self.animation_now_time = time.time() - self.pause_time - self.animation_starting_time_mark
        if self.internal_animation:
            return self.animation_now_time

        if self.in_pause: return

        if self.animation_now_time >= self.animation_total_time \
                and not(self.internal_animation):
            self.in_animation = False
            return 1.0
        self.Accelerate(mode)
        return self.animation_rate