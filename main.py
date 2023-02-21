#!/usr/bin/env python3

import time

import pygame
from game import Game

import scenes
from assets import ASSETS
from settings import SETTINGS

pygame.init()


screen = pygame.display.set_mode((576, 576))
pygame.display.set_caption('Yaji-Rush')


font_won = pygame.font.SysFont(None, 50)

bgSet = ASSETS.image.background

bg1p = bgSet.copy()
bg1p.blit(ASSETS.image.bg_1p, (0, 0))
bg1pTime = bgSet.copy()
bg1pTime.blit(ASSETS.image.bg_1pTime, (0, 0))
bg2p = bgSet.copy()
bg2p.blit(ASSETS.image.bg_2p, (0, 0))
bg2pTime = bgSet.copy()
bg2pTime.blit(ASSETS.image.bg_2pTime, (0, 0))
bg_go_1p = bgSet.copy()
bg_go_1p.blit(ASSETS.image.bg_go_1p, (0, 0))
bg_go_2p = bgSet.copy()
bg_go_2p.blit(ASSETS.image.bg_go_2p, (0, 0))


title_screen = scenes.Main(
    lambda _: (setattr(game, 'phase', '1p'), setattr(game, 'mode', '1p')),
    lambda _: (setattr(game, 'mode', '2p'), game.start()),
    lambda _: setattr(game, 'phase', 'settings'),
    lambda _: (globals().__setitem__("running", False), pygame.quit()),
    lambda: (globals().__setitem__("running", False), pygame.quit()),
)

one_player_menu = scenes.OnePlayerMenu(
    lambda _: start_game('time', {0: True, 1: False, 2: False}),
    lambda _: start_game('scor', {0: False, 1: True, 2: False}),
    lambda _: start_game('life', {0: False, 1: False, 2: True}),
    lambda _: start_game('cstm', game.gameplan.copy(), game.gameset.copy()),
    lambda _: (highscore_screen.refresh(), setattr(game, 'phase', 'hs')),
    lambda: setattr(game, 'phase', 'title'),
)


settings_screen = scenes.Settings(
    lambda value: game.gameplan.__setitem__(0, value),
    lambda value: game.gameplan.__setitem__(1, value),
    lambda value: game.gameplan.__setitem__(2, value),
    lambda _: setattr(game, 'phase', 'key_set'),
    lambda: setattr(game, 'phase', 'title'),
    lambda _, value: game.gameset.__setitem__(0, value),
    lambda _, value: game.gameset.__setitem__(1, value),
    lambda _, value: game.gameset.__setitem__(2, value),
)

controls_screen = scenes.ControlSettings(
    lambda: setattr(game, 'phase', 'settings'),
)

highscore_screen = scenes.Highscore(
    lambda: setattr(game, 'phase', '1p')
)


def start_game(mode, plan, set=None):
    global game
    game.mod1p = mode
    game.gameplan2 = plan

    if set is None:
        game.gameset2 = {0: 30000, 1: 2000, 2: 5}
    else:
        game.gameset2 = set

    game.start()


game = Game(screen, {0: settings_screen.left_menu.widgets[0].checked,
                     1: settings_screen.left_menu.widgets[1].checked, 2: settings_screen.left_menu.widgets[2].checked})


running = True
# clock = pygame.time.Clock()

while running:
    before = time.perf_counter()

    if game.phase == "title":
        title_screen.tick(0)
        title_screen.draw(screen)
    elif game.phase == "1p":
        one_player_menu.tick(0)
        one_player_menu.draw(screen)
    elif game.phase == 'settings':
        settings_screen.tick(0)
        settings_screen.draw(screen)
    elif game.phase == 'key_set':
        controls_screen.tick(0)
        controls_screen.draw(screen)
    elif game.phase == 'hs':
        highscore_screen.tick(0)
        highscore_screen.draw(screen)

    elif game.phase == 'game':
        if game.mode == '1p':
            if game.gameplan2[0] or game.mod1p == 'scor':
                screen.blit(bg1pTime, (0, 0))
            else:
                screen.blit(bg1p, (0, 0))
        else:
            if game.gameplan[0]:
                screen.blit(bg2pTime, (0, 0))
            else:
                screen.blit(bg2p, (0, 0))
        game.update()

    elif game.phase == 'gameover':
        screen.blit(bg_go_2p, (0, 0))
        if game.win == 'tied':
            screen.blit(font_won.render(
                'Tied !', True, (250, 250, 0)), (225, 170))
        else:
            screen.blit(font_won.render('player ' + str(game.win) +
                                        ' won !', True, (250, 250, 0)), (175, 170))
        screen.blit(font_won.render(str(game.score),
                                    True, (255, 255, 255)), (250, 270))
        screen.blit(font_won.render(str(game.score2),
                                    True, (255, 255, 255)), (250, 366))

    elif game.phase == 'gameover1p':
        screen.blit(bg_go_1p, (0, 0))
        if game.mod1p == 'scor':
            screen.blit(font_won.render(str(game.final_time) +
                                        's', True, (255, 255, 255)), (250, 222))
            screen.blit(font_won.render(str(game.high_score) +
                                        's', True, (255, 255, 255)), (324, 342))
        else:
            screen.blit(font_won.render(str(game.score),
                                        True, (255, 255, 255)), (250, 222))
            screen.blit(font_won.render(str(game.high_score),
                                        True, (255, 255, 255)), (324, 342))

    pygame.display.flip()

    for event in pygame.event.get():

        if game.phase == "title":
            title_screen.event(event)
        elif game.phase == '1p':
            one_player_menu.event(event)
        elif game.phase == 'settings':
            settings_screen.event(event)
        elif game.phase == 'key_set':
            controls_screen.event(event)
        elif game.phase == 'hs':
            highscore_screen.event(event)

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            game.presse[event.key] = True

            if game.phase == 'game':
                if game.mode == '1p' and event.key == pygame.K_ESCAPE:
                    game.gameover1p()
                if game.mode == '2p' and event.key == pygame.K_ESCAPE:
                    game.gameover('tied')
                if event.key == SETTINGS.p1_controls.up:
                    game.verif_p1('z')
                if event.key == SETTINGS.p1_controls.left:
                    game.verif_p1('q')
                if event.key == SETTINGS.p1_controls.down:
                    game.verif_p1('s')
                if event.key == SETTINGS.p1_controls.right:
                    game.verif_p1('d')

                if game.mode == '2p':
                    if event.key == SETTINGS.p2_controls.up:
                        game.verif_p2('z')
                    if event.key == SETTINGS.p2_controls.left:
                        game.verif_p2('q')
                    if event.key == SETTINGS.p2_controls.down:
                        game.verif_p2('s')
                    if event.key == SETTINGS.p2_controls.right:
                        game.verif_p2('d')

            elif event.key == pygame.K_RETURN and (game.phase == 'gameover' or game.phase == 'gameover1p'):
                game.phase = 'title'

        elif event.type == pygame.KEYUP:
            game.presse[event.key] = False

    # clock.tick(60)

    elapsed = time.perf_counter() - before
    if elapsed < 0.01666666667:
        time.sleep(0.01666666667 - elapsed)

    # elapsed = time.perf_counter() - before
    # print(
    #     f"Frame took {round(elapsed * 1000, 1)}ms, which is {round(1 / elapsed)} fps")
