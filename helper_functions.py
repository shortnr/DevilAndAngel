import numpy as np
import pygame as pg
from constants import *


def get_agent_inputs(board, bomb, robot):
    x_dist = abs(robot.x - bomb.x)
    y_dist = abs(robot.y - bomb.y)
    cell_1 = board[robot.x + 1][robot.y]
    cell_2 = board[robot.x + 1][robot.y - 1]
    cell_3 = board[robot.x + 2][robot.y]
    cell_4 = board[robot.x + 2][robot.y - 1]
    cell_5 = board[robot.x + 2][robot.y - 2]
    cell_6 = board[robot.x + 3][robot.y]
    cell_7 = board[robot.x + 3][robot.y - 1]
    cell_8 = board[robot.x + 3][robot.y - 2]
    cell_9 = board[robot.x + 3][robot.y - 3]
    cell_10 = board[robot.x + 4][robot.y]
    cell_11 = board[robot.x + 4][robot.y - 1]
    cell_12 = board[robot.x + 4][robot.y - 2]
    cell_13 = board[robot.x + 4][robot.y - 3]
    cell_14 = board[robot.x + 4][robot.y - 4]
    inputs = np.array([x_dist, y_dist, cell_1, cell_2, cell_3, cell_4,
                       cell_5, cell_6, cell_7, cell_8, cell_9, cell_10,
                       cell_11, cell_12, cell_13, cell_14])
    return inputs


def draw_grid(screen):
    for x in range(0, cell_width * num_cells, cell_width):
        for y in range(0, cell_height * num_cells, cell_height):
            square = pg.Rect(950 + x, 50 + y, cell_width + 1, cell_height + 1)
            if (x + y) / cell_height % 2 == 0:
                pg.draw.rect(screen, MEDIUM_GRAY, square, 0)
            else:
                pg.draw.rect(screen, WHITE, square, 0)

    border = pg.Rect(948, 48, num_cells * cell_width + 4, num_cells * cell_height + 4)
    pg.draw.rect(screen, BLACK, border, 3)


def gen_text(font, text):
    return font.render(text, True, BLACK, LIGHT_GRAY)


def draw_sprite(screen, sprite, x, y):
    sp = pg.Rect(951 + x * (sprite_width + 1), 51 + y * (sprite_height + 1), sprite_width - 1, sprite_height - 1)
    pg.draw.rect(screen, sprite, sp, 0)


def population_sort(e):
    return e[2]
