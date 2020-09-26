import pygame
import settings
import SlideBar
import ButtonClass
import NumberClass
import ShaderClass

import ColorClass as clr

pygame.init()
STD_FONT = pygame.font.SysFont("consolas",18)

def RenderSlideBar(DISPLAYSURF, slidebar):
    pygame.draw.line(DISPLAYSURF, settings.frame_color, slidebar.minpos, slidebar.maxpos, settings.frame_width)
    pygame.draw.circle(DISPLAYSURF, settings.frame_color, slidebar.pos, settings.frame_width+5)
    pygame.draw.circle(DISPLAYSURF, settings.background_color, slidebar.pos, settings.frame_width)
    DISPLAYSURF.blit(STD_FONT.render(str(slidebar.minnum),1,settings.font_color),(slidebar.minpos[0],slidebar.minpos[1]));
    DISPLAYSURF.blit(STD_FONT.render(str(slidebar.maxnum),1,settings.font_color),(slidebar.maxpos[0],slidebar.maxpos[1]));
    DISPLAYSURF.blit(STD_FONT.render(str(slidebar.num),1,settings.font_color),(slidebar.pos[0],slidebar.pos[1]+8));

def RenderButton(DISPLAYSURF, button, mode=0):
    if mode == 0 or mode == 1:
        pygame.draw.rect(DISPLAYSURF, settings.frame_color, pygame.rect.Rect(button.rect[0][0],
                                                                             button.rect[0][1],
                                                                             button.rect[1][0] - button.rect[0][0],
                                                                             button.rect[1][1] - button.rect[0][1]))
    if mode == 1:
        pygame.draw.rect(DISPLAYSURF, settings.background_color, pygame.rect.Rect(button.rect[0][0]+3,
                                                                             button.rect[0][1]+3,
                                                                             button.rect[1][0] - button.rect[0][0] - 6,
                                                                             button.rect[1][1] - button.rect[0][1] - 6))
    textLength = len(button.text)
    DISPLAYSURF.blit(STD_FONT.render(button.text,1,settings.font_color),(button.centerPos[0]-(textLength*9//2),button.centerPos[1]-11));

def RenderNoticeLabel(DISPLAYSURF, *args, mode=0):
    for label in args:
        RenderButton(DISPLAYSURF, label, mode)

def RenderNumbers(DISPLAYSURF, number, mode=1):
    renderColor = (0, 0, 0)

    if number.colorAnimation != None:
        if number.colorAnimation.animation.in_animation:
            renderColor = number.colorAnimation.GetColor()
    else:
        renderColor = clr.ColorRenderer(number.mode)
        if renderColor == None:
            renderColor = number.customColor

    pygame.draw.rect(DISPLAYSURF, renderColor, number.rect)
    if mode == 0 or mode == 1:
        pygame.draw.rect(DISPLAYSURF, settings.background_color, pygame.rect.Rect(number.rect.left+3,
                                                                             number.rect.top+3,
                                                                             number.rect.width-6,
                                                                             number.rect.height-6))
    if number.preNumber != None:
        if number.preNumber == 0:
            _tempNumberStr = "_"
        else:
            _tempNumberStr = str(number.preNumber)+"_"
    else:
        _tempNumberStr = str(number.number)

    if mode == 0 or mode == 2:
        DISPLAYSURF.blit(STD_FONT.render(_tempNumberStr,1,settings.font_color),(number.rect.midtop[0]-10,number.rect.midtop[1]+25));
    elif mode == 1 or mode == 3:
        DISPLAYSURF.blit(STD_FONT.render(_tempNumberStr,1,settings.font_color),(number.rect.midtop[0]-10,number.rect.midtop[1]-25));

def RenderDrawingArea(DISPLAYSURF, elementContainer, mode=1):
    if elementContainer == None: return
    for element in elementContainer.elementList:
        if element.number.selected:
            RenderNumbers(DISPLAYSURF, element.number, 1)
        else:
            RenderNumbers(DISPLAYSURF, element.number, mode)

def RenderShader(DISPLAYSURF, shaderLayer, mode=1):
    for shader in shaderLayer:
        SHADER_LAYER = DISPLAYSURF.convert_alpha()
        _tempRect = shader.rect
        pygame.draw.rect(SHADER_LAYER,settings.shader_color_alpha,
                         pygame.rect.Rect(settings.shader_area[0][0],
                                          settings.shader_area[0][1],
                                          settings.shader_area[1][0] - settings.shader_area[0][0],
                                          _tempRect.top - settings.shader_area[0][1]))
        pygame.draw.rect(SHADER_LAYER,settings.shader_color_alpha,
                         pygame.rect.Rect(settings.shader_area[0][0],
                                          _tempRect.top,
                                          _tempRect.left - settings.shader_area[0][0],
                                          settings.shader_area[1][1] - _tempRect.top))
        pygame.draw.rect(SHADER_LAYER,settings.shader_color_alpha,
                         pygame.rect.Rect(_tempRect.right + settings.numbers_gap,
                                          _tempRect.top,
                                          settings.shader_area[1][0] - _tempRect.right - settings.numbers_gap,
                                          settings.shader_area[1][1] - _tempRect.top))
        pygame.draw.rect(SHADER_LAYER,settings.shader_color_alpha,
                         pygame.rect.Rect(_tempRect.left,
                                          _tempRect.bottom,
                                          _tempRect.width + settings.numbers_gap,
                                          settings.shader_area[1][1] - _tempRect.bottom))
        SHADER_LAYER.set_alpha(settings.shader_color_alpha[3])
        DISPLAYSURF.blit(SHADER_LAYER,(0,0))