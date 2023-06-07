import pygame


class Button:
    def __init__(self, x, y, w, h, font, text='', action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (100, 100, 100)  # Default color
        self.bg_color = (50, 50, 50)
        self.hover_color = (150, 150, 150)  # Color when mouse over
        self.font = font
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.action = action

    def handle_event(self, event, eventhandler=None):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action is not None:
                    self.action()

    def draw(self, screen):
        # Change color if mouse is over the button
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = self.hover_color
        else:
            color = self.bg_color

        pygame.draw.rect(screen, color, self.rect)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
