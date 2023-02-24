import pygame
from random import randint
from arrow import Arrow
from keys import Keys
from os import path

def get_file(name):
    return path.join(path.dirname(path.realpath(__file__)), name)

class Game():

	def __init__(self,screen, gameplan):
		self.phase = 'title'
		self.screen = screen
		self.font = pygame.font.SysFont(None, 25)
		self.font2 = pygame.font.SysFont(None, 50)
		self.img_flash = pygame.image.load(get_file('assets\\flash.png'))
		self.flashx = 0
		self.startimer_flash = 0
		self.mode = '1p'
		self.gameplan2 = gameplan
		self.gameplan = gameplan
		self.time = 10000
		self.goal = 500
		self.vie_max = 3
		self.gameset = {0 : 10000, 1 : 500, 2 : 3}
		self.gameset2 = {0 : 10000, 1 : 500, 2 : 3}
		self.mod1p = 'time'
		self.final_time = 0
		self.high_score = 0
		self.hs_guy = ''
		self.can_play = False

		self.arrows = pygame.sprite.Group()

		self.ctrl_p1 = {'q' : pygame.K_q, 'z' : pygame.K_z, 's' : pygame.K_s, 'd' : pygame.K_d}
		self.ctrl_p2 = {'q' : pygame.K_KP4, 'z' : pygame.K_KP8, 's' : pygame.K_KP5, 'd' : pygame.K_KP6}
		
		self.game1 = []
		self.game2 = []
		self.all_keys1 = pygame.sprite.Group()
		self.all_keys2 = pygame.sprite.Group()

		self.vie1=self.gameset[2]
		self.vie2=self.gameset[2]
	
		self.presse = {}

	def create_arrow(self):
		if self.mode == '1p':
			self.q = Arrow('q', 192, 432, 1, self)
			self.z = Arrow('z', 240, 432, 1, self)
			self.s = Arrow('s', 288, 432, 1, self)
			self.d = Arrow('d', 336, 432, 1, self)
			self.arrows.add(self.q)
			self.arrows.add(self.z)
			self.arrows.add(self.s)
			self.arrows.add(self.d)
			self.dico_arrows1 = {'q' : self.q, 'z' : self.z, 's' : self.s, 'd' : self.d}
		else:
			self.q = Arrow('q', 1*48, 432, 1, self)
			self.z = Arrow('z', 2*48, 432, 1, self)
			self.s = Arrow('s', 3*48, 432, 1, self)
			self.d = Arrow('d', 4*48, 432, 1, self)
			self.arrows.add(self.q)
			self.arrows.add(self.z)
			self.arrows.add(self.s)
			self.arrows.add(self.d)
			self.dico_arrows1 = {'q' : self.q, 'z' : self.z, 's' : self.s, 'd' : self.d}


			self.q2 = Arrow('q', 1*48+288, 432, 2, self)
			self.z2 = Arrow('z', 2*48+288, 432, 2, self)
			self.s2 = Arrow('s', 3*48+288, 432, 2, self)
			self.d2 = Arrow('d', 4*48+288, 432, 2, self)
			self.arrows.add(self.q2)
			self.arrows.add(self.z2)
			self.arrows.add(self.s2)
			self.arrows.add(self.d2)
			self.dico_arrows2 = {'q' : self.q2, 'z' : self.z2, 's' : self.s2, 'd' : self.d2}
	
	def create_key(self, x, y):
		self.r=randint(1,4)
		if self.mode == '1p':
			self.key = Keys(self.r, x+self.r*48, y, 1, self)
			self.all_keys1.add(self.key)
			return (self.key, 0)
		else:
			self.key = Keys(self.r, x+self.r*48, y, 1, self)
			self.all_keys1.add(self.key)
			self.key2 = Keys(self.r, x+self.r*48, y, 2, self)
			self.all_keys2.add(self.key2)
			return (self.key, self.key2)

	def start(self):
		self.start_time = pygame.time.get_ticks()

		self.score=0
		self.combo=0

		self.score2=0
		self.combo2=0

		if self.mode == '2p':
			self.vie1=self.gameset[2]
			self.vie2=self.gameset[2]
		else:
			self.vie1=self.gameset2[2]

		self.create_arrow()

		self.phase = 'game'

		if self.mode == '1p':
			for i in range(10):
				self.game1.append(self.create_key(144, i*48)[0])
		else:
			for i in range(10):
				self.game1.append(self.create_key(0, i*48)[1])
				self.game2.append(self.create_key(288, i*48)[0])

	def gameover(self, win):
		self.can_play = False
		self.game1.clear()
		self.game2.clear()
		
		for key in self.all_keys1:
			key.remove()
		for key in self.all_keys2:
			key.remove()

		for arrow in self.arrows:
			arrow.remove()

		self.phase = 'gameover'
		self.win = win

	def gameover1p(self):
		self.can_play = False
		self.vie1 = 5
		self.game1.clear()
		for key in self.all_keys1:
			key.remove()

		for arrow in self.arrows:
			arrow.remove()

		if self.mod1p != 'cstm':
			if self.save_vierge(self.mod1p):
				if self.mod1p == 'scor':
					self.high_score = self.final_time
				else:
					self.high_score = self.score
				self.phase = 'nhs'
			else:
				self.high_score = self.get_hs(self.mod1p)

				if self.mod1p == 'scor':
					if self.final_time <= self.high_score:
						self.high_score = self.final_time
						self.phase = 'nhs'
					else:
						self.phase = 'gameover1p'
						
				else:
					if self.score >= self.high_score:
						self.high_score = self.score
						self.phase = 'nhs'
					else:
						self.phase = 'gameover1p'
		else:
			self.phase = 'gameover1p'

	def save(self):
		with open(get_file('save\\save_' + self.mod1p + '.txt'), 'w') as f:
			f.writelines(self.hs_guy + '.' + str(self.high_score))

	def save_vierge(self, mod):
		with open(get_file('save\\save_' + mod + '.txt'), 'r') as f:
				n = f.read()
		return n==''

	def get_hs(self, mod):
		if self.save_vierge(mod):
			return 'no high_score'
		with open(get_file('save\\save_' + mod + '.txt'), 'r') as f:
				n = f.read()
		i=0
		while n[i]!='.':
			i+=1
		s=''
		for j in range(i+1, len(n)):
			s+=n[j]
		return int(s)

	def get_hs_guy(self, mod):
		with open(get_file('save\\save_' + mod + '.txt'), 'r') as f:
				n = f.read()
		i=0
		s=''
		while n[i]!='.':
			s+=n[i]
			i+=1
		return s

	def true_start(self):
		self.start_time = pygame.time.get_ticks()
		self.can_play = True

	def update(self):

		if not self.can_play:
			self.screen.blit(self.font2.render(str(3-((pygame.time.get_ticks()-self.start_time)//1000)), True, (255,255,255)), (278,270))
			print((pygame.time.get_ticks()-self.start_time)//1000 >= 4)
			if (pygame.time.get_ticks()-self.start_time)//1000 >= 4:
				self.true_start()
		else:
			if self.mode == '2p' and self.gameplan[0]:
				if (pygame.time.get_ticks()-self.start_time)//1000 < 10:
					self.screen.blit(self.font2.render(str((pygame.time.get_ticks()-self.start_time)//1000), True, (0,0,0)), (278,270))
				else:
					self.screen.blit(self.font2.render(str((pygame.time.get_ticks()-self.start_time)//1000), True, (0,0,0)), (268,270))
			if self.mode == '1p' and (self.gameplan2[0] or self.mod1p == 'scor'):
				if (pygame.time.get_ticks()-self.start_time)//1000 < 10:
					self.screen.blit(self.font2.render(str((pygame.time.get_ticks()-self.start_time)//1000), True, (0,0,0)), (135,465))
				else:
					self.screen.blit(self.font2.render(str((pygame.time.get_ticks()-self.start_time)//1000), True, (0,0,0)), (125,465))

			if self.mode == '1p':
				self.screen.blit(self.font.render(f'Score : {self.score}', True, (0,0,0)), (200,492))
				self.screen.blit(self.font.render(f'Combo : {self.combo}', True, (0,0,0)), (200,516))
				if self.gameplan2[2]:
					self.screen.blit(self.font.render(f'Lives : {self.vie1}', True, (0,0,0)), (200,540))
			else:
				self.screen.blit(self.font.render(f'Score : {self.score}', True, (0,0,0)), (55,492))
				self.screen.blit(self.font.render(f'Combo : {self.combo}', True, (0,0,0)), (55,516))
				if self.gameplan[2]:
					self.screen.blit(self.font.render(f'Lives : {self.vie1}', True, (0,0,0)), (55,540))

				self.screen.blit(self.font.render(f'Score : {self.score2}', True, (0,0,0)), (343,492))
				self.screen.blit(self.font.render(f'Combo : {self.combo2}', True, (0,0,0)), (343,516))
				if self.gameplan[2]:
					self.screen.blit(self.font.render(f'Lives : {self.vie2}', True, (0,0,0)), (343,540))

			for arrow in self.arrows:
				self.screen.blit(arrow.image, arrow.rect)

			for key in self.game1:
				self.screen.blit(key.image, key.rect)
			for key in self.game2:
				self.screen.blit(key.image, key.rect)

			if self.presse.get(self.ctrl_p1['q']):
				self.q.pressed()
			else:
				self.q.unpressed()
			if self.presse.get(self.ctrl_p1['z']):
				self.z.pressed()
			else:
				self.z.unpressed()
			if self.presse.get(self.ctrl_p1['s']):
				self.s.pressed()
			else:
				self.s.unpressed()
			if self.presse.get(self.ctrl_p1['d']):
				self.d.pressed()
			else:
				self.d.unpressed()

			if self.mode == '2p':
				if self.presse.get(self.ctrl_p2['q']):
					self.q2.pressed()
				else:
					self.q2.unpressed()
				if self.presse.get(self.ctrl_p2['z']):
					self.z2.pressed()
				else:
					self.z2.unpressed()
				if self.presse.get(self.ctrl_p2['s']):
					self.s2.pressed()
				else:
					self.s2.unpressed()
				if self.presse.get(self.ctrl_p2['d']):
					self.d2.pressed()
				else:
					self.d2.unpressed()

			if self.mode == '2p':
				if self.gameplan[0]:
					if pygame.time.get_ticks()-self.start_time > self.gameset[0]:
						if self.score > self.score2:
							self.gameover(1)
						elif self.score < self.score2:
							self.gameover(2)
						else:
							self.gameover('tied')
				if self.gameplan[1]:
					if self.score >= self.gameset[1]:
						self.gameover(1)
					if self.score2 >= self.gameset[1]:
						self.gameover(2)
				if self.gameplan[2]:
					if self.vie1 == 0:
						self.gameover(2)
					elif self.vie2 == 0:
						self.gameover(1)
			else:
				if self.gameplan2[0]:
					if pygame.time.get_ticks()-self.start_time > self.gameset2[0]:
						self.gameover1p()
				if self.gameplan2[1]:
					if self.score >= self.gameset2[1]:
						self.final_time = (pygame.time.get_ticks()-self.start_time)//1000
						self.gameover1p()
				if self.gameplan2[2]:
					if self.vie1 == 0:
						self.gameover1p()

			if pygame.time.get_ticks() - self.startimer_flash < 25:
				self.screen.blit(self.img_flash, (self.flashx, 0))
			else:
				self.startimer_flash = 0
			
	def verif_p1(self, k):
		if self.game1[-1].k == k:
			self.game1.pop()
			for key in self.game1:
				key.avance()
			if self.mode == '1p':
				self.game1.insert(0, self.create_key(144, 0)[0])
			else:
				self.game1.insert(0, self.create_key(0, 0)[0])
			self.score+=1+self.combo
			self.combo+=1
		else:
			self.screen.blit(self.img_flash, (0, 0))
			self.score-=1
			self.combo=0
			self.vie1-=1
			self.startimer_flash = pygame.time.get_ticks()
			if self.mode == '1p':
				self.flashx = 144
			else:
				self.flashx = 0


	def verif_p2(self, k):
		if self.game2[-1].k == k:
			self.game2.pop()
			for key in self.game2:
				key.avance()
			self.game2.insert(0, self.create_key(288, 0)[0])
			self.score2+=1+self.combo2
			self.combo2+=1
		else:
			self.score2-=1
			self.combo2=0
			self.vie2-=1
			self.startimer_flash = pygame.time.get_ticks()
			self.flashx = 288