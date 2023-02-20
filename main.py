#!/usr/bin/env python3

import pygame
from game import Game
from title import Title as MainTitle
from title import Cog
from os import path

from assets import Assets
from widgets.box import Title
from widgets.buttons import Button, CheckButton, ListButton, ControlButton
from widgets.layouts import ListLayout, Direction

pygame.init()


def get_file(name):
    return path.join(path.dirname(path.realpath(__file__)), name)


pygame.display.set_caption('Yaji-Rush')
screen = pygame.display.set_mode((576, 576))


font = pygame.font.SysFont(None, 25)
font_won = pygame.font.SysFont(None, 50)

bgSet = Assets.image.background

bg_hs = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
a = Title(100, 73, "High Scores")
a.draw(bg_hs)
bg_hs.blit(Assets.image.bg_hs, (0, 0))

bg1p = bgSet.copy()
bg1p.blit(Assets.image.bg_1p, (0, 0))
bg1pTime = bgSet.copy()
bg1pTime.blit(Assets.image.bg_1pTime, (0, 0))
bg2p = bgSet.copy()
bg2p.blit(Assets.image.bg_2p, (0, 0))
bg2pTime = bgSet.copy()
bg2pTime.blit(Assets.image.bg_2pTime, (0, 0))
bg_go_1p = bgSet.copy()
bg_go_1p.blit(Assets.image.bg_go_1p, (0, 0))
bg_go_2p = bgSet.copy()
bg_go_2p.blit(Assets.image.bg_go_2p, (0, 0))

head_1p = Title(0, 50, "1 player")
head_1p.x = (576 / 2) - (head_1p.image.get_rect().width / 2)
head_ctrl = Title(0, 50, "Controls")
head_ctrl.x = (576 / 2) - (head_1p.image.get_rect().width / 2)
head_set = Title(0, 50, "Settings")
head_set.x = (576 / 2) - (head_1p.image.get_rect().width / 2)

title = MainTitle(screen)
title_animation = 0
title_angle = -30

cog = Cog(screen, 288, 0)
cog2 = Cog(screen, -288, 0)
cog3 = Cog(screen, 288, -288)
cog4 = Cog(screen, 288, 288)
cog5 = Cog(screen, -288, -288)
cog6 = Cog(screen, -288, 288)
cog7 = Cog(screen, 0, 0)

buttons_1p = ListLayout(
    -50, 110,
    Button(0, 0, "Time"),
    Button(0, 0, "Score"),
    Button(0, 0, "Lives"),
    Button(0, 0, "Custom"),
    Button(0, 0, "High score"),
    Button(0, 0, "Back"),
)

buttons_set = ListLayout(
    -100, 200,
    CheckButton(0, 0, "Time"),
    CheckButton(0, 0, "Score"),
    CheckButton(0, 0, "Lives"),
    Button(0, 0, "Controls"),
    Button(0, 0, "Back"),
)

buttons_set2 = ListLayout(
    288, 200,
    ListButton(0, 0, {"10s": 10000, "30s": 30000, "60s": 60000}),
    ListButton(0, 0, {"500": 500, "1000": 1000, "2000": 2000}),
    ListButton(0, 0, {"3": 3, "5": 5, "10": 10}),
)

buttons_key = ListLayout(
    27, 200,
    ControlButton(
        0, 0,
        Assets.image.template("arrow_icon", color="#211dde", angle=180)
    ),
    ControlButton(
        0, 0,
        Assets.image.template("arrow_icon", color="#e2cb0e", angle=-90),
        offsetx=2
    ),
    ControlButton(
        0, 0,
        Assets.image.template("arrow_icon", color="#0ee20e", angle=90),
        offsetx=2
    ),
    ControlButton(
        0, 0,
        Assets.image.template("arrow_icon", color="#e20e0e", angle=0),
        offsetx=5
    ),
    spacing=144,
    direction=Direction.Horizontal,
)

buttons_key2 = ListLayout(
    27, 354,
    ControlButton(
        0, 0,
        Assets.image.template("arrow_icon", color="#211dde", angle=180)
    ),
    ControlButton(
        0, 0,
        Assets.image.template("arrow_icon", color="#e2cb0e", angle=-90),
        offsetx=2
    ),
    ControlButton(
        0, 0,
        Assets.image.template("arrow_icon", color="#0ee20e", angle=90),
        offsetx=2
    ),
    ControlButton(
        0, 0,
        Assets.image.template("arrow_icon", color="#e20e0e", angle=0),
        offsetx=5
    ),
    spacing=144,
    direction=Direction.Horizontal,
)

btn_back_ctrl = Button(-50, 500, "Back")

cursor = 0
cur1p = -1
curset = [-1, 0]
curctrl = [-1, 0]

key_selected = False

game = Game(screen, {0: buttons_set.widgets[0].checked,
                     1: buttons_set.widgets[1].checked, 2: buttons_set.widgets[2].checked})

buttons_title = ListLayout(
    -10, 275,
    Button(0, 0, "1 player", callback=lambda: setattr(game, 'phase', '1p')),
    Button(0, 0, "2 players", callback=lambda: game.start()),
    Button(0, 0, "Settings",
           callback=lambda: setattr(game, 'phase', 'settings')),
    Button(0, 0, "Quit",
           callback=lambda: (globals().__setitem__("running", False), pygame.quit()))
)

running = True

while running:

    if game.phase == 'game':
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

    elif game.phase == 'title':
        screen.blit(bgSet, (0, 0))
        cog4.animate()
        if title_animation < 60*2:
            title_animation += 1
            title_angle += 0.5
        else:
            title_animation += 1
            title_angle -= 0.5
            if title_animation >= 120*2:
                title_animation = 0
        title.blitRotateCenter(screen, title.image,
                               (title.rect.x, title.rect.y), title_angle)

        buttons_title.draw(screen)
        if cursor == 0:
            game.mode = '1p'

        elif cursor == 1:
            game.mode = '2p'

        buttons_title.focus(cursor)

    elif game.phase == '1p':
        screen.blit(bgSet, (0, 0))
        cog3.animate()
        cog4.animate()
        cog5.animate()
        cog6.animate()
        head_1p.draw(screen)
        buttons_1p.draw(screen)
        if cur1p != -1:
            buttons_1p.focus(cur1p)
        else:
            buttons_1p.unfocus()

    elif game.phase == 'hs':
        with open(get_file('save/save_time.txt'), 'r') as f:
            high_score_time = f.read()
        with open(get_file('save/save_scor.txt'), 'r') as f:
            high_score_scor = f.read()
        with open(get_file('save/save_life.txt'), 'r') as f:
            high_score_life = f.read()
        screen.blit(bgSet, (0, 0))
        cog7.animate()
        screen.blit(bg_hs, (0, 0))
        screen.blit(font_won.render(high_score_time,
                                    True, (255, 255, 255)), (200, 198))
        screen.blit(font_won.render(high_score_scor+'s',
                                    True, (255, 255, 255)), (210, 294))
        screen.blit(font_won.render(high_score_life,
                                    True, (255, 255, 255)), (200, 390))

    elif game.phase == 'settings':
        screen.blit(bgSet, (0, 0))
        cog.animate()
        cog2.animate()
        head_set.draw(screen)

        buttons_set.draw(screen)
        if curset[1] == 0 or curset[0] > 2:
            buttons_set2.unfocus()
            buttons_set.focus(curset[0])

        for i in range(len(buttons_set2.widgets)):
            if game.gameplan[i]:
                buttons_set2.widgets[i].draw(screen)
        if curset[1] == 1 and curset[0] < 3:
            buttons_set.unfocus()
            buttons_set2.focus(curset[0])
        if curset[0] == -1:
            buttons_set.unfocus()
            buttons_set2.unfocus()

    elif game.phase == 'key_set':
        screen.blit(bgSet, (0, 0))
        cog.animate()
        cog2.animate()

        head_ctrl.draw(screen)

        screen.blit(Assets.image.layout_ctrl_p1, (0, 152))
        screen.blit(Assets.image.layout_ctrl_p2, (0, 306))

        btn_back_ctrl.draw(screen)
        buttons_key.draw(screen)
        buttons_key2.draw(screen)

        if curctrl[0] == 0:
            buttons_key2.unfocus()
            buttons_key.focus(curctrl[1])
        elif curctrl[0] == 1:
            buttons_key.unfocus()
            buttons_key2.focus(curctrl[1])
            btn_back_ctrl.unfocus()
        elif curctrl[0] == 2:
            buttons_key2.unfocus()
            btn_back_ctrl.focus()

        screen.blit(font.render(pygame.key.name(
            game.ctrl_p1['q']), True, (0, 0, 0)), (65, 265))
        screen.blit(font.render(pygame.key.name(
            game.ctrl_p1['z']), True, (0, 0, 0)), (209, 265))
        screen.blit(font.render(pygame.key.name(
            game.ctrl_p1['s']), True, (0, 0, 0)), (353, 265))
        screen.blit(font.render(pygame.key.name(
            game.ctrl_p1['d']), True, (0, 0, 0)), (497, 265))

        screen.blit(font.render(pygame.key.name(
            game.ctrl_p2['q']), True, (0, 0, 0)), (65, 426))
        screen.blit(font.render(pygame.key.name(
            game.ctrl_p2['z']), True, (0, 0, 0)), (209, 426))
        screen.blit(font.render(pygame.key.name(
            game.ctrl_p2['s']), True, (0, 0, 0)), (353, 426))
        screen.blit(font.render(pygame.key.name(
            game.ctrl_p2['d']), True, (0, 0, 0)), (497, 426))

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
        if game.phase == 'title':
            buttons_title.event(event)

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            game.presse[event.key] = True

            if game.phase == 'title':
                if event.key == pygame.K_UP and cursor > 0:
                    cursor -= 1
                if event.key == pygame.K_DOWN and cursor < 3:
                    cursor += 1
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            elif game.phase == '1p':
                if event.key == pygame.K_RETURN:
                    if cur1p != -1:
                        if cur1p == 4:
                            game.phase = 'hs'
                        elif cur1p == 5:
                            game.phase = 'title'
                        else:
                            game.gameset2 = {0: 30000, 1: 2000, 2: 5}
                            if cur1p == 0:
                                game.gameplan2 = {0: True, 1: False, 2: False}
                                game.mod1p = 'time'
                            elif cur1p == 1:
                                game.gameplan2 = {0: False, 1: True, 2: False}
                                game.mod1p = 'scor'
                            elif cur1p == 2:
                                game.gameplan2 = {0: False, 1: False, 2: True}
                                game.mod1p = 'life'
                            elif cur1p == 3:
                                game.gameplan2 = game.gameplan.copy()
                                game.gameset2 = game.gameset.copy()
                                game.mod1p = 'cstm'
                            game.start()
                    cur1p = -1
                if event.key == pygame.K_UP and cur1p > 0:
                    cur1p -= 1
                if event.key == pygame.K_DOWN and cur1p < 5:
                    cur1p += 1
                if event.key == pygame.K_ESCAPE:
                    cur1p = -1
                    game.phase = 'title'

            elif game.phase == 'settings':
                if event.key == pygame.K_ESCAPE:
                    curset = [-1, 0]
                    game.phase = 'title'

                elif event.key == pygame.K_UP and curset[0] > 0:
                    curset[0] -= 1
                elif event.key == pygame.K_DOWN and curset[0] < 4:
                    curset[0] += 1
                elif event.key == pygame.K_LEFT and curset[1] > 0:
                    curset[1] -= 1
                elif event.key == pygame.K_RIGHT and curset[1] < 1:
                    curset[1] += 1

                elif event.key == pygame.K_RETURN:
                    if curset[0] != -1:
                        if curset[0] > 2:
                            if curset[0] == 3:
                                game.phase = 'key_set'
                                curset = [-1, 0]
                                curctrl = [-1, 0]
                                key_selected = False
                            else:
                                game.phase = 'title'
                                curset = [-1, 0]
                        elif curset[1] == 0:
                            if buttons_set.widgets[curset[0]].checked:
                                buttons_set.widgets[curset[0]].checked = False
                                game.gameplan[curset[0]] = False
                            else:
                                buttons_set.widgets[curset[0]].checked = True
                                game.gameplan[curset[0]] = True
                        elif curset[1] == 1:
                            buttons_set2.widgets[curset[0]].next()
                            game.gameset[curset[0]] = buttons_set2.widgets[curset[0]
                                                                           ].value

            elif game.phase == 'key_set':
                if event.key == pygame.K_ESCAPE:
                    game.phase = 'settings'
                elif event.key == pygame.K_UP and curctrl[0] > 0 and key_selected == False:
                    curctrl[0] -= 1
                elif event.key == pygame.K_DOWN and curctrl[0] < 2 and key_selected == False:
                    curctrl[0] += 1
                elif event.key == pygame.K_LEFT and curctrl[1] > 0 and key_selected == False:
                    curctrl[1] -= 1
                elif event.key == pygame.K_RIGHT and curctrl[1] < 3 and key_selected == False:
                    curctrl[1] += 1
                elif event.key == pygame.K_RETURN:
                    if curctrl[0] == 2:
                        btn_back_ctrl.unfocus()
                        game.phase = 'settings'
                    elif key_selected is False:
                        if curctrl[0] == 0:
                            buttons_key.widgets[curctrl[1]].checked = True
                        elif curctrl[0] == 1:
                            buttons_key2.widgets[curctrl[1]].checked = True
                        key_selected = True

                if key_selected and event.key != pygame.K_RETURN:
                    if curctrl == [0, 0]:
                        game.ctrl_p1['q'] = event.key
                    if curctrl == [0, 1]:
                        game.ctrl_p1['z'] = event.key
                    if curctrl == [0, 2]:
                        game.ctrl_p1['s'] = event.key
                    if curctrl == [0, 3]:
                        game.ctrl_p1['d'] = event.key
                    if curctrl == [1, 0]:
                        game.ctrl_p2['q'] = event.key
                    if curctrl == [1, 1]:
                        game.ctrl_p2['z'] = event.key
                    if curctrl == [1, 2]:
                        game.ctrl_p2['s'] = event.key
                    if curctrl == [1, 3]:
                        game.ctrl_p2['d'] = event.key

                    if curctrl[0] == 0:
                        buttons_key.widgets[curctrl[1]].checked = False
                    else:
                        buttons_key2.widgets[curctrl[1]].checked = False
                    key_selected = False

            elif game.phase == 'game':
                if game.mode == '1p' and event.key == pygame.K_ESCAPE:
                    game.gameover1p()
                if game.mode == '2p' and event.key == pygame.K_ESCAPE:
                    game.gameover('tied')
                if event.key == game.ctrl_p1['z']:
                    game.verif_p1('z')
                if event.key == game.ctrl_p1['q']:
                    game.verif_p1('q')
                if event.key == game.ctrl_p1['s']:
                    game.verif_p1('s')
                if event.key == game.ctrl_p1['d']:
                    game.verif_p1('d')

                if game.mode == '2p':
                    if event.key == game.ctrl_p2['z']:
                        game.verif_p2('z')
                    if event.key == game.ctrl_p2['q']:
                        game.verif_p2('q')
                    if event.key == game.ctrl_p2['s']:
                        game.verif_p2('s')
                    if event.key == game.ctrl_p2['d']:
                        game.verif_p2('d')

            elif event.key == pygame.K_RETURN and (game.phase == 'gameover' or game.phase == 'gameover1p'):
                game.phase = 'title'

            elif event.key == pygame.K_ESCAPE and game.phase == 'hs':
                game.phase = '1p'

        elif event.type == pygame.KEYUP:
            game.presse[event.key] = False
