import pygame
from os import path

def get_file(name):
	return path.join(path.dirname(path.realpath(__file__)), name)

class Title(pygame.sprite.Sprite):

	def __init__(self, screen):
		super().__init__()
		self.image = pygame.image.load(get_file('assets\\flash.png')).convert_alpha()
