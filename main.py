""" Made to imitate https://twitter.com/_Rasmus_Clausen/status/1157615234913308672"""
import pygame as pg
from pygame import draw, mouse
from pygame.locals import MOUSEBUTTONDOWN
from random import randint, seed
from typing import Tuple
from vec2d import Vec2d


def gen_points(amount: int, x_range: Tuple[int, int], y_range: Tuple[int, int], random_seed=42):
    seed(random_seed)
    return [(randint(*x_range), randint(*y_range)) for _ in range(amount)]


def get_line_from_mouse(width, height):
    mx, my = mouse.get_pos()
    cx, cy = (width / 2, height / 2)
    # Function is ax + b = y
    if mx - cx != 0:
        a = (my - cy) / (mx - cx)
    else:
        a = (my - cy) / 0.01
    b = my - (a * mx)
    def f(x): return a * x + b
    return f


def dot_product(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]


def project(v1: Vec2d, v2: Vec2d) -> Vec2d:
    return v2 * (v1.dot_product(v2) / (v2.length ** 2))


if __name__ == "__main__":
    sw, sh = (700, 700)
    # setup
    pg.init()
    screen = pg.display.set_mode((sw, sh))
    pg.mouse.set_visible(1)
    bg = pg.Surface(screen.get_size()).convert()

    points = gen_points(10, (0, sw), (0, sh))

    running = True
    while running:  # mainloop
        for event in pg.event.get():
            if event.type == MOUSEBUTTONDOWN:
                print("regenning")
                points = gen_points(10, (0, sw), (0, sh), random_seed=None)

        bg.fill(0xFFFFFF)

        line = get_line_from_mouse(sw, sh)
        line_vec = Vec2d(sw, line(sw))
        O = Vec2d(0, line(0))
        line_vec_O = (line_vec - O)
        for p in points:
            # Get a point
            draw.circle(bg, 0xFF0000, p, 5)
            # now calc a projection
            p = Vec2d(*p)
            p_O = p - O
            p_proj_O = project(p_O, line_vec_O)
            p_proj = p_proj_O + O
            draw.line(bg, 0x00FF00, (int(p.x), int(p.y)),
                      (int(p_proj.x), int(p_proj.y)))

        draw.line(bg, 0x0000FF, (0, line(0)),
                  (int(line_vec.x), int(line_vec.y)))

        screen.blit(bg, (0, 0))
        pg.display.flip()
