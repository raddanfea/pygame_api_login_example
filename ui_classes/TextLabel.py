import pygame


class TextLabel:
    def __init__(self, x, y, font, text='', color=(255, 255, 255)):
        self.position = (x, y)
        self.font = font
        self.text = text
        self.color = color
        self.txt_surface = self.font.render(text, True, self.color)

    def set_text(self, text):
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, self.position)

    def handle_event(self, event, eventhandler):
        pass
