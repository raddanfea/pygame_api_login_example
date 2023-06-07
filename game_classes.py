import json

import pygame as pygame

import requests

from ui_classes.Button import Button
from ui_classes.TextBox import TextBox
from ui_classes.TextLabel import TextLabel

variables = {
    'ssl': False,
    'ip': '127.0.0.1',
    'port': 3000
}


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.requests = requests
        self.variables = variables
        self.address = self.parse_address()
        self.windows = dict()
        self.event_handler = CustomEventsObject()

    def parse_address(self):
        return f'http{"s" if self.variables["ssl"] else ""}:{self.variables["ip"]}'

    def login_screen(self):

        self.windows = dict()

        def _send_login_data():
            data = {
                "name": self.windows['name'].text,
                "password": self.windows['pass'].text
            }
            url = 'http://127.0.0.1:3000/login'

            headers = {'Content-type': 'application/json'}
            response = requests.post(url, data=json.dumps(data), headers=headers)
            self.windows['label'].set_text(response.text)

        label = TextLabel(self.screen.get_width() * 0.4, self.screen.get_height() * 0.35,
                          self.font, text='Label')

        name_box = TextBox(self.screen.get_width() * 0.4, self.screen.get_height() * 0.4,
                           self.screen.get_width() * 0.2, self.font.get_height() * 1.3,
                           self.font,
                           text='')
        password_box = TextBox(self.screen.get_width() * 0.4, self.screen.get_height() * 0.45,
                               self.screen.get_width() * 0.2, self.font.get_height() * 1.3,
                               self.font,
                               text='',
                               is_password=True)
        button = Button(self.screen.get_width() * 0.4, self.screen.get_height() * 0.5,
                        self.screen.get_width() * 0.1, self.font.get_height() * 1.3,
                        self.font,
                        text='Login',
                        action=_send_login_data)

        self.windows.update({
            'label': label,
            'name': name_box,
            'pass': password_box,
            'login': button
        })

    def draw_windows(self):
        for each in self.windows.values():
            each.draw(self.screen)

    def event_windows(self, event):
        for each in self.windows.values():
            each.handle_event(event, self.event_handler)


class CustomEventsObject:
    def __init__(self):
        self.user_events = {}

    def add_user_event(self, name: str, length: int, once=False):
        if name in self.user_events:
            event_id = self.user_events[name]
        else:
            event_id = pygame.USEREVENT + 1 + len(self.user_events)

        pygame.time.set_timer(event_id, int(length), once)
        self.user_events[name] = event_id

    def stop_user_event(self, event_name):
        pygame.time.set_timer(self.user_events[event_name], 0)

    def get_event_id(self, name):
        return self.user_events.get(name, False)
