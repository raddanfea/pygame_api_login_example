import pygame


class TextBox:
    def __init__(self, x, y, w, h, font, text='', is_password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255)  # White color
        self.text = text
        self.font = font
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.is_password = is_password

    def handle_event(self, event, event_handler):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                event_handler.add_user_event('backspace', 80)
            elif len(self.text) < 33 and str(event.unicode).isalnum():
                self.text += event.unicode
            self.txt_surface = self._is_password_render()
        elif event.type == pygame.KEYUP:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    event_handler.add_user_event('backspace', 0)
        elif event.type == event_handler.get_event_id('backspace') and self.active:
            self.text = self.text[:-1]
            self.txt_surface = self._is_password_render()

    def _is_password_render(self):
        if self.is_password: return self.font.render('*'*len(self.text), True, self.color)
        return self.font.render(self.text, True, self.color)

    def draw(self, screen):
        if self.active: pygame.draw.rect(screen, (0, 0, 180), self.rect, 2)
        else: pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
