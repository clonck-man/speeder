import math

import engine.window
import utils
import pygame


class component:
    def __init__(self, position, thickness):
        self.position = position
        self.thickness = thickness

    def distance(self, p):
        x1, y1 = engine.window.unite_to_pixel(self.position)
        x2, y2 = engine.window.unite_to_pixel(p)

        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def draw(self, screen):
        pass


class point(component):
    def __init__(self, position, radius=5):
        super().__init__(position, radius)

        self.walls = []
        self.checkpoints = []

    def check_if_triggered(self, triggered_point):
        dist = self.distance(triggered_point)
        return dist <= self.thickness

    def draw(self, screen, color=utils.RED):
        pygame.draw.circle(screen, color, engine.window.unite_to_pixel(self.position), self.thickness)


class wall(component):
    def __init__(self, p1, p2, width=5):
        x1, y1 = p1
        x2, y2 = p2

        position = ((x1 + x2) / 2, (y1 + y2) / 2)  # Position of the wall midpoint
        length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # Length of the wall
        rotation = math.degrees(math.atan2(y2 - y1, x2 - x1))  # Rotation angle
        super().__init__(position, width)

        self.rotation = rotation
        self.length = length

        self.p1 = p1
        self.p2 = p2

    def check_if_triggered(self, triggered_point):
        x, y = engine.window.unite_to_pixel(triggered_point)
        px, py = engine.window.unite_to_pixel(self.position)

        # Rotate the point based on the wall's rotation
        x_rot = (x - px) * math.cos(math.radians(self.rotation)) + (y - py) * math.sin(math.radians(self.rotation)) + px
        y_rot = -(x - px) * math.sin(math.radians(self.rotation)) + (y - py) * math.cos(math.radians(self.rotation)) + py

        # Check if the rotated point is within the rectangle
        within_x = px <= x_rot <= px + self.length
        within_y = py - self.thickness / 2 <= y_rot <= py + self.thickness / 2
        return within_x and within_y

    def draw(self, screen, color=utils.RED):
        pygame.draw.line(screen, color, engine.window.unite_to_pixel(self.p1), engine.window.unite_to_pixel(self.p2), self.thickness)
