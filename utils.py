import math
import json
import os
import pygame

from engine.window import unite_to_pixel

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def rotate_point(x, y, cx, cy, angle_deg):
    """
    Fait tourner le point x,y de 'angle_deg' autour du point cx,cy
    :param x:
    :param y:
    :param cx:
    :param cy:
    :param angle_deg:
    :return:
    """
    angle_rad = math.radians(-angle_deg)

    new_x = math.cos(angle_rad) * (x - cx) - math.sin(angle_rad) * (y - cy) + cx
    new_y = math.sin(angle_rad) * (x - cx) + math.cos(angle_rad) * (y - cy) + cy
    return new_x, new_y


def calculate_rectangle_corners(position, dimension, rotation_angle):
    """
    Détermine les coordonées des coins d'un rectangle
    :param position: position du rectangle
    :param dimension: dimension du rectangle
    :param rotation_angle: orientation du rectangle
    :return: list de x,y
    """
    center_x, center_y = position
    length, width = dimension

    half_length = length / 2
    half_width = width / 2

    top_left = (center_x - half_length, center_y + half_width)
    top_right = (center_x + half_length, center_y + half_width)
    bottom_left = (center_x - half_length, center_y - half_width)
    bottom_right = (center_x + half_length, center_y - half_width)

    rotated_top_left = rotate_point(*top_left, center_x, center_y, rotation_angle)
    rotated_top_right = rotate_point(*top_right, center_x, center_y, rotation_angle)
    rotated_bottom_left = rotate_point(*bottom_left, center_x, center_y, rotation_angle)
    rotated_bottom_right = rotate_point(*bottom_right, center_x, center_y, rotation_angle)

    return rotated_top_left, rotated_top_right, rotated_bottom_left, rotated_bottom_right


def on_segment(p, q, r):
    """
    Détermine si un point q est sur le segment p,r
    :param p:
    :param q:
    :param r:
    :return: Boolean
    """
    if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
            (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
        return True
    return False


def orientation(p, q, r):
    """
    Détermine si les points p,q et r forme un virage ou si ils sont alignés
    :param p:
    :param q:
    :param r:
    :return:
    """
    val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
    if val > 0:
        return 1
    elif val < 0:
        return 2
    else:
        return 0


def do_intersect(p1, q1, p2, q2):
    """
    Détermine si les segments p1,q1 et p2,q2 se croisent
    :param p1:
    :param q1:
    :param p2:
    :param q2:
    :return: Boolean
    """
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if (o1 != o2) and (o3 != o4):
        return True

    if (o1 == 0) and on_segment(p1, p2, q1):
        return True

    if (o2 == 0) and on_segment(p1, q2, q1):
        return True

    if (o3 == 0) and on_segment(p2, p1, q2):
        return True

    if (o4 == 0) and on_segment(p2, q1, q2):
        return True

    return False


def intersect_pts(p1, q1, p2, q2):
    """
    Détermine le point d'intersection des segments p1,q1 et p2,q2
    :param p1:
    :param q1:
    :param p2:
    :param q2:
    :return: x,y
    """
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if (o1 != o2) and (o3 != o4):
        x_intersect = ((p1[0] * q1[1] - p1[1] * q1[0]) * (p2[0] - q2[0]) -
                       (p1[0] - q1[0]) * (p2[0] * q2[1] - p2[1] * q2[0])) / \
                      ((p1[0] - q1[0]) * (p2[1] - q2[1]) - (p1[1] - q1[1]) * (p2[0] - q2[0]))
        y_intersect = ((p1[0] * q1[1] - p1[1] * q1[0]) * (p2[1] - q2[1]) -
                       (p1[1] - q1[1]) * (p2[0] * q2[1] - p2[1] * q2[0])) / \
                      ((p1[0] - q1[0]) * (p2[1] - q2[1]) - (p1[1] - q1[1]) * (p2[0] - q2[0]))

        return x_intersect, y_intersect

    return None


def get_collisions(segment, segments, return_segment=False):
    p1, p2 = segment

    collisions = []
    for s in segments:
        p3, p4 = s

        pts = intersect_pts(p1, p2, p3, p4)
        if pts:
            if return_segment:
                collisions.append(s)
            else:
                collisions.append(pts)
    return list(set(collisions))


def get_all_collisions(segments_1, segments_2, return_segment=False):
    """
    Détermine tout les points de collisions entre la list de segment segments_1 la list de segment segments_2
    :param return_segment:
    :param segments_1:
    :param segments_2:
    :return:
    """
    collisions = []
    for s in segments_1:
        collisions.extend(get_collisions(s, segments_2, return_segment))

    return list(set(collisions))


def get_collision_by_segments(segments_1, segments_2, return_segment=False):
    """
    Pour chaque segment de la list segments_1, détermine sa list de collisions avec la list de segment segments_2
    :param return_segment:
    :param segments_1:
    :param segments_2:
    :return:
    """
    collisions = []
    for s in segments_1:
        collisions.append(get_collisions(s, segments_2, return_segment))

    return collisions


def get_nearest_point(origin, points):
    """
    Détermine le point le plus proche de l'origine
    :param origin: x,y
    :param points: list[(x,y), ...]
    :return: x,y
    """
    min_distance = float('inf')
    nearest_point = None

    for point in points:
        dist = math.hypot(point[0] - origin[0], point[1] - origin[1])
        if dist < min_distance:
            min_distance = dist
            nearest_point = point

    return nearest_point


def get_nearest_points(origin, points):
    """
    Pour chaque list de point de points, détermine le point le plus proche de l'origine
    :param origin:
    :param points:
    :return:
    """
    return [get_nearest_point(origin, p) for p in points]


def center_between_points(p1, p2):
    """
    Détermine le centre du segment p1,p2
    :param p1: x,y
    :param p2: x,y
    :return: x,y
    """
    center_x = (p1[0] + p2[0]) / 2
    center_y = (p1[1] + p2[1]) / 2

    return center_x, center_y


def create_ray(p, angle, size):
    """
    Créer un segment d'origine p, de direction angle et de taille size
    :param p: x,y
    :param angle: degré
    :param size: x
    :return: p,p2
    """
    angle_radians = math.radians(angle)

    x1, y1 = p

    x2 = x1 + size * math.cos(-angle_radians)
    y2 = y1 + size * math.sin(-angle_radians)

    return x2, y2


def save_walls(filename, ppu, walls, checkpoints):
    data = {
        "ppu": ppu,
        "walls": [],
        "checkpoints": []
    }

    for w in walls:
        p1, p2 = w
        data["walls"].append({"p1": p1, "p2": p2})

    for c in checkpoints:
        p1, p2 = c
        data["checkpoints"].append({"p1": p1, "p2": p2})

    path = os.path.dirname(os.path.abspath(__file__))
    # path = os.path.dirname(os.getcwd())
    json_path = os.path.join(path, filename)

    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)


def load_walls(filename="level.json"):
    path = os.path.dirname(os.path.abspath(__file__))
    # path = os.path.dirname(os.getcwd())
    json_path = os.path.join(path, filename)

    with open(json_path, "r") as file:
        data = json.load(file)

    walls = [(tuple(wall["p1"]), tuple(wall["p2"])) for wall in data["walls"]]
    checkpoints = [(tuple(checkpoints["p1"]), tuple(checkpoints["p2"])) for checkpoints in data["checkpoints"]]

    return walls, checkpoints


def draw_segment(screen, color, segment, thickness=3, convert_px=True):
    p1, p2 = segment
    if convert_px:
        pygame.draw.line(screen, color, unite_to_pixel(p1), unite_to_pixel(p2), thickness)
    else:
        pygame.draw.line(screen, color, p1, p2, thickness)


def draw_segments(screen, color, segments, thickness=3, convert_px=True):
    """
    Dessine une list de segments
    :param convert_px:
    :param screen:
    :param color:
    :param segments:
    :param thickness:
    :return:
    """
    for segment in segments:
        draw_segment(screen, color, segment, thickness=thickness, convert_px=convert_px)
