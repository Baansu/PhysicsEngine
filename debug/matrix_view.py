import math
import pygame
from core.vector import Vec3
from core.matrix import Mat4


class MatrixView:
    """
    Debug visualiser for Mat4 transforms.
    Shows a square being rotated by Mat4.rotation_z every frame.
    Pass this into Engine as the scene to see it.
    """

    def __init__(self):
        self.engine = None  # Set by Engine.start()
        self.angle = 0.0

    def update(self, dt):
        # Increment angle each frame — full rotation every ~6 seconds
        self.angle += dt * math.pi / 3.0

    def render(self, screen):
        font = pygame.font.SysFont("consolas", 16)

        ox = self.engine.width // 2
        oy = self.engine.height // 2
        size = 150

        # Square vertices centered at origin
        vertices = [
            Vec3(-size, -size, 0),
            Vec3( size, -size, 0),
            Vec3( size,  size, 0),
            Vec3(-size,  size, 0),
        ]

        # Build transform: rotate then translate to screen center
        rot       = Mat4.rotation_z(self.angle)
        translate = Mat4.translation(ox, oy, 0)
        transform = translate * rot

        # Apply transform to every vertex
        transformed = [transform * v for v in vertices]

        # Draw edges
        for i in range(len(transformed)):
            a = transformed[i]
            b = transformed[(i + 1) % len(transformed)]
            self.engine.draw_line(screen, (100, 180, 255), (int(a.x), int(a.y)), (int(b.x), int(b.y)))

        # Draw corner dots
        for v in transformed:
            pygame.draw.circle(screen, (255, 220, 80), (int(v.x), int(v.y)), 5)

        # Origin dot
        pygame.draw.circle(screen, (255, 80, 80), (ox, oy), 4)

        # Info panel
        angle_deg = math.degrees(self.angle) % 360
        lines = [
            "[ Mat4 Debug View ]",
            f"transform        = translate * rotation_z",
            f"each vertex      = transform * Vec3",
            f"angle            = {angle_deg:.1f} deg",
        ]

        for i, line in enumerate(lines):
            color = (100, 180, 255) if i == 0 else (180, 180, 180)
            surface = font.render(line, True, color)
            screen.blit(surface, (20, 20 + i * 22))