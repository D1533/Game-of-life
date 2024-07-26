import time
import random
import pygame
import sys
from GameClass import Game
import settings


screen = pygame.display.set_mode((settings.SCREEN_MAP_X_SIZE, settings.SCREEN_MAP_Y_SIZE + settings.PANEL_Y_SIZE))
pygame.display.set_caption('The Game of Life')
clock = pygame.time.Clock()
Game = Game(screen)
Game.drawMap()
Game.drawPanel()
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # Checks only one left mouse button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            # Start the game
            if Game.StartButton.collidepoint(pos):
                Game.Start = True
                Game.gameBegin()
            # Random generation
            if Game.RandomButton.collidepoint(pos):
                Game.randomPopulation()
            # Reset stats and map
            elif Game.ResetButton.collidepoint(pos):
                Game.gameReset()
    # Checks left mouse button click hold
    if pygame.mouse.get_pressed()[0] == 1:
        pos = pygame.mouse.get_pos()
        Game.drawCell(pos)
        # Increase number of cells
        if Game.IncreaseCellButton.collidepoint(pos):
            Game.increaseNumberOfCells()
        # Decrease number of cells
        elif Game.DecreaseCellButton.collidepoint(pos):
            Game.decreaseNumberOfCells()
        # Erase Wall
    if pygame.mouse.get_pressed() == (0,0,1):
            pos = pygame.mouse.get_pos()
            Game.eraseCell(pos)

    Game.drawMap()
    Game.drawPanel()
    pygame.display.flip()
    clock.tick(60)

