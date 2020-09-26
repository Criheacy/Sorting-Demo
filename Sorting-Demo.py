import sys
import getopt
import pygame
from pygame.locals import *

import settings
import SlideBar as sbr
import ButtonClass as btn
import NumberClass as num
import ElementClass as elm
import ColorClass as clr
import Renderer
import SortingAlgorithm

def MainLoop():
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode(settings.display_size)

    numbersBar = sbr.SlideBar(settings.slide_bar_range[0],settings.slide_bar_range[1],(635,85),(755,85))
    spanRandomButton = btn.ButtonClass(((625,220),(775,260)),"Generate")
    sortButton = btn.ButtonClass(((625,280),(775,320)),"")

    sortNameLabel = btn.ButtonClass(((50,345),(200,355)),"")
    sortInformationLabel = btn.ButtonClass(((300,345),(520,355)),"")
    sortTimeLabel = btn.ButtonClass(((600,345),(700,355)),"")
    
    copyrightLabel = btn.ButtonClass(((625, 0), (775, 35)), settings.copyright_str)

    sortMethodIndex = 0
    sortAlgorithms = ["InsertionSort","SelectionSort","BubbleSort",
                      "QuickSort","MergeSort","HeapSort","RadixSort"]

    elementContainer = None
    showNoticeLabel = False

    MOUSEPOS = (0, 0)

    LEFT_PRESSED = False
    LEFT_PRESSING_CONTROL = None

    RIGHT_PRESSED = False
    RIGHT_PRESSING_CONTROL = None

    KEY_PRESSED = None

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0);

    # ---------------------------- MOUSE EVENTS ------------------------
            elif event.type == MOUSEBUTTONDOWN:
                MOUSEPOS = event.pos
                if event.button == 1:
                    LEFT_PRESSED = True
                    if numbersBar.InControlCheck(event.pos):
                        LEFT_PRESSING_CONTROL = "NumbersBar"
                    if spanRandomButton.InControlCheck(event.pos):
                        LEFT_PRESSING_CONTROL = "SpanRandomButton"
                    if sortButton.InControlCheck(event.pos):
                        LEFT_PRESSING_CONTROL = "SortButton"
                    if elementContainer != None:
                        for i in range(elementContainer.length):
                            if elementContainer.elementList[i].number.InControlCheck(event.pos):
                                elementContainer.Input(0, -2)
                                elementContainer.Select(i)
                elif event.button == 3:
                    RIGHT_PRESSED = True
                    if sortButton.InControlCheck(event.pos):
                        RIGHT_PRESSING_CONTROL = "SortButton"
            elif event.type == MOUSEBUTTONUP:
                MOUSEPOS = event.pos  
                if event.button == 1:
                    LEFT_PRESSED = False
                    LEFT_PRESSING_CONTROL = None
                elif event.button == 3:
                    RIGHT_PRESSED = False
                    RIGHT_PRESSING_CONTROL = None
            elif event.type == MOUSEMOTION:
                MOUSEPOS = event.pos
            
    # --------------------------- KEY EVENTS ------------------------------

            elif event.type == KEYDOWN:
                KEY_PRESSED = event.key

    # ---------------------------- MOUSE FUNCTIONS ------------------------
        if LEFT_PRESSED:
            if LEFT_PRESSING_CONTROL == "NumbersBar":
                numbersBar.UpdateNumber(MOUSEPOS)
            elif LEFT_PRESSING_CONTROL == "SpanRandomButton":
                showNoticeLabel = False
                elementContainer = elm.ElementContainer("random",numbersBar.num)
                LEFT_PRESSING_CONTROL = None
            elif LEFT_PRESSING_CONTROL == "SortButton":
                if elementContainer != None:
                    if elementContainer.running:
                        if elementContainer.pausing:
                            elementContainer.Continue()
                        else:
                            elementContainer.Pause()
                    else:
                        elementContainer.Input(0, -2)
                        elementContainer.Deselect()
                        elementContainer.CopyList()
                        if sortAlgorithms[sortMethodIndex] == "InsertionSort":
                            SortingAlgorithm.InsertionSort(elementContainer)
                        elif sortAlgorithms[sortMethodIndex] == "SelectionSort":
                            SortingAlgorithm.SelectionSort(elementContainer)
                        elif sortAlgorithms[sortMethodIndex] == "BubbleSort":
                            SortingAlgorithm.BubbleSort(elementContainer)
                        elif sortAlgorithms[sortMethodIndex] == "QuickSort":
                            SortingAlgorithm.QuickSort(elementContainer)
                        elif sortAlgorithms[sortMethodIndex] == "MergeSort":
                            SortingAlgorithm.MergeSort(elementContainer)
                        elif sortAlgorithms[sortMethodIndex] == "HeapSort":
                            SortingAlgorithm.HeapSort(elementContainer)
                        elif sortAlgorithms[sortMethodIndex] == "RadixSort":
                            SortingAlgorithm.RadixSort(elementContainer)
                        showNoticeLabel = True
                        elementContainer.Run()
                LEFT_PRESSING_CONTROL = None
    
        if RIGHT_PRESSED:
            if RIGHT_PRESSING_CONTROL == "SortButton":
                if elementContainer != None and not(elementContainer.running):
                    sortMethodIndex = (sortMethodIndex + 1) % len(sortAlgorithms)
                    sortButton.text = sortAlgorithms[sortMethodIndex]
                    RIGHT_PRESSING_CONTROL = None

    # -------------------------- KEY FUNCTIONS -----------------------
    
        if elementContainer != None and not(elementContainer.running):
            if KEY_PRESSED == K_BACKSPACE or KEY_PRESSED == K_DELETE:
                elementContainer.Input(0, -1)
            elif KEY_PRESSED == K_RETURN:
                elementContainer.Input(0, 1)
            elif KEY_PRESSED == K_ESCAPE:
                elementContainer.Input(0, -2)
            elif KEY_PRESSED == K_TAB:
                elementContainer.Input(0, 2)
            elif KEY_PRESSED == K_0: elementContainer.Input(0)
            elif KEY_PRESSED == K_1: elementContainer.Input(1)
            elif KEY_PRESSED == K_2: elementContainer.Input(2)
            elif KEY_PRESSED == K_3: elementContainer.Input(3)
            elif KEY_PRESSED == K_4: elementContainer.Input(4)
            elif KEY_PRESSED == K_5: elementContainer.Input(5)
            elif KEY_PRESSED == K_6: elementContainer.Input(6)
            elif KEY_PRESSED == K_7: elementContainer.Input(7)
            elif KEY_PRESSED == K_8: elementContainer.Input(8)
            elif KEY_PRESSED == K_9: elementContainer.Input(9)

            KEY_PRESSED = None

    # ---------------------------- LOGIC TEXT ------------------------

        # Notice Label Settings
        if elementContainer != None:
            sortName = "Method: " + elementContainer.sortingMethod
            sortInformation = str(elementContainer.changesCount) + " changes - " + \
                                        str(elementContainer.stepCount) + " access"
            if elementContainer.running and not(elementContainer.pausing):
                sortTime = "Time: " + str(round(elementContainer.runningTimer.Flash() / settings.global_animation_speed,1))

        # Buttons Text Settings
        if elementContainer != None and elementContainer.running:
            if elementContainer.pausing:
                sortButton.text = "Continue"
            else:
                sortButton.text = "Pause"
            sortNameLabel.text = sortName
            sortInformationLabel.text = sortInformation
            sortTimeLabel.text = sortTime
        else:
            sortButton.text = sortAlgorithms[sortMethodIndex]

    # -------------------------- FLASH ANIMATIONS ------------------------
        if elementContainer != None:
            elementContainer.Update()   # Refresh all element in container
                                        # Also refresh number-controller
        
    # ---------------------------- RENDER SCREEN ------------------------
        DISPLAYSURF.fill(settings.background_color)

        Renderer.RenderSlideBar(DISPLAYSURF, numbersBar)
        Renderer.RenderButton(DISPLAYSURF, spanRandomButton,1)
        Renderer.RenderButton(DISPLAYSURF, sortButton,1)
        Renderer.RenderDrawingArea(DISPLAYSURF, elementContainer,settings.drawing_area_mode)

        if showNoticeLabel:
            Renderer.RenderNoticeLabel(DISPLAYSURF, sortNameLabel, sortInformationLabel, sortTimeLabel, mode=2)

        if elementContainer != None:
            Renderer.RenderShader(DISPLAYSURF, elementContainer.shaderLayer, 1)

        if settings.enable_copyright:
            tempColor = settings.font_color
            settings.font_color = (100, 100, 100)
            Renderer.RenderButton(DISPLAYSURF, copyrightLabel, 2)
            settings.font_color = tempColor

        pygame.display.update()



if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:", ["help", "mode="])
    except getopt.GetoptError:
        print('Execute: Sorting-Demo.py -m <mode> [arguments]')
        print('Error: Parameter Error')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Execute: Sorting-Demo.py -m <mode> [arguments]')
            sys.exit(0)
        elif opt in ("-m", "--mode"):
            if arg == "color_mode":
                settings.use_gradiant_in_numbers_rank = True
                settings.use_shader = False
                settings.drawing_area_mode = 5
                settings.global_animation_speed = 0.005
                settings.numbers_gap = -1
                settings.exchange_animation_mode = 4
                settings.slide_bar_range = (50,300)
                settings.random_range = (1,500)
            elif arg == "number_mode":
                pass
    MainLoop()  # init screen
