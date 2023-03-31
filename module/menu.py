import pygame
import data

pygame.init()

class Menu():
    def __init__(self, window, text, font_text, color_text, fon_color):
        self.WINDOW = window
        self.FON_COLOR = fon_color
        self.TEXT = pygame.font.Font(None, font_text).render(text, True, color_text)

        self.BUTTONS = []

    def add_button(self, size, text, func, font_text, color, color_text, img=None):
        x = data.settings_window['WIDTH']//2 - size[0]//2
        if len(self.BUTTONS) > 0:
            y = self.BUTTONS[-1][0].bottom + 30
        else:
            y = 200
        text_buttton = pygame.font.SysFont('notoserifcondensed', font_text).render(text, True, color_text)
        new_button = (pygame.Rect(x, y, size[0], size[1]), text_buttton, color, func, img)
        self.BUTTONS.append(new_button)

    def show(self):
        if self.FON_COLOR != None:
            self.WINDOW.fill(self.FON_COLOR)
        text_rect = self.TEXT.get_rect()
        text_rect.center = (data.settings_window['WIDTH']//2, 100)
        self.WINDOW.blit(self.TEXT, text_rect.topleft)
        for button in self.BUTTONS:
            pygame.draw.rect(self.WINDOW, button[2], button[0])
            text_rect = button[1].get_rect()
            text_rect.center = button[0].center
            self.WINDOW.blit(button[1], text_rect.topleft)
            if button[-1] != None:
                self.WINDOW.blit(button[4], (button[0].x+button[0].h//20, button[0].y+button[0].h//20))
