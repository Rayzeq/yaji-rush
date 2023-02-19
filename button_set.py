import pygame
from widgets import Button, CheckButton, ListButton, ControlButton


class Button_set():

    def __init__(self, head, typ):
        self.typ = typ
        self.head = head
        self.buttons = [self.head]

    def add(self, text: str):
        if self.typ == 'menu':
            self.buttons.append(
                Button(self.head.x, self.head.y + 77 * len(self.buttons), text))
        elif self.typ == 'key':
            self.buttons.append(
                Button(self.head.x + 144 * len(self.buttons), self.head.y, text))

    def add_check(self, text: str):
        if self.typ == 'menu':
            self.buttons.append(
                CheckButton(self.head.x, self.head.y + 77 * len(self.buttons), text))
        elif self.typ == 'key':
            self.buttons.append(
                CheckButton(self.head.x + 144 * len(self.buttons), self.head.y, text))

    def add_list(self, texts):
        if self.typ == 'menu':
            self.buttons.append(
                ListButton(self.head.x, self.head.y + 77 * len(self.buttons), texts))
        elif self.typ == 'key':
            self.buttons.append(
                ListButton(self.head.x + 144 * len(self.buttons), self.head.y, texts))

    def add_control(self, image, **kwargs):
        if self.typ == 'menu':
            self.buttons.append(
                ControlButton(self.head.x, self.head.y + 77 * len(self.buttons), image, **kwargs))
        elif self.typ == 'key':
            self.buttons.append(
                ControlButton(self.head.x + 144 * len(self.buttons), self.head.y, image, **kwargs))

    def select(self, cursor):
        self.unselect()
        self.buttons[cursor].select()

    def unselect(self):
        for button in self.buttons:
            button.deselect()
