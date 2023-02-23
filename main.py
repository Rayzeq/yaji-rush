#!/usr/bin/env python3

import pygame
import scenes

pygame.init()
screen = pygame.display.set_mode((576, 576))
pygame.display.set_caption('Yaji-Rush')

scene_manager = scenes.SceneManager()
scene_manager.add("main", scenes.Main())
scene_manager.add("menu1p", scenes.OnePlayerMenu())
scene_manager.add("settings", scenes.Settings())
scene_manager.add("controls", scenes.ControlSettings())
scene_manager.goto("main")

clock = pygame.time.Clock()

while scene_manager.running:
    scene_manager.tick(0)
    scene_manager.draw(screen)

    pygame.display.flip()

    for event in pygame.event.get():
        scene_manager.event(event)

    # print(f"FPS: {clock.get_fps()}")
    clock.tick(60)

pygame.quit()
