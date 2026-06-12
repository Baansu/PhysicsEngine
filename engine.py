import time
import pygame
from core.vector import Vec3


class Engine:
    def __init__(self, fps=90, antialiasing=False):
        self.fps = fps
        self.dt = 1.0 / fps
        self.running = False
        self.screen = None
        self.width = 0
        self.height = 0
        self.antialiasing = antialiasing  # Toggle: True = smooth, False = raw/pixelated

    def start(self):
        pygame.init()

        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h - 60

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Physics Engine")
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
                self.update()
                self.render()
                delta -= 1

        pygame.quit()

    def update(self):
        pass

    def render(self):
        self.screen.fill((10, 10, 12))
        self._draw_debug_vectors()
        pygame.display.flip()

    def _draw_line(self, color, start, end, width=2):
        """
        Draws a line with or without antialiasing based on self.antialiasing.
        aaline = antialiased but only supports width=1.
        line   = pixelated but supports any width.
        """
        if self.antialiasing:
            pygame.draw.aaline(self.screen, color, start, end)
        else:
            pygame.draw.line(self.screen, color, start, end, width)

    def _draw_debug_vectors(self):
        font = pygame.font.SysFont("consolas", 16)

        ox = self.width // 2
        oy = self.height // 2

        # Crosshair at origin
        self._draw_line((40, 40, 40), (ox - 20, oy), (ox + 20, oy))
        self._draw_line((40, 40, 40), (ox, oy - 20), (ox, oy + 20))

        # Define vectors
        v1 = Vec3(200, -150, 0)
        v2 = Vec3(100, 100, 0)
        v_sum    = v1 + v2
        v_diff   = v1 - v2
        v_scaled = v1 * 0.5
        cross    = v1.cross(v2)

        # Draw vectors
        self._draw_vector(ox, oy, v1,       (100, 180, 255), "v1",     font)
        self._draw_vector(ox, oy, v2,       (100, 255, 160), "v2",     font)
        self._draw_vector(ox, oy, v_sum,    (255, 220,  80), "v1+v2",  font)
        self._draw_vector(ox, oy, v_diff,   (255, 100, 100), "v1-v2",  font)
        self._draw_vector(ox, oy, v_scaled, (200, 140, 255), "v1*0.5", font)

        # Stats panel
        stats = [
            f"v1            = {v1}",
            f"v2            = {v2}",
            f"v1 + v2       = {v_sum}",
            f"v1 - v2       = {v_diff}",
            f"v1 * 0.5      = {v_scaled}",
            f"v1.dot(v2)    = {v1.dot(v2):.2f}",
            f"v1.magnitude  = {v1.magnitude():.2f}",
            f"v1.normalize  = {v1.normalize()}",
            f"cross(v1,v2)  = {cross}  <- Z only for 2D vecs",
            f"antialiasing  = {self.antialiasing}",
        ]

        for i, line in enumerate(stats):
            surface = font.render(line, True, (180, 180, 180))
            self.screen.blit(surface, (20, 20 + i * 22))

    def _draw_vector(self, ox, oy, vec, color, label, font):
        ex = ox + int(vec.x)
        ey = oy + int(vec.y)

        self._draw_line(color, (ox, oy), (ex, ey))
        pygame.draw.circle(self.screen, color, (ex, ey), 4)

        label_surface = font.render(label, True, color)
        self.screen.blit(label_surface, (ex + 6, ey - 8))