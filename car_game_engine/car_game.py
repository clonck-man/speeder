import pygame
import math

from car_game_engine.car import Car

import utils
from utils import load_walls, get_all_collisions, center_between_points, draw_segments

from engine.window import Window
from engine.window import unite_to_pixel


def get_spawn(checkpoints):
    x, y = (0, 0)
    if len(checkpoints) >= 1:
        p1, p2 = checkpoints[0]
        x, y = center_between_points(p1, p2)

    angle = 0.0
    if len(checkpoints) >= 2:
        p1, p2 = checkpoints[0]
        p3, p4 = checkpoints[1]

        c1, c2 = center_between_points(p1, p2)
        c3, c4 = center_between_points(p3, p4)

        angle = math.degrees(math.atan2(c3 - c1, c4 - c2) + 3 * math.pi / 2)

    return x, y, angle


class Game(Window):
    def __init__(self):
        super().__init__("Car Game")

        self.walls, self.checkpoints = load_walls()
        self.validated_checkpoints = []

        x, y, angle = get_spawn(self.checkpoints)

        self.car = Car(x, y, angle=angle)

        self.crash = False
        self.victory = False

    def __reset__(self):
        self.walls, self.checkpoints = load_walls()
        self.validated_checkpoints = []

        x, y, angle = get_spawn(self.checkpoints)
        self.car = Car(x, y, angle=angle)

        self.crash = False
        self.victory = False

    def logic(self, dt, events, pressed):
        up = pressed[pygame.K_UP],
        down = pressed[pygame.K_DOWN],
        left = pressed[pygame.K_LEFT],
        right = pressed[pygame.K_RIGHT]

        outputs_flat = []
        for element in [up, down, left, right, False]:
            if isinstance(element, tuple):
                outputs_flat.append(element[0])
            else:
                outputs_flat.append(element)

        self.logic_blind(dt, outputs_flat)

    def logic_blind(self, dt, inputs):
        if inputs[4]:
            self.car.control(dt, False, False, False, False)
        else:
            self.car.control(dt, inputs[0], inputs[1], inputs[2], inputs[3])

        self.car.update(dt)

        collide_walls = get_all_collisions(self.car.get_segments(), self.walls)
        collide_checkpoint = get_all_collisions(self.car.get_segments(), self.checkpoints, return_segment=True)

        self.crash = len(collide_walls) != 0

        self.validated_checkpoints.extend([c for c in collide_checkpoint if c not in self.validated_checkpoints])
        self.victory = len(self.validated_checkpoints) == len(self.checkpoints)

    def draw(self):
        self.screen.fill((0, 0, 0))

        draw_segments(self.screen, utils.PURPLE, self.walls)
        draw_segments(self.screen, utils.BLUE, self.checkpoints)
        draw_segments(self.screen, utils.GREEN, [self.checkpoints[len(self.checkpoints) - 1]])

        self.car.draw(self.screen, show_ray=False)

        for pts in self.car.get_view(self.walls):
            pygame.draw.circle(self.screen, utils.GREEN, unite_to_pixel(pts), 5)

    def update_board(self):
        self.board["car_position"] = self.car.position
        self.board["car_velocity"] = self.car.velocity
        self.board["validated_checkpoints"] = len(self.validated_checkpoints)
        self.board["crash"] = self.crash
        self.board["victory"] = self.victory


if __name__ == '__main__':
    game = Game()
    game.run()
