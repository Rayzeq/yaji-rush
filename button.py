import pygame
from os import path

def get_file(name):
	return path.join(path.dirname(path.realpath(__file__)), name)

class Button(pygame.sprite.Sprite):

	def __init__(self, img, x, y):
		super().__init__()
		self.x = x
		self.y = y
		self.img = img
		self.image = pygame.image.load(get_file(img))
		self.is_int = False
		if img[8] == '2':
			self.image = pygame.transform.scale(self.image, (48, 48))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.n = 1
		self.gameset = {0 : [10000,30000,60000], 1 : [500,1000,2000], 2 : [3,5,10]}

	def selected(self):
		self.image = pygame.transform.scale(self.image, (int(self.rect.width*1.5), int(self.rect.height*1.5)))
		self.rect.x = self.x-(self.rect.width//4)
		self.rect.y = self.y-(self.rect.height//4)

	def unselected(self):
		self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
		self.rect.x = self.x
		self.rect.y = self.y

	def int(self):
		self.image = pygame.image.load(get_file(self.img[:-4] + '2' + self.img[-4:]))
		self.is_int = True
	def deint(self):
		self.image = pygame.image.load(get_file(self.img))
		self.is_int = False

	def next(self):
		if self.n < 3:
			self.n += 1
		else:
			self.n = 1
		self.image = pygame.image.load(get_file(self.img[:-5] + str(self.n) + self.img[-4:]))
