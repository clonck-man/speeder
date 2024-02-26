import json

import pygame

from engine.window import Window
from engine.window import unite_to_pixel, PPU

import utils
from utils import draw_segments

import random


def coordonnee_valide(i, j, min_i, max_i, min_j, max_j):
    return min_i <= i <= max_i and min_j <= j <= max_j


def cases_autour(i, j, min_i, max_i, min_j, max_j):
    cases = []
    if coordonnee_valide(i-1, j, min_i, max_i, min_j, max_j):
        cases.append((i-1, j))
    if coordonnee_valide(i+1, j, min_i, max_i, min_j, max_j):
        cases.append((i+1, j))
    if coordonnee_valide(i, j-1, min_i, max_i, min_j, max_j):
        cases.append((i, j-1))
    if coordonnee_valide(i, j+1, min_i, max_i, min_j, max_j):
        cases.append((i, j+1))
    return cases


def generate_terrain(lim_w, lim_h, min, max):
    i, j = random.randint(0, lim_w), random.randint(0, lim_h)
    cells = [(i, j)]

    for num in range(max):
        i, j = cells[len(cells)-1]
        c = [c for c in cases_autour(i, j, 0, lim_w, 0, lim_h) if c not in cells]

        if len(c) == 0:
            if len(cells) < min:
                return generate_terrain(lim_w, lim_h, min, max)
            else:
                return cells
        else:
            cells.append(c[random.randint(0, len(c)-1)])

    return cells


def determiner_tuiles(cells, tuiles):
    res = []

    x1, y1 = cells[0]
    x2, y2 = cells[1]
    if x1 == x2:
        if y1 < y2:
            res.append(tuiles["D1"])
        elif y1 > y2:
            res.append(tuiles["D3"])
        else:
            print("TODO_1")
    elif y1 == y2:
        if x1 < x2:
            res.append(tuiles["D2"])
        elif x1 > x2:
            res.append(tuiles["D4"])
        else:
            print("TODO_2")

    for i in range(1, len(cells) - 1):
        x1, y1 = cells[i - 1]
        x2, y2 = cells[i]
        x3, y3 = cells[i + 1]

        if x1 == x2 < x3 or x1 > x2 == x3:
            if y1 > y2 == y3 or y1 == y2 < y3:
                res.append(tuiles["R1"])
            elif y1 < y2 == y3 or y1 == y2 > y3:
                res.append(tuiles["R4"])
            else:
                print("TODO_1")
        elif x1 == x2 > x3 or x1 < x2 == x3:
            if y1 < y2 == y3 or y1 == y2 > y3:
                res.append(tuiles["R3"])
            elif y1 > y2 == y3 or y1 == y2 < y3:
                res.append(tuiles["R2"])
            else:
                print("TODO_2")
        elif x1 == x2 == x3:
            res.append(tuiles["S1"])
        elif y1 == y2 == y3:
            res.append(tuiles["S2"])
        else:
            print("TODO_3")

    x1, y1 = cells[len(cells)-2]
    x2, y2 = cells[len(cells)-1]
    if x1 == x2:
        if y1 < y2:
            res.append(tuiles["A3"])
        elif y1 > y2:
            res.append(tuiles["A1"])
        else:
            print("TODO_1")
    elif y1 == y2:
        if x1 < x2:
            res.append(tuiles["A4"])
        elif x1 > x2:
            res.append(tuiles["A2"])
        else:
            print("TODO_2")

    return res


def get_wall_checkpoint(field, tuiles):
    walls, ck = [], []

    for i in range(len(field)):
        x, y = field[i]
        t_s = tuiles[i]["SG"]
        t_c = tuiles[i]["CK"]

        for p1, p2 in coords_liste_points_tuile(t_s, x, y, 6):
            walls.append((p1, p2))

        ck.append(coords_liste_points_tuile([t_c], x, y, 6)[0])

    return walls, ck


def coords_point_tuile(i, j, taille_tuile):
    x = i * taille_tuile
    y = j * taille_tuile
    return x, y


def coords_liste_points_tuile(segments, i, j, taille_tuile):
    x_offset, y_offset = coords_point_tuile(i, j, taille_tuile)
    return [(((x1 + x_offset), (y1 + y_offset)), ((x2 + x_offset), (y2 + y_offset))) for (x1, y1), (x2, y2) in segments]


def segments_unite_to_px(segments):
    return [(unite_to_pixel(p1), unite_to_pixel(p2)) for p1, p2 in segments]


def load_tuiles():
    with open('tuiles.json', 'r') as f:
        data = json.load(f)

    return data


def create_terrain_no_gui(lim_w=5, lim_h=2, min=10, max=30):
    tuiles_templates = load_tuiles()

    field = generate_terrain(lim_w, lim_h, min, max)
    tuiles = determiner_tuiles(field, tuiles_templates)

    walls, checkpoints = get_wall_checkpoint(field, tuiles)

    utils.save_walls_bis("level.json", PPU, walls, checkpoints)


class level_generator(Window):
    def __init__(self):
        super().__init__("Level Editor")

        self.t_w, self.t_h, self.m_w, self.m_h = self.init_tab()

        self.tuiles_templates = load_tuiles()

        self.field = generate_terrain(5, 2, 10, 30)
        self.tuiles = determiner_tuiles(self.field, self.tuiles_templates)

        self.walls, self.checkpoints = get_wall_checkpoint(self.field, self.tuiles)

    def init_tab(self):
        w, h = self.screen.get_width(), self.screen.get_height()

        t_w, t_h = (w // PPU), (h // PPU)
        m_w, m_h = (w % PPU) / 2, (h % PPU) + PPU / 2

        return t_w, t_h, m_w, m_h

    def generate_terrain(self):
        self.field = generate_terrain(5, 2, 10, 30)
        self.tuiles = determiner_tuiles(self.field, self.tuiles_templates)

        self.walls, self.checkpoints = get_wall_checkpoint(self.field, self.tuiles)

    def logic(self, dt, events, pressed):
        if pressed[pygame.K_r]:
            self.generate_terrain()
        if pressed[pygame.K_s]:
            utils.save_walls_bis("level.json", PPU, self.walls, self.checkpoints)

    def draw(self):
        self.screen.fill((0, 0, 0))

        draw_segments(self.screen, utils.RED, segments_unite_to_px(self.walls), convert_px=False)
        draw_segments(self.screen, utils.YELLOW, segments_unite_to_px(self.checkpoints), convert_px=False)

    def update_board(self):
        # self.board["nbr_pts"] = len(self.points)
        pass


if __name__ == '__main__':
    lvl = level_generator()
    lvl.run()
