import pygame

PPU = 32


def unite_to_pixel(coo):
    x_pixel = coo[0] * PPU
    y_pixel = coo[1] * PPU
    return x_pixel, y_pixel


def pixel_to_unite(coo):

    x_unite = coo[0] / PPU
    y_unite = coo[1] / PPU
    return x_unite, y_unite


class Window:
    def __init__(self, name, resolution=(1280, 720), ticks=60):
        pygame.init()
        pygame.font.init()

        self.font = pygame.font.Font(None, 24)

        pygame.display.set_caption(name)

        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.ticks = ticks

        self.board = {}

        self.exit = False

    def run(self):
        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            events = pygame.event.get()
            pressed = pygame.key.get_pressed()

            for event in events:
                if event.type == pygame.QUIT:
                    self.exit = True

            self.logic(dt, events, pressed)
            self.update_board()

            self.draw()
            self.display_board()

            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()

    def logic(self, dt, events, pressed):
        pass

    def draw(self):
        pass

    def display_board(self):
        i = 0
        for key, value in self.board.items():
            self.screen.blit(
                self.font.render(
                    f"{key} : {value}",
                    1,
                    (255, 255, 255)),
                (0, self.font.get_linesize()*i)
            )
            i = i+1

    def update_board(self):
        pass

    def add_to_board(self, key, value):
        self.board[key] = value


if __name__ == '__main__':
    window = Window("Hello World")
    window.run()
