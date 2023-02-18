import pygame
from button import Button

class Button_set():

	def __init__(self, head, typ):
		self.typ = typ
		self.head = head
		self.buttons = [self.head]

	def add(self, img):
		if self.typ == 'menu':
			self.buttons.append(Button(img, self.head.rect.x, self.head.rect.y + 77 * len(self.buttons)))
		elif self.typ == 'key':
			self.buttons.append(Button(img, self.head.rect.x + 144 * len(self.buttons), self.head.rect.y))

	def select(self, cursor):
		self.unselect()
		self.buttons[cursor].selected()

	def unselect(self):
		for button in self.buttons:
			button.unselected()