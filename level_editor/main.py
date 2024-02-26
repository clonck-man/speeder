import pygame

import engine.window
import utils
from utils import save_walls
from component import point, wall
from engine.window import Window


def get_triggered_component(triggered_point, component_list):
    triggered_points = [c for c in component_list if c.check_if_triggered(triggered_point)]
    if len(triggered_points) == 1:
        return triggered_points[0]
    else:
        return None


class level_editor(Window):
    def __init__(self):
        super().__init__("Level Editor")

        self.previous_click_state = False
        self.previous_key_state = False
        self.adding_checkpoints = False

        self.points = []
        self.walls = []
        self.checkpoints = []

        self.active_component = None

    def logic(self, dt, events, pressed):
        # Keyboards Events
        if pressed[pygame.K_s]:
            save_walls("level.json", engine.window.PPU, self.walls, self.checkpoints)
        elif pressed[pygame.K_r]:
            if isinstance(self.active_component, point):
                if self.active_component in self.points:
                    self.points.remove(self.active_component)
                    self.walls = [w for w in self.walls if w not in self.active_component.walls]
                    self.checkpoints = [c for c in self.checkpoints if c not in self.active_component.checkpoints]

            elif isinstance(self.active_component, wall):
                if self.active_component in self.walls:
                    self.walls.remove(self.active_component)

            self.active_component = None
        elif pressed[pygame.K_c]:
            if not self.previous_key_state:
                self.adding_checkpoints = not self.adding_checkpoints
                self.previous_key_state = True
        else:
            self.previous_key_state = False

        # Mouses Events
        mouse_event = None
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN \
                    or e.type == pygame.MOUSEBUTTONUP \
                    or e.type == pygame.MOUSEWHEEL \
                    or e.type == pygame.MOUSEMOTION:
                mouse_event = e

        if not mouse_event:
            pass
        elif mouse_event.type == pygame.MOUSEBUTTONDOWN and not self.previous_click_state:
            pos = engine.window.pixel_to_unite(mouse_event.pos)

            if mouse_event.button == 1:  # Clic gauche de la souris (pose un pts, active/désactive un pts)
                component = get_triggered_component(pos, self.points + self.walls)

                if component:
                    if self.active_component == component:
                        pass
                    elif self.adding_checkpoints and self.active_component:
                        p1 = component
                        p2 = self.active_component
                        checkpoint = wall(p1.position, p2.position, width=5)

                        self.checkpoints.append(checkpoint)
                        p1.checkpoints.append(checkpoint)
                        p2.checkpoints.append(checkpoint)

                        self.active_component = None
                    else:
                        self.active_component = component
                else:
                    self.active_component = None

                self.previous_click_state = True

            elif mouse_event.button == 3:  # Clic droit de la souris
                if not get_triggered_component(pos, self.points + self.walls):
                    pts = point(pos)
                    self.points.append(pts)

                    if self.active_component and isinstance(self.active_component, point):
                        p1 = pts
                        p2 = self.active_component

                        w = wall(p1.position, p2.position, width=5)
                        self.walls.append(w)
                        p1.walls.append(w)
                        p2.walls.append(w)

                    self.active_component = pts

                self.previous_click_state = True
        elif mouse_event.type == pygame.MOUSEBUTTONUP:
            self.previous_click_state = False

    def draw(self):
        self.screen.fill((0, 0, 0))

        for c in self.walls:
            c.draw(self.screen)

        for c in self.checkpoints:
            c.draw(self.screen, color=utils.YELLOW)

        for c in self.points:
            c.draw(self.screen, color=utils.BLUE)

        if self.active_component:
            self.active_component.draw(self.screen, utils.GREEN)

    def update_board(self):
        self.board["nbr_pts"] = len(self.points)
        self.board["nbr_wall"] = len(self.walls)
        self.board["active_compo"] = self.active_component.position if self.active_component else "None"
        self.board["ajout_checkpnts"] = self.adding_checkpoints


if __name__ == '__main__':
    lvl = level_editor()
    lvl.run()
