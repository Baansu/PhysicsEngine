import pygame
from core.vector import Vec3


class VectorView:
    """
    Debug visualiser for Vec3 operations.
    Pass this into Engine as the scene to see it.
    """

    def __init__(self):
        self.engine = None  # Set by Engine.start()

    def update(self, dt):
        pass  # Nothing to update, this is a static view

    def render(self, screen):
        font = pygame.font.SysFont("consolas", 16)

        ox = self.engine.width // 2
        oy = self.engine.height // 2

        # Crosshair at origin
        self.engine.draw_line(screen, (40, 40, 40), (ox - 20, oy), (ox + 20, oy))
        self.engine.draw_line(screen, (40, 40, 40), (ox, oy - 20), (ox, oy + 20))

        # Define vectors
        v1      = Vec3(200, -150, 0)
        v2      = Vec3(100,  100, 0)
        v_sum   = v1 + v2
        v_diff  = v1 - v2
        v_scaled = v1 * 0.5
        cross   = v1.cross(v2)

        # Draw vectors
        self._draw_vector(screen, ox, oy, v1,       (100, 180, 255), "v1",     font)
        self._draw_vector(screen, ox, oy, v2,       (100, 255, 160), "v2",     font)
        self._draw_vector(screen, ox, oy, v_sum,    (255, 220,  80), "v1+v2",  font)
        self._draw_vector(screen, ox, oy, v_diff,   (255, 100, 100), "v1-v2",  font)
        self._draw_vector(screen, ox, oy, v_scaled, (200, 140, 255), "v1*0.5", font)

        # Stats panel
        stats = [
            "[ Vec3 Debug View ]",
            f"v1            = {v1}",
            f"v2            = {v2}",
            f"v1 + v2       = {v_sum}",
            f"v1 - v2       = {v_diff}",
            f"v1 * 0.5      = {v_scaled}",
            f"v1.dot(v2)    = {v1.dot(v2):.2f}",
            f"v1.magnitude  = {v1.magnitude():.2f}",
            f"v1.normalize  = {v1.normalize()}",
            f"cross(v1,v2)  = {cross}  <- Z only for 2D vecs",
        ]

        for i, line in enumerate(stats):
            color = (100, 180, 255) if i == 0 else (180, 180, 180)
            surface = font.render(line, True, color)
            screen.blit(surface, (20, 20 + i * 22))

    def _draw_vector(self, screen, ox, oy, vec, color, label, font):
        ex = ox + int(vec.x)
        ey = oy + int(vec.y)

        self.engine.draw_line(screen, color, (ox, oy), (ex, ey))
        pygame.draw.circle(screen, color, (ex, ey), 4)

        label_surface = font.render(label, True, color)
        screen.blit(label_surface, (ex + 6, ey - 8))