#      ==========================================
#      IMPORTS
#      ==========================================

import pygame
from pygame.locals import *

#      ==========================================
#      INITIALYZE PYGAME
#      ==========================================

pygame.init()

screen_width = 300
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
#   Set window resolution
pygame.display.set_caption("They see me toein'")
#   Game title

#      ==========================================
#      GLOBAL GAME VARIABLES
#      ==========================================

line_width = 6
markers = []
#   3x3 to save game state
clicked = False
pos = []
player = 1
#   1 = player X (green), -1 = player O (red)
winner = 0
game_over = False

#      ==========================================
#      COLORS (RGB)
#      ==========================================

green = (0, 255, 0)
red = (255, 0, 0)

#      ==========================================
#      DRAWING AND GAMEPLAY FUNCTION
#      ==========================================


def draw_grid():
    #   Draw a white background and lines on 3x3 grid
    bg = (255, 255, 255)
    grid = (50, 50, 50)
    screen.fill(bg)

    #   Draw 2 horizontals and 2 verticals lines
    for x in range(1, 3):
        pygame.draw.line(screen, grid, (0, x * 100),
                         (screen_width, x * 100), line_width)
        pygame.draw.line(screen, grid, (x * 100, 0),
                         (x * 100, screen_height), line_width)


def draw_markers():
    #   Browse grid and draw X or O depending game state
    x_pos = 0
    for x in markers:
        #   For every row
        y_pos = 0
        for y in x:
            #   For every column
            if y == 1:
                #   If cell contains 1, draw X
                pygame.draw.line(screen, green,
                                 (x_pos * 100 + 15, y_pos * 100 + 15),
                                 (x_pos * 100 + 85, y_pos * 100 + 85), line_width)
                pygame.draw.line(screen, green,
                                 (x_pos * 100 + 15, y_pos * 100 + 85),
                                 (x_pos * 100 + 85, y_pos * 100 + 15), line_width)
            if y == -1:
                #   If cell contains -1, draw O
                pygame.draw.circle(screen, red,
                                   (x_pos * 100 + 50, y_pos * 100 + 50), 38, line_width)
            y_pos += 1
        x_pos += 1


def check_winner():

    global winner
    global game_over

    y_pos = 0
    for x in markers:
        #   check columns
        if sum(x) == 3:
            winner = 1
            game_over = True
        if sum(x) == -3:
            winner = 2
            game_over = True
            
        #   check rows
        if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == 3:
            winner = 1
            game_over = True
        if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == -3:
            winner = 2
            game_over = True
        y_pos += 1

    # check diagonals
    if markers[0][0] + markers[1][1] + markers[2][2] == 3\
            or markers[2][0] + markers[1][1] + markers[0][2] == 3:
        winner = 1
        game_over = True
    if markers[0][0] + markers[1][1] + markers[2][2] == -3\
            or markers[2][0] + markers[1][1] + markers[0][2] == -3:
        winner = 2
        game_over = True


#      ==========================================
#      INITIATE EMPTY GRID 3x3
#      ==========================================

for x in range(3):
    row = [0] * 3
    #   0 means empty cell
    markers.append(row)

#      ==========================================
#      PRINCIPAL LOOP
#      ==========================================

running = True
while running:

    draw_grid()
    draw_markers()

    for event in pygame.event.get():
        #   Events Management
        if event.type == pygame.QUIT:
            running = False
        if game_over == 0:
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                #   Detect mouse click
                clicked = True

            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                pos = pygame.mouse.get_pos()
                cell_x = pos[0]
                cell_y = pos[1]

                if markers[cell_x // 100][cell_y // 100] == 0:
                    #   Verify if cell is empty
                    markers[cell_x // 100][cell_y // 100] = player
                    #   Alternate between 1 and -1 (X and O)
                    player *= -1
                    check_winner()

    pygame.display.update()
    #   Refresh screen

pygame.quit()
