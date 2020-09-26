import math
import settings
import AnimationClass as anim

def ColorGradiant(mixRate, colors):
    if mixRate <= 0:
        return colors[0]
    elif mixRate >= 1:
        return colors[-1]
    else:
        mixRate *= len(colors) - 1
        _l = colors[math.floor(mixRate)]
        _r = colors[math.ceil(mixRate)]
        mixRate -= math.floor(mixRate)
        return (round(_l[0]* (1-mixRate) + _r[0] * mixRate),
                round(_l[1]* (1-mixRate) + _r[1] * mixRate),
                round(_l[2]* (1-mixRate) + _r[2] * mixRate))

def ColorRenderer(mode):
    if mode == "processing":
        return settings.processing_color
    elif mode == "special":
        return settings.special_color
    elif mode == "smallersign":
        return settings.smallersign_color
    elif mode == "mediumsign":
        return settings.mediumsign_color
    elif mode == "greatersign":
        return settings.greatersign_color
    elif settings.use_gradiant_in_numbers_rank:
        return None
    elif mode == "unsolved":
        return settings.unsolved_color
    elif mode == "finish":
        return settings.finished_color
    elif mode == "finish":
        return settings.mediumsign_color
    elif mode == "error":
        return settings.error_color

class ColorAnimation(object):
    def __init__(self, animation_time, colorList, mode=0):
        self.animation_mode = mode
        self.colorList = colorList
        self.animation = anim.Animation()
        self.animation.SetAnimation(animation_time)

    def ColorAnimationPause(self):
        if not(self.animation.in_animation): return
        self.animation.PauseAnimation()

    def ColorAnimationContinue(self):
        if not(self.animation.in_animation): return
        self.animation.ContinueAnimation()

    def GetColor(self):
        if not(self.animation.in_animation): return
        animation_rate = self.animation.Flash(self.animation_mode)
        return ColorGradiant(animation_rate, self.colorList)

