import time
import pygame


class Engine:
    def __init__(self, scene, fps=90, antialiasing=False):
        self.fps = fps
        self.dt = 1.0 / fps
        self.running = False
        self.screen = None
        self.width = 0
        self.height = 0
        self.antialiasing = antialiasing
        self.scene = scene  # Whatever we want to render gets passed in

    def start(self):
        pygame.init()

        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h - 60

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Physics Engine")

        # Give the scene access to the engine so it can draw
        self.scene.engine = self

        self.running = True
        self._loop()

    def _loop(self):
        draw_interval = 1_000_000_000 / self.fps
        delta = 0.0
        last_time = time.time_ns()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            current_time = time.time_ns()
            delta += (current_time - last_time) / draw_interval
            last_time = current_time

            if delta >= 1:
                self.scene.update(self.dt)
                self.screen.fill((10, 10, 12))
                self.scene.render(self.screen)
                pygame.display.flip()
                delta -= 1

        pygame.quit()

    def draw_line(self, surface, color, start, end, width=2):
        """Central draw line — respects antialiasing toggle."""
        if self.antialiasing:
            pygame.draw.aaline(surface, color, start, end)
        else:
            pygame.draw.line(surface, color, start, end, width)