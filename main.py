import pygame
from game import Game
from button import Button
from button_set import Button_set
from title import Title
from title import Cog
from os import path

pygame.init()
def get_file(name):
    return path.join(path.dirname(path.realpath(__file__)), name)

pygame.display.set_caption('Yaji-Rush')
screen = pygame.display.set_mode((576,576))


font = pygame.font.SysFont(None, 25)
font_won = pygame.font.SysFont(None, 50)

bg1p = pygame.image.load(get_file('assets\\bg_1p.png'))
bg1pTime = pygame.image.load(get_file('assets\\bg_1pTime.png'))
bg2p = pygame.image.load(get_file('assets\\bg_2p.png'))
bg2pTime = pygame.image.load(get_file('assets\\bg_2pTime.png'))
bg_go_1p = pygame.image.load(get_file('assets\\bg_go_1p.png'))
bg_go_2p = pygame.image.load(get_file('assets\\bg_go_2p.png'))

bgSet = pygame.image.load(get_file('assets\\bg_test.png'))
bg_hs = pygame.image.load(get_file('assets\\bg_hs.png'))

title = Title(screen)
title_animation = 0
title_angle=-30

cog = Cog(screen,288,0)
cog2 = Cog(screen,-288,0) 
cog3 = Cog(screen,288,-288) 
cog4 = Cog(screen,288,288)
cog5 = Cog(screen,-288,-288) 
cog6 = Cog(screen,-288,288) 
cog7 = Cog(screen,0,0) 

buttons_title = Button_set(Button('assets\\btn_1p.png', -10, 275), 'menu')
buttons_title.add('assets\\btn_2p.png')
buttons_title.add('assets\\btn_set.png')
buttons_title.add('assets\\btn_quit.png')

buttons_1p = Button_set(Button('assets\\btn_time.png', -50, 110), 'menu')
buttons_1p.add('assets\\btn_score.png')
buttons_1p.add('assets\\btn_vie.png')
buttons_1p.add('assets\\btn_custom.png')
buttons_1p.add('assets\\btn_high-score.png')
buttons_1p.add('assets\\btn_back.png')

buttons_set = Button_set(Button('assets\\btn_time.png', -100, 200), 'menu')
buttons_set.add('assets\\btn_score.png')
buttons_set.add('assets\\btn_vie.png')
buttons_set.add('assets\\btn_control.png')
buttons_set.add('assets\\btn_back.png')

buttons_set2 = Button_set(Button('assets\\btn_time_1.png', 288, 200), 'menu')
buttons_set2.add('assets\\btn_scor_1.png')
buttons_set2.add('assets\\btn_vies_1.png')

buttons_key = Button_set(Button('assets\\btn_k_q.png', 0, 200), 'key')
buttons_key.add('assets\\btn_k_z.png')
buttons_key.add('assets\\btn_k_s.png')
buttons_key.add('assets\\btn_k_d.png')

buttons_key2 = Button_set(Button('assets\\btn_k_q.png', 0, 354), 'key')
buttons_key2.add('assets\\btn_k_z.png')
buttons_key2.add('assets\\btn_k_s.png')
buttons_key2.add('assets\\btn_k_d.png')

btn_back_ctrl = Button('assets\\btn_back.png', -50, 500)

cursor = 0
cur1p = -1
curset = [-1,0]
curctrl = [-1,0]

key_selected = False

game = Game(screen, {0 : buttons_set.buttons[0].is_int, 1 : buttons_set.buttons[1].is_int, 2 : buttons_set.buttons[2].is_int})

running = True

while running:

    if game.phase == 'game':
        if game.mode=='1p':
            if game.gameplan2[0] or game.mod1p == 'scor':
                screen.blit(bg1pTime, (0,0))
            else:
                screen.blit(bg1p, (0,0))
        else:
            if game.gameplan[0]:
                screen.blit(bg2pTime, (0,0))
            else:
                screen.blit(bg2p, (0,0))
        game.update()

    elif game.phase == 'title':
        screen.blit(bgSet, (0,0))
        cog4.animate()
        if title_animation < 60:
            title_animation+=1
            title_angle+=1
        else:
            title_animation+=1
            title_angle-=1
            if title_animation >= 120:
                title_animation = 0
        title.blitRotateCenter(screen, title.image, (title.rect.x, title.rect.y), title_angle)

        for button in buttons_title.buttons:
            screen.blit(button.image, button.rect)
        if cursor == 0:
            game.mode = '1p'
            
        elif cursor == 1:
            game.mode = '2p'

        buttons_title.select(cursor)

    elif game.phase == '1p':
        screen.blit(bgSet, (0,0))
        cog3.animate()
        cog4.animate()
        cog5.animate()
        cog6.animate()
        screen.blit(pygame.image.load(get_file('assets\\head_1p.png')), (144,50))
        for button in buttons_1p.buttons:
            screen.blit(button.image, button.rect)
        if cur1p!=-1:
            buttons_1p.select(cur1p)
        else:
            buttons_1p.unselect()

    elif game.phase == 'hs':
        with open(get_file('save\\save_time.txt'), 'r') as f:
                high_score_time = f.read()
        with open(get_file('save\\save_scor.txt'), 'r') as f:
                high_score_scor = f.read()
        with open(get_file('save\\save_life.txt'), 'r') as f:
                high_score_life = f.read()
        screen.blit(bgSet, (0,0))
        cog7.animate()
        screen.blit(bg_hs, (0,0))
        screen.blit(font_won.render(high_score_time, True, (255,255,255)), (200,198))
        screen.blit(font_won.render(high_score_scor+'s', True, (255,255,255)), (210,294))
        screen.blit(font_won.render(high_score_life, True, (255,255,255)), (200,390))

    elif game.phase == 'settings':
        screen.blit(bgSet, (0,0))
        cog.animate()
        cog2.animate()
        screen.blit(pygame.image.load(get_file('assets\\head_set.png')), (144,50))

        for button in buttons_set.buttons:
            screen.blit(button.image, button.rect)
        if curset[1] == 0 or curset[0] > 2:
            buttons_set2.unselect()
            buttons_set.select(curset[0])

        for i in range(len(buttons_set2.buttons)):
            if game.gameplan[i]:
                screen.blit(buttons_set2.buttons[i].image, buttons_set2.buttons[i].rect)
        if curset[1] == 1 and curset[0] < 3:
            buttons_set.unselect()
            buttons_set2.select(curset[0])
        if curset[0] == -1:
            buttons_set.unselect()
            buttons_set2.unselect()

    elif game.phase == 'key_set':
        screen.blit(bgSet, (0,0))
        cog.animate()
        cog2.animate()

        screen.blit(pygame.image.load(get_file('assets\\head_ctrl.png')), (144,50))

        screen.blit(pygame.image.load(get_file('assets\\layout_ctrl_p1.png')), (0,152))
        screen.blit(pygame.image.load(get_file('assets\\layout_ctrl_p2.png')), (0,306))

        screen.blit(btn_back_ctrl.image, btn_back_ctrl.rect)
        for button in buttons_key.buttons:
            screen.blit(button.image, button.rect)

        for button in buttons_key2.buttons:
            screen.blit(button.image, button.rect)

        if curctrl[0] == 0:
            buttons_key2.unselect()
            buttons_key.select(curctrl[1])
        elif curctrl[0] == 1:
            buttons_key.unselect()
            buttons_key2.select(curctrl[1])
            btn_back_ctrl.unselected()
        elif curctrl[0] == 2:
            buttons_key2.unselect()
            btn_back_ctrl.selected()

        screen.blit(font.render(pygame.key.name(game.ctrl_p1['q']), True, (0,0,0)), (65,265))
        screen.blit(font.render(pygame.key.name(game.ctrl_p1['z']), True, (0,0,0)), (209,265))
        screen.blit(font.render(pygame.key.name(game.ctrl_p1['s']), True, (0,0,0)), (353,265))
        screen.blit(font.render(pygame.key.name(game.ctrl_p1['d']), True, (0,0,0)), (497,265))

        screen.blit(font.render(pygame.key.name(game.ctrl_p2['q']), True, (0,0,0)), (65,426))
        screen.blit(font.render(pygame.key.name(game.ctrl_p2['z']), True, (0,0,0)), (209,426))
        screen.blit(font.render(pygame.key.name(game.ctrl_p2['s']), True, (0,0,0)), (353,426))
        screen.blit(font.render(pygame.key.name(game.ctrl_p2['d']), True, (0,0,0)), (497,426))

    elif game.phase == 'gameover':
        screen.blit(bg_go_2p, (0,0))
        if game.win == 'tied':
            screen.blit(font_won.render('Tied !', True, (250,250,0)), (225,170))   
        else: 
            screen.blit(font_won.render('player ' + str(game.win) + ' won !', True, (250,250,0)), (175,170))
        screen.blit(font_won.render(str(game.score), True, (255,255,255)), (250,270))
        screen.blit(font_won.render(str(game.score2), True, (255,255,255)), (250,366))

    elif game.phase == 'gameover1p':
        screen.blit(bg_go_1p, (0,0))
        if game.mod1p == 'scor':
            screen.blit(font_won.render(str(game.final_time) + 's', True, (255,255,255)), (250,222))
            screen.blit(font_won.render(str(game.high_score) + 's', True, (255,255,255)), (324,342))
        else:
            screen.blit(font_won.render(str(game.score), True, (255,255,255)), (250,222))
            screen.blit(font_won.render(str(game.high_score), True, (255,255,255)), (324,342))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running == False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            game.presse[event.key] = True

            if game.phase == 'title': 
                if event.key == pygame.K_RETURN:
                    if cursor == 2:
                        game.phase = 'settings'
                    elif cursor == 3:
                        running == False
                        pygame.quit()
                    elif cursor == 0:
                        game.phase = '1p' 
                    else:
                        game.start()   
                if event.key == pygame.K_UP and cursor > 0:
                    cursor -= 1
                if event.key == pygame.K_DOWN and cursor < 3:
                    cursor +=1
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            if game.phase == '1p': 
                if event.key == pygame.K_RETURN:
                    if cur1p != -1:
                        if cur1p == 4:
                            game.phase = 'hs'
                        elif cur1p == 5:
                            game.phase = 'title'
                        else:
                            game.gameset2 = {0 : 30000, 1 : 2000, 2 : 5}
                            if cur1p == 0:
                                game.gameplan2 = {0 : True, 1 : False, 2 : False}
                                game.mod1p = 'time'
                            elif cur1p == 1:
                                game.gameplan2 = {0 : False, 1 : True, 2 : False}
                                game.mod1p = 'scor'
                            elif cur1p == 2:
                                game.gameplan2 = {0 : False, 1 : False, 2 : True}
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
                    cur1p +=1
                if event.key == pygame.K_ESCAPE:
                    cur1p = -1
                    game.phase = 'title'

            if game.phase == 'settings':
                if event.key == pygame.K_ESCAPE:
                    curset = [-1,0]
                    game.phase = 'title'

                elif event.key == pygame.K_UP and curset[0] > 0:
                    curset[0] -= 1
                elif event.key == pygame.K_DOWN and curset[0] < 4:
                    curset[0] +=1
                elif event.key == pygame.K_LEFT and curset[1] > 0:
                    curset[1] -= 1
                elif event.key == pygame.K_RIGHT and curset[1] < 1:
                    curset[1] +=1

                elif event.key == pygame.K_RETURN:
                    if curset[0]!=-1:
                        if curset[0] > 2:
                            if curset[0] == 3:
                                game.phase = 'key_set'
                                curset = [-1,0]
                                curctrl = [-1,0]
                                key_selected = False
                            else:
                                game.phase = 'title'
                                curset = [-1,0]
                        elif curset[1]==0:
                            if buttons_set.buttons[curset[0]].is_int:
                                buttons_set.buttons[curset[0]].deint()
                                game.gameplan[curset[0]] = False
                            else:
                                buttons_set.buttons[curset[0]].int()
                                game.gameplan[curset[0]] = True
                        elif curset[1] == 1:
                            buttons_set2.buttons[curset[0]].next()
                            game.gameset[curset[0]] = buttons_set2.buttons[curset[0]].gameset[curset[0]][buttons_set2.buttons[curset[0]].n-1]

            
            if game.phase == 'key_set':
                if event.key == pygame.K_ESCAPE:
                    game.phase = 'settings'
                elif event.key == pygame.K_UP and curctrl[0] > 0 and key_selected == False:
                    curctrl[0] -= 1
                elif event.key == pygame.K_DOWN and curctrl[0] < 2 and key_selected == False:
                    curctrl[0] +=1
                elif event.key == pygame.K_LEFT and curctrl[1] > 0 and key_selected == False:
                    curctrl[1] -= 1
                elif event.key == pygame.K_RIGHT and curctrl[1] < 3 and key_selected == False:
                    curctrl[1] +=1
                elif event.key == pygame.K_RETURN:
                    if curctrl[0] == 2:
                        btn_back_ctrl.unselected()
                        game.phase = 'settings'
                    elif key_selected is False:
                        if curctrl[0] == 0:
                            buttons_key.buttons[curctrl[1]].int()
                        elif curctrl[0] == 1:
                            buttons_key2.buttons[curctrl[1]].int()
                        key_selected = True
                        

            if key_selected and game.phase == 'key_set' and event.key != pygame.K_RETURN:
                if curctrl == [0,0]:
                    game.ctrl_p1['q'] = event.key
                if curctrl == [0,1]:
                    game.ctrl_p1['z'] = event.key
                if curctrl == [0,2]:
                    game.ctrl_p1['s'] = event.key
                if curctrl == [0,3]:
                    game.ctrl_p1['d'] = event.key
                if curctrl == [1,0]:
                    game.ctrl_p2['q'] = event.key
                if curctrl == [1,1]:
                    game.ctrl_p2['z'] = event.key
                if curctrl == [1,2]:
                    game.ctrl_p2['s'] = event.key
                if curctrl == [1,3]:
                    game.ctrl_p2['d'] = event.key

                if curctrl[0] == 0:
                    buttons_key.buttons[curctrl[1]].deint()
                else:
                    buttons_key2.buttons[curctrl[1]].deint()
                key_selected = False

            if game.phase == 'game':
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

            if event.key == pygame.K_RETURN and (game.phase == 'gameover' or game.phase == 'gameover1p'):
                game.phase = 'title'

            if event.key == pygame.K_ESCAPE and game.phase == 'hs':
                game.phase = '1p'

        elif event.type == pygame.KEYUP:
            game.presse[event.key] = False