import pygame
import os
from math import sin, radians, degrees, copysign, hypot
from pygame.math import Vector2

import utils
from utils import calculate_rectangle_corners, create_ray, draw_segments

from engine.window import PPU, unite_to_pixel


RAY_SIZE = 10
CAR_FOV = 180


class Car:
    def __init__(self, x, y, dim=(1.25, 0.625), angle=0.0, length=0.5, max_steering=30, max_acceleration=5.0):
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imgs/car_1.png")
        img = pygame.image.load(image_path)

        dimW, dimH = dim
        self.img = pygame.transform.scale(img, (dimW * PPU, dimH * PPU))
        self.car_size = dim

        self.position = Vector2(x, y)
        self.velocity = 0.0
        self.acceleration = 0.0
        self.steering = 0.0

        self.angle = angle
        self.steering_length = length

        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 8
        self.brake_deceleration = 10
        self.free_deceleration = 2

    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.velocity = max(-self.max_velocity, min(self.velocity, self.max_velocity))

        if self.steering:
            turning_radius = self.steering_length / sin(radians(self.steering))
            angular_velocity = self.velocity / turning_radius
        else:
            angular_velocity = 0

        self.position += Vector2(self.velocity, 0).rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

    def control(self, dt, accelerate, brake, steer_left, steer_right):
        if accelerate:
            self.set_acceleration(dt, 1)
        else:
            self.coast(dt, brake_mode=brake)

        if steer_left != steer_right:
            s_factor = 1 if steer_left else -1 if steer_right else 0
            self.steer(dt, s_factor)
        else:
            self.steer(dt, 0)

    def set_acceleration(self, dt, factor):
        """
        :param dt:
        :param factor:
        :return:
        """
        if (self.velocity < 0 and factor > 0) or (self.velocity > 0 and factor < 0):
            self.acceleration = factor * self.brake_deceleration
        else:
            self.acceleration += factor * dt

        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

    def coast(self, dt, brake_mode=False):
        deceleration = self.free_deceleration if not brake_mode else self.brake_deceleration

        if abs(self.velocity) > dt * deceleration:
            self.acceleration = -copysign(deceleration, self.velocity)
        elif dt != 0:
            self.acceleration = -self.velocity / dt

        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

    def steer(self, dt, direction):
        """
        :param dt:
        :param direction: 1 for left, -1 for right
        :return:
        """
        self.steering = self.steering + 30 * dt * direction if direction != 0 else 0
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

    def draw(self, screen, show_corner=False, show_ray=False):
        rotated = pygame.transform.rotate(self.img, self.angle)
        rect = rotated.get_rect()
        screen.blit(rotated, self.position * PPU - (rect.width / 2, rect.height / 2))

        if show_corner:
            for corner in self.get_corners(px=True):
                pygame.draw.circle(screen, utils.GREEN, corner, 5)
        if show_ray:
            draw_segments(screen, utils.BLUE, self.get_ray())

    def get_corners(self, px=False):
        corners = calculate_rectangle_corners(self.position, self.car_size, self.angle)

        if px:
            return [unite_to_pixel(corner) for corner in corners]
        return corners

    def get_segments(self):
        corners = self.get_corners()
        return [(corners[i], corners[(i + 1) % len(corners)]) for i in range(len(corners))]

    def get_rays(self, nbr_ray=9, size_ray=RAY_SIZE, fov=CAR_FOV):
        gap = fov / (nbr_ray - 1)
        start_angle = self.angle - fov / 2

        return [(self.position, create_ray(self.position, start_angle + gap * n, size_ray)) for n in range(nbr_ray)]

    def get_view(self, walls, return_dist=False):
        rays = self.get_rays()
        view = []
        for ray in rays:
            collisions = utils.get_collisions(ray, walls)
            pts = utils.get_nearest_point(self.position, collisions)
            pts = pts if pts else ray[1]
            view.append(pts)

        if return_dist:
            view = [hypot(v[0] - self.position[0], v[1] - self.position[1]) for v in view]

        return view
