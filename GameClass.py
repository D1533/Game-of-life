import sys
import pygame
import settings
import random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.number_of_Xcells = settings.NUMBER_OF_X_CELLS
        self.cellSize = settings.SCREEN_MAP_X_SIZE / settings.NUMBER_OF_X_CELLS
        self.number_of_Ycells = int(settings.SCREEN_MAP_Y_SIZE / settings.CELLSIZE)
        self.map = [[0 for x in range(self.number_of_Xcells)] for y in range(self.number_of_Ycells)]
        self.tempMap = [[0 for x in range(self.number_of_Xcells)] for y in range(self.number_of_Ycells)]
        self.living_cells = 0
        self.born_cells = 0
        self.dead_cells = 0

        # Panel members
        self.Start = False
        self.StartButton = pygame.Rect(settings.START_BUTTON_X, settings.START_BUTTON_Y, settings.START_BUTTON_X_SIZE, settings.START_BUTTON_Y_SIZE)
        self.ResetButton = pygame.Rect(settings.RESET_BUTTON_X, settings.RESET_BUTTON_Y, settings.RESET_BUTTON_X_SIZE, settings.RESET_BUTTON_Y_SIZE)
        self.RandomButton = pygame.Rect(settings.RANDOM_BUTTON_X, settings.RANDOM_BUTTON_Y, settings.RANDOM_BUTTON_X_SIZE, settings.RANDOM_BUTTON_Y_SIZE)
        self.IncreaseCellButton = pygame.Rect(settings.INCREASE_CELLS_BUTTON_X, settings.INCREASE_CELLS_BUTTON_Y, settings.INCREASE_CELLS_X_SIZE,settings.INCREASE_CELLS_Y_SIZE)
        self.DecreaseCellButton = pygame.Rect(settings.DECREASE_CELLS_BUTTON_X, settings.DECREASE_CELLS_BUTTON_Y, settings.DECREASE_CELLS_X_SIZE,settings.DECREASE_CELLS_Y_SIZE)
        pygame.font.init()
        self.font = pygame.font.SysFont("Console", 20, bold = True)
        self.font2 = pygame.font.SysFont("Console", 50, bold = True)
        self.font3 = pygame.font.SysFont("Console", 15, bold = True)
        self.font4 = pygame.font.SysFont("Console", 11, bold = True)
    
    def increaseNumberOfCells(self):
        # Increase the number of cells and recalculate the size and number of cells
        if self.number_of_Xcells <= settings.SUP_LIM_OF_X_CELLS:
            self.number_of_Xcells += settings.INCREASE_NUMBER_OF_CELLS
            self.cellSize = settings.SCREEN_MAP_X_SIZE / self.number_of_Xcells
            prev_number_of_Ycells = self.number_of_Ycells
            self.number_of_Ycells = int(settings.SCREEN_MAP_Y_SIZE / self.cellSize)

            # Checks if it is necessary to add a new row
            if prev_number_of_Ycells < self.number_of_Ycells:
                self.map.append([0]*(self.number_of_Xcells))

            # Adds a new column
            for i in range(self.number_of_Ycells):
                self.map[i].append(0)
            # Update the tempMap size too
            self.tempMap = [[0 for x in range(self.number_of_Xcells)] for y in range(self.number_of_Ycells)]

    def decreaseNumberOfCells(self):
        # Decrease the number of cells and recalculate the size and number of cells
        if self.number_of_Xcells >= settings.INF_LIM_OF_X_CELLS:
            prev_number_of_X_cells = self.number_of_Xcells
            self.number_of_Xcells -= settings.DECREASE_NUMBER_OF_CELLS
            self.cellSize = settings.SCREEN_MAP_X_SIZE / self.number_of_Xcells
            prev_number_of_Ycells = self.number_of_Ycells
            self.number_of_Ycells = int(settings.SCREEN_MAP_Y_SIZE / self.cellSize)
    
            # Checks if it is necessary to remove the last row
            if prev_number_of_Ycells > self.number_of_Ycells:
                self.map.pop()
                self.map[-1] = [0]*(prev_number_of_X_cells)
    
            # Removes the last column
            for i in range(self.number_of_Ycells):
                self.map[i].pop()
                self.map[i][-1] = 0
    
            # Update the tempMap size too
            self.tempMap = [[0 for x in range(self.number_of_Xcells)] for y in range(self.number_of_Ycells)]

    def numberOfNeighbors(self, i, j):
        # Top left corner
        if i == 0 and j == 0: 
            return  self.map[1][0] + self.map[1][1] + self.map[0][1] 
        # Bottom left corner
        elif i == self.number_of_Ycells - 1 and j == 0:
            return self.map[i-1][j] + self.map[i-1][j+1] + self.map[i][j+1]
        # Top right corner
        elif i == 0 and j == self.number_of_Xcells - 1:
            return self.map[i][j-1] + self.map[i+1][j-1] + self.map[i+1][j]
        # Bottom right corner
        elif i == self.number_of_Ycells - 1 and j == self.number_of_Xcells - 1:
            return self.map[i-1][j-1] + self.map[i][j-1] + self.map[i-1][j]
        # First row
        elif i == 0:
            return self.map[i][j-1] + self.map[i][j+1] + self.map[i+1][j-1] + self.map[i+1][j] + self.map[i+1][j+1]
        # Last row 
        elif i == self.number_of_Ycells - 1:
            return self.map[i-1][j-1] + self.map[i-1][j] + self.map[i-1][j+1] + self.map[i][j-1] + self.map[i][j+1] 
        # First column
        elif j == 0:
            return self.map[i-1][j] + self.map[i-1][j+1]  + self.map[i][j+1]  + self.map[i+1][j+1] + self.map[i+1][j]
        # Last column
        elif j == self.number_of_Xcells - 1:
            return self.map[i-1][j-1] + self.map[i-1][j] + self.map[i][j-1]  + self.map[i+1][j-1] + self.map[i+1][j] 
        else:
            return self.map[i-1][j-1] + self.map[i-1][j] + self.map[i-1][j+1] + self.map[i][j-1] + self.map[i][j+1] + self.map[i+1][j-1] + self.map[i+1][j] + self.map[i+1][j+1]
    
    def drawMap(self):
        self.screen.fill((20,20,20))
        for i in range(0, self.number_of_Ycells):
            for j in range(0, self.number_of_Xcells):
                #if self.map[i][j] == 0:
                #    pygame.draw.rect(self.screen, (20,20,20), (j*self.cellSize, i*self.cellSize, self.cellSize, self.cellSize))
                if self.map[i][j] == 1:
                    pygame.draw.rect(self.screen, (200,200,200), (j*self.cellSize, i*self.cellSize, self.cellSize, self.cellSize))
                
    def drawPanel(self):
        pygame.draw.line(self.screen, (200,200,200), (0,settings.SCREEN_MAP_Y_SIZE),(settings.SCREEN_MAP_X_SIZE, settings.SCREEN_MAP_Y_SIZE))
        
        # Change Start to Pause text
        if self.Start == False:
            text = self.font.render("START", True, (0,0,0))
        else:
            text = self.font.render("PAUSE", True, (0,0,0))
        
        # Start button
        pygame.draw.rect(self.screen, (200,200,200), ((settings.START_BUTTON_X, settings.START_BUTTON_Y, settings.START_BUTTON_X_SIZE, settings.START_BUTTON_Y_SIZE)))
        pygame.draw.rect(self.screen, (10,10,10), ((settings.START_BUTTON_X, settings.START_BUTTON_Y, settings.START_BUTTON_X_SIZE,settings.START_BUTTON_Y_SIZE)), 2)
        self.screen.blit(text, (settings.START_BUTTON_X + 20, settings.START_BUTTON_Y + 10))

        # Random button
        pygame.draw.rect(self.screen, (200,200,200), ((settings.RANDOM_BUTTON_X, settings.RANDOM_BUTTON_Y, settings.RANDOM_BUTTON_X_SIZE, settings.RANDOM_BUTTON_Y_SIZE)))
        pygame.draw.rect(self.screen, (10,10,10), ((settings.RANDOM_BUTTON_X, settings.RANDOM_BUTTON_Y, settings.RANDOM_BUTTON_X_SIZE,settings.RANDOM_BUTTON_Y_SIZE)), 2)
        self.screen.blit(self.font.render("RANDOM", True, (0,0,0)), (settings.RANDOM_BUTTON_X + 15, settings.RANDOM_BUTTON_Y + 10))

        # Reset button
        pygame.draw.rect(self.screen, (200,200,200), ((settings.RESET_BUTTON_X, settings.RESET_BUTTON_Y, settings.RESET_BUTTON_X_SIZE, settings.RESET_BUTTON_Y_SIZE)))
        pygame.draw.rect(self.screen, (10,10,10), ((settings.RESET_BUTTON_X, settings.RESET_BUTTON_Y, settings.RESET_BUTTON_X_SIZE, settings.RESET_BUTTON_Y_SIZE)), 2)
        self.screen.blit(self.font.render("RESET", True, (0,0,0)), (settings.RESET_BUTTON_X + 20  , settings.RESET_BUTTON_Y + 10) )

        # Increase number of cells button
        pygame.draw.rect(self.screen, (0,255,100),(settings.INCREASE_CELLS_BUTTON_X, settings.INCREASE_CELLS_BUTTON_Y, settings.INCREASE_CELLS_X_SIZE,settings.INCREASE_CELLS_Y_SIZE))
        pygame.draw.rect(self.screen, (0,150,100),(settings.INCREASE_CELLS_BUTTON_X, settings.INCREASE_CELLS_BUTTON_Y, settings.INCREASE_CELLS_X_SIZE,settings.INCREASE_CELLS_Y_SIZE), 2)
        self.screen.blit(self.font2.render("+", True, (0,0,0)),(settings.INCREASE_CELLS_BUTTON_X  , settings.INCREASE_CELLS_BUTTON_Y  - 12) )

        # Decrease number of cells button
        pygame.draw.rect(self.screen, (200,0,0),(settings.DECREASE_CELLS_BUTTON_X, settings.DECREASE_CELLS_BUTTON_Y, settings.DECREASE_CELLS_X_SIZE,settings.DECREASE_CELLS_Y_SIZE))
        pygame.draw.rect(self.screen, (100,0,0),(settings.DECREASE_CELLS_BUTTON_X, settings.DECREASE_CELLS_BUTTON_Y, settings.DECREASE_CELLS_X_SIZE,settings.DECREASE_CELLS_Y_SIZE),2)
        self.screen.blit(self.font2.render("-", True, (0,0,0)),(settings.DECREASE_CELLS_BUTTON_X  , settings.DECREASE_CELLS_BUTTON_Y  - 12) )

        # Stats text
        self.screen.blit(self.font3.render("Cell Grid Size", True, (200,200,200)), (settings.INCREASE_CELLS_BUTTON_X - 135, settings.INCREASE_CELLS_BUTTON_Y))
        self.screen.blit(self.font3.render("%d x %d" %(self.number_of_Xcells,self.number_of_Ycells), True, (200,200,200)), (settings.INCREASE_CELLS_BUTTON_X - 100, settings.INCREASE_CELLS_BUTTON_Y + 18))

        self.screen.blit(self.font3.render("Living cells  %d" %self.living_cells, True, (200,200,200)), (5, settings.SCREEN_MAP_Y_SIZE + 10))
        self.screen.blit(self.font3.render("Dead cells    %d" %self.dead_cells, True, (200,200,200)), (5, settings.SCREEN_MAP_Y_SIZE + 30))
        self.screen.blit(self.font3.render("Born cells    %d" %self.born_cells, True, (200,200,200)), (5, settings.SCREEN_MAP_Y_SIZE + 50))
        self.screen.blit(self.font4.render("Programmed by D1533", True, (200,200,200)), (settings.SCREEN_MAP_X_SIZE - 150, settings.SCREEN_MAP_Y_SIZE + 60))
    
    def calculateNextGeneration(self):
        for i in range(0, self.number_of_Ycells):
            for j in range(0, self.number_of_Xcells):
                # The cell dies by underpopulation
                if self.map[i][j] == 1 and (self.numberOfNeighbors(i,j) < 2):
                    self.tempMap[i][j] = 0
                    self.living_cells -= 1
                    self.dead_cells += 1
                # The cell lives
                elif self.map[i][j] == 1 and (self.numberOfNeighbors(i,j) == 2 or self.numberOfNeighbors(i,j)== 3):
                    self.tempMap[i][j] = 1
                # The cell dies by overpopulation
                elif self.map[i][j] == 1 and (self.numberOfNeighbors(i,j) > 3):
                    self.tempMap[i][j] = 0
                    self.living_cells -= 1
                    self.dead_cells += 1
                # New cell is born
                elif self.map[i][j] == 0 and self.numberOfNeighbors(i,j) == 3:
                    self.tempMap[i][j] = 1
                    self.living_cells += 1
                    self.born_cells += 1
        # Update the maps
        self.map = self.tempMap
        self.tempMap = [[0 for x in range(self.number_of_Xcells)] for y in range(self.number_of_Ycells)]

    def drawCell(self, pos):
        # Checks if the mouse is in the limits of the map
        if pos[1] < self.number_of_Ycells * self.cellSize:
            if self.map[int(pos[1]/self.cellSize)][int(pos[0]/self.cellSize)] == 0:
                self.map[int(pos[1]/self.cellSize)][int(pos[0]/self.cellSize)] = 1
                self.living_cells += 1

    def eraseCell(self, pos):
        if self.map[int(pos[1]/self.cellSize)][int(pos[0]/self.cellSize)] == 1:
            self.map[int(pos[1]/self.cellSize)][int(pos[0]/self.cellSize)] = 0
            self.living_cells -= 1
    
    def gameBegin(self):
        while self.Start:
            self.calculateNextGeneration()
            self.drawMap()
            self.drawPanel()
            pygame.display.flip()
            pygame.time.wait(settings.NEXT_GENERATION_WAIT_TIME )

            # Checks if pause button is clicked (Start button becomes the pause button when it is set on true)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.StartButton.collidepoint(pos):
                        self.Start = False
                    
    
    def gameReset(self):
        # Resets all the stats values and maps
        self.living_cells = 0
        self.dead_cells = 0
        self.born_cells = 0
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                self.map[i][j] = 0
        self.temp = self.map
    
    def randomPopulation(self):
        self.living_cells = 0
        self.born_cells = 0
        self.dead_cells = 0
        for i in range(self.number_of_Ycells):
            for j in range(self.number_of_Xcells):
                self.map[i][j] = 0
                if random.choice([0, 1]):
                    self.map[i][j] = 1
                    self.living_cells += 1

   