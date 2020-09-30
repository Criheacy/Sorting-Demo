import copy
import random
import settings
import NumberClass as num
import StepClass as stp
import AnimationClass as anim
import ColorClass as clr
import ShaderClass as sdr
from pygame import rect
from ColorClass import ColorGradiant

class ElementContainer(object):
    def __init__(self, mode, length):
        self.length = length
        self.elementList = []

        self.sortingMethod = ""
        self.sortingStep = []
        self.elementPosition = []
        self.shaderLayer = []
        self.animation = anim.Animation()

        self.selected = None

        self.changesCount = 0
        self.stepCount = 0

        self.running = False
        self.pausing = False
        self.runningTimer = anim.Animation(True)

        if mode == "random":
            for i in range(length):
                random_value = random.randint(settings.random_range[0], settings.random_range[1])
                self.elementList.append(Element(i,random_value,length))
        if mode == "shuffled":
            tempList = []
            for i in range(length):
                tempList.append(((length - i) * settings.random_range[0] + i * settings.random_range[1]) // length)
            for i in range(length - 1):
                pos = random.randint(i + 1, length - 1)
                self.elementList.append(Element(i,tempList[pos],length))
                tempList[pos] = tempList[i]
            self.elementList.append(Element(length - 1,tempList[length - 1],length))
        elif type(mode) == list:
            pass

# ----------------------- Select Operations -------------------------

    def Select(self, index):
        ''' Select element and enlight it '''
        self.Deselect()
        self.selected = index
        self.elementList[index].number.selected = True

    def Deselect(self):
        ''' Deselect all elements '''
        if self.selected != None:
            self.elementList[self.selected].number.selected = False
            self.selected = None

# ---------------------- Input Operations --------------------------

    def Input(self, number, controled=None):
        ''' Control input options '''
        if self.selected == None: return
        if controled == -1:  # BackSpace / Delete
            if self.elementList[self.selected].number.preNumber == None \
                    or self.elementList[self.selected].number.preNumber == 0:
                self.elementList[self.selected].number.preNumber = 0
            else:
                self.elementList[self.selected].number.preNumber = \
                    self.elementList[self.selected].number.preNumber // 10
        elif controled == 1:  # Enter
            if self.elementList[self.selected].number.preNumber == None \
                    or self.elementList[self.selected].number.preNumber == 0:
                self.elementList[self.selected].number.preNumber = None
            else:
                self.elementList[self.selected].value = self.elementList[self.selected].number.preNumber
                self.elementList[self.selected].number.number = self.elementList[self.selected].number.preNumber
                self.elementList[self.selected].number.preNumber = None
                self.elementList[self.selected].number.UpdateNumberRect(self.selected, self.length)
            self.Deselect()
        elif controled == -2: # Escape
            self.elementList[self.selected].number.preNumber = None
            self.Deselect()
        elif controled == 2:  # Tab
            if self.elementList[self.selected].number.preNumber == None \
                    or self.elementList[self.selected].number.preNumber == 0:
                self.elementList[self.selected].number.preNumber = None
            else:
                self.elementList[self.selected].value = self.elementList[self.selected].number.preNumber
                self.elementList[self.selected].number.number = self.elementList[self.selected].number.preNumber
                self.elementList[self.selected].number.preNumber = None
                self.elementList[self.selected].number.UpdateNumberRect(self.selected, self.length)
            if self.selected < self.length - 1:
                self.Select(self.selected + 1)
            else:
                self.Deselect()

        else:
            if self.elementList[self.selected].number.preNumber == None:
                self.elementList[self.selected].number.preNumber = 0
            self.elementList[self.selected].number.preNumber = \
                self.elementList[self.selected].number.preNumber * 10 + number

# ---------------------------------------------------------------------

    def CopyList(self):
        ''' Use deepcopy to re-instantiate every subitems in list '''
        self.sortingElementList = copy.deepcopy(self.elementList)
    
# ---------------------- ElementContainer Operation -------------------

    def ExchangeElements(self, firstIndex, secondIndex, delay=1):
        if firstIndex == secondIndex:
            return
        _tempElement = self.sortingElementList[firstIndex]
        self.sortingElementList[firstIndex] = self.sortingElementList[secondIndex]
        self.sortingElementList[secondIndex] = _tempElement
        self.sortingStep.append(stp.Step("exchange", delay, firstIndex, secondIndex))

    def InsertElement(self, fromIndex, toIndex, delay=1):
        if fromIndex == toIndex:
            return
        _tempElement = self.sortingElementList[fromIndex]
        if fromIndex > toIndex:
            for i in range(fromIndex,toIndex,-1):
                self.sortingElementList[i] = self.sortingElementList[i-1]
        elif fromIndex < toIndex:
            for i in range(fromIndex,toIndex):
                self.sortingElementList[i] = self.sortingElementList[i+1]
        self.sortingElementList[toIndex] = _tempElement
        self.sortingStep.append(stp.Step("insert", delay, fromIndex, toIndex))

    def GetElement(self, index, mark=False, delay=0, re_mark=False, re_delay=0):
        if mark:
            self.MarkElement(index, "processing", delay)
            if re_mark:
                self.MarkElement(index, "unsolved", re_delay)
        return self.sortingElementList[index]

    def CompareElements(self, firstIndex, secondIndex, mark=False, delay=0, re_mark=True, re_delay=0):
        result = self.sortingElementList[firstIndex].value - self.sortingElementList[secondIndex].value
        if mark:
            if result < 0:
                self.MarkElement(firstIndex, "smallersign", 0)
                self.MarkElement(secondIndex, "greatersign", delay)
            if result > 0:
                self.MarkElement(firstIndex, "greatersign", 0)
                self.MarkElement(secondIndex, "smallersign", delay)
            if result == 0:
                self.MarkElement(firstIndex, "mediumsign", 0)
                self.MarkElement(secondIndex, "mediumsign", delay)
            if re_mark:
                self.MarkElement(firstIndex, "unsolved", 0)
                self.MarkElement(secondIndex, "unsolved", re_delay)
        return result

    def CompareToBase(self, baseIndex, otherIndex, mark=False, delay=0, re_mark=True, re_delay=0):
        result = self.sortingElementList[otherIndex].value - self.sortingElementList[baseIndex].value
        if mark:
            self.MarkElement(baseIndex, "processing", 0)
            if result < 0:
                self.MarkElement(otherIndex, "smallersign", delay)
            if result > 0:
                self.MarkElement(otherIndex, "greatersign", delay)
            if result == 0:
                self.MarkElement(otherIndex, "mediumsign", delay)
            if re_mark:
                self.MarkElement(otherIndex, "unsolved", 0)
                self.MarkElement(baseIndex, "unsolved", re_delay)
        return result

    def MarkElement(self, index, sign, delay):
        self.sortingStep.append(stp.Step("mark-"+sign, delay, index))

    def CastShader(self, range, delay=0):
        self.sortingStep.append(stp.Step("shader",delay,range[0],range[1]))

    def DecastShader(self, delay=0):
        self.sortingStep.append(stp.Step("deshader",delay))

# --------------------------- Run ElementContainer -----------------------
    def Run(self):
        self.running = True
        self.runningTimer.SetAnimation(0)
        self.changesCount = 0
        self.stepCount = 0

    def Pause(self):
        self.pausing = True
        self.runningTimer.PauseAnimation()

    def Continue(self):
        if self.pausing:
            self.runningTimer.ContinueAnimation()
        self.pausing = False

    def Update(self):
        if not(self.running): return
        self.animation.Flash()
        for i in range(self.length):
            self.elementList[i].number.NumberAnimationUpdate(i,self.length,settings.exchange_animation_mode)
        if not(self.animation.in_animation):
            if len(self.sortingStep) == 0:
                self.running = False
                self.runningTimer.TerminateAnimation()
                return
            elif self.pausing:
                self.runningTimer.PauseAnimation()
            else:
                self.animation.SetAnimation \
                    (settings.global_animation_speed * settings.delay_between_movements
                     * self.sortingStep[0].delay)
                self.PlayNextStep(self.sortingStep[0])
                self.sortingStep.pop(0)
    
    def PlayNextStep(self, step):
        if step.mode == "exchange":
            self.changesCount += 1
            self.stepCount += 1

            deltaPosition = int(((step.params[1] - step.params[0])/self.length) \
                                      * (settings.drawing_area[1][0] - settings.drawing_area[0][0]))
            _tempElement = self.elementList[step.params[0]]
            
            self.elementList[step.params[0]].number.NumberAnimationStart \
                        (settings.global_animation_speed * settings.speedof_exchange_numbers, (deltaPosition,0))
            self.elementList[step.params[1]].number.NumberAnimationStart \
                (settings.global_animation_speed * settings.speedof_exchange_numbers, (-deltaPosition,0))
                
            self.elementList[step.params[0]] = self.elementList[step.params[1]]
            self.elementList[step.params[1]] = _tempElement

        elif step.mode[:4] == "mark":
            self.stepCount += 1
            self.elementList[step.params[0]].number.mode = step.mode[5:]

        elif step.mode == "insert":
            self.changesCount += 1
            self.stepCount += 1

            deltaPosition = int(((step.params[1] - step.params[0])/self.length) \
                                      * (settings.drawing_area[1][0] - settings.drawing_area[0][0]))
            
            _tempElement = self.elementList[step.params[0]]
            self.elementList[step.params[0]].number.NumberAnimationStart \
                        (settings.global_animation_speed * settings.speedof_exchange_numbers, (deltaPosition,0))
            
            deltaPosition = int((1 / self.length) \
                                * (settings.drawing_area[1][0] - settings.drawing_area[0][0]))
            
            if step.params[0] > step.params[1]:
                for i in range(step.params[0]-1,step.params[1]-1,-1):
                    self.elementList[i].number.NumberAnimationStart \
                        (settings.global_animation_speed * settings.speedof_exchange_numbers, (deltaPosition,0))
                    self.elementList[i+1] = self.elementList[i]

            elif step.params[0] < step.params[1]:
                for i in range(step.params[0]+1,step.params[1]+1):
                    self.elementList[i].number.NumberAnimationStart \
                        (settings.global_animation_speed * settings.speedof_exchange_numbers, (-deltaPosition,0))
                    self.elementList[i-1] = self.elementList[i]

            self.elementList[step.params[1]] = _tempElement

        elif step.mode == "shader":
            if settings.use_shader:
                self.shaderLayer.append(sdr.Shader(step.params[0], step.params[1], self.length))

        elif step.mode == "deshader":
            if settings.use_shader:
                if not(self.shaderLayer == []):
                    self.shaderLayer.pop()


class Element(object):
    def __init__(self, index, value, length):
        self.value = value
        self.number = num.Number(value, index, length, settings.use_gradiant_in_numbers_rank,
                                 ColorGradiant((value/settings.random_range[1]), settings.gradiant_color_sign))
        