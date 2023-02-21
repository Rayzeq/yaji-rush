import pygame
from random import randint
from arrow import Arrow
from keys import Keys
from os import path

from saves import SAVES
from assets import ASSETS
from settings import SETTINGS


def get_file(name):
    return path.join(path.dirname(path.realpath(__file__)), name)


class Game():

    def __init__(self, screen, gameplan):
        self.phase = 'title'
        self.screen = screen
        self.font = pygame.font.SysFont(None, 25)
        self.font2 = pygame.font.SysFont(None, 50)
        self.img_flash = ASSETS.image.flash
        self.flashx = 0
        self.startimer_flash = 0
        self.mode = '1p'
        self.gameplan2 = gameplan
        self.gameplan = gameplan
        self.time = 10000
        self.goal = 500
        self.vie_max = 3
        self.gameset = {0: 10000, 1: 500, 2: 3}
        self.gameset2 = {0: 10000, 1: 500, 2: 3}
        self.mod1p = 'time'
        self.final_time = 0
        self.high_score = 0

        self.arrows = pygame.sprite.Group()

        self.game1 = []
        self.game2 = []
        self.all_keys1 = pygame.sprite.Group()
        self.all_keys2 = pygame.sprite.Group()

        self.vie1 = self.gameset[2]
        self.vie2 = self.gameset[2]

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
            self.dico_arrows1 = {'q': self.q,
                                 'z': self.z, 's': self.s, 'd': self.d}
        else:
            self.q = Arrow('q', 1*48, 432, 1, self)
            self.z = Arrow('z', 2*48, 432, 1, self)
            self.s = Arrow('s', 3*48, 432, 1, self)
            self.d = Arrow('d', 4*48, 432, 1, self)
            self.arrows.add(self.q)
            self.arrows.add(self.z)
            self.arrows.add(self.s)
            self.arrows.add(self.d)
            self.dico_arrows1 = {'q': self.q,
                                 'z': self.z, 's': self.s, 'd': self.d}

            self.q2 = Arrow('q', 1*48+288, 432, 2, self)
            self.z2 = Arrow('z', 2*48+288, 432, 2, self)
            self.s2 = Arrow('s', 3*48+288, 432, 2, self)
            self.d2 = Arrow('d', 4*48+288, 432, 2, self)
            self.arrows.add(self.q2)
            self.arrows.add(self.z2)
            self.arrows.add(self.s2)
            self.arrows.add(self.d2)
            self.dico_arrows2 = {'q': self.q2,
                                 'z': self.z2, 's': self.s2, 'd': self.d2}

    def create_key(self, x, y):
        self.r = randint(1, 4)
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

        self.score = 0
        self.combo = 0

        self.score2 = 0
        self.combo2 = 0

        if self.mode == '2p':
            self.vie1 = self.gameset[2]
            self.vie2 = self.gameset[2]
        else:
            self.vie1 = self.gameset2[2]

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
        self.vie1 = 5
        self.game1.clear()
        for key in self.all_keys1:
            key.remove()

        for arrow in self.arrows:
            arrow.remove()

        if self.mod1p != 'cstm':
            if self.mod1p == 'scor':
                SAVES.add({"time": "time", "life": "lives", "scor": "score"}[
                          self.mod1p], self.final_time)
                if self.final_time <= self.high_score:
                    self.high_score = self.final_time
            else:
                SAVES.add({"time": "time", "life": "lives", "scor": "score"}[
                          self.mod1p], self.score)
                if self.score >= self.high_score:
                    self.high_score = self.score
        else:
            self.high_score = 'not aviable'

        self.phase = 'gameover1p'

    def update(self):

        if self.mode == '2p' and self.gameplan[0]:
            if (pygame.time.get_ticks()-self.start_time)//1000 < 10:
                self.screen.blit(self.font2.render(str(
                    (pygame.time.get_ticks()-self.start_time)//1000), True, (0, 0, 0)), (278, 270))
            else:
                self.screen.blit(self.font2.render(str(
                    (pygame.time.get_ticks()-self.start_time)//1000), True, (0, 0, 0)), (268, 270))
        if self.mode == '1p' and (self.gameplan2[0] or self.mod1p == 'scor'):
            if (pygame.time.get_ticks()-self.start_time)//1000 < 10:
                self.screen.blit(self.font2.render(str(
                    (pygame.time.get_ticks()-self.start_time)//1000), True, (0, 0, 0)), (135, 465))
            else:
                self.screen.blit(self.font2.render(str(
                    (pygame.time.get_ticks()-self.start_time)//1000), True, (0, 0, 0)), (125, 465))

        if self.mode == '1p':
            self.screen.blit(self.font.render(
                f'Score : {self.score}', True, (0, 0, 0)), (200, 492))
            self.screen.blit(self.font.render(
                f'Combo : {self.combo}', True, (0, 0, 0)), (200, 516))
            if self.gameplan2[2]:
                self.screen.blit(self.font.render(
                    f'Lives : {self.vie1}', True, (0, 0, 0)), (200, 540))
        else:
            self.screen.blit(self.font.render(
                f'Score : {self.score}', True, (0, 0, 0)), (55, 492))
            self.screen.blit(self.font.render(
                f'Combo : {self.combo}', True, (0, 0, 0)), (55, 516))
            if self.gameplan[2]:
                self.screen.blit(self.font.render(
                    f'Lives : {self.vie1}', True, (0, 0, 0)), (55, 540))

            self.screen.blit(self.font.render(
                f'Score : {self.score2}', True, (0, 0, 0)), (343, 492))
            self.screen.blit(self.font.render(
                f'Combo : {self.combo2}', True, (0, 0, 0)), (343, 516))
            if self.gameplan[2]:
                self.screen.blit(self.font.render(
                    f'Lives : {self.vie2}', True, (0, 0, 0)), (343, 540))

        for arrow in self.arrows:
            self.screen.blit(arrow.image, arrow.rect)

        for key in self.game1:
            self.screen.blit(key.image, key.rect)
        for key in self.game2:
            self.screen.blit(key.image, key.rect)

        if self.presse.get(SETTINGS.p1_controls.left):
            self.q.pressed()
        else:
            self.q.unpressed()
        if self.presse.get(SETTINGS.p1_controls.up):
            self.z.pressed()
        else:
            self.z.unpressed()
        if self.presse.get(SETTINGS.p1_controls.down):
            self.s.pressed()
        else:
            self.s.unpressed()
        if self.presse.get(SETTINGS.p1_controls.right):
            self.d.pressed()
        else:
            self.d.unpressed()

        if self.mode == '2p':
            if self.presse.get(SETTINGS.p2_controls.left):
                self.q2.pressed()
            else:
                self.q2.unpressed()
            if self.presse.get(SETTINGS.p2_controls.up):
                self.z2.pressed()
            else:
                self.z2.unpressed()
            if self.presse.get(SETTINGS.p2_controls.down):
                self.s2.pressed()
            else:
                self.s2.unpressed()
            if self.presse.get(SETTINGS.p2_controls.right):
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
                    self.final_time = (
                        pygame.time.get_ticks()-self.start_time)//1000
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
            self.score += 1+self.combo
            self.combo += 1
        else:
            self.screen.blit(self.img_flash, (0, 0))
            self.score -= 1
            self.combo = 0
            self.vie1 -= 1
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
            self.score2 += 1+self.combo2
            self.combo2 += 1
        else:
            self.score2 -= 1
            self.combo2 = 0
            self.vie2 -= 1
            self.startimer_flash = pygame.time.get_ticks()
            self.flashx = 288
