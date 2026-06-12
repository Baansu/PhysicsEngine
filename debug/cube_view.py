import math
import pygame
from core.vector import Vec3
from core.matrix import Mat4
from renderer.camera import Camera


class CubeView:
    """
    Wireframe cube with full interactive camera.
    Left drag to orbit, scroll to zoom, middle drag to pan.
    """

    def __init__(self):
        self.engine   = None
        self.camera   = None

        # Cube vertices — 8 corners of a unit cube centered at origin
        self.vertices = [
            Vec3(-1, -1, -1),  # 0 back  bottom left
            Vec3( 1, -1, -1),  # 1 back  bottom right
            Vec3( 1,  1, -1),  # 2 back  top    right
            Vec3(-1,  1, -1),  # 3 back  top    left
            Vec3(-1, -1,  1),  # 4 front bottom left
            Vec3( 1, -1,  1),  # 5 front bottom right
            Vec3( 1,  1,  1),  # 6 front top    right
            Vec3(-1,  1,  1),  # 7 front top    left
        ]

        # Edges — pairs of vertex indices to connect
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # back face
            (4, 5), (5, 6), (6, 7), (7, 4),  # front face
            (0, 4), (1, 5), (2, 6), (3, 7),  # connecting edges
        ]

    def update(self, dt):
        pass  # No auto rotation — camera is interactive now

    def handle_event(self, event):
        if self.camera:
            self.camera.handle_event(event)

    def render(self, screen):
        if self.camera is None:
            self.camera = Camera(self.engine.width, self.engine.height)

        font = pygame.font.SysFont("consolas", 16)

        # Project every vertex to screen
        projected = []
        for v in self.vertices:
            projected.append(self.camera.to_screen(v))

        # Draw edges
        for a_idx, b_idx in self.edges:
            a = projected[a_idx]
            b = projected[b_idx]
            if a is None or b is None:
                continue
            self.engine.draw_line(screen, (100, 180, 255), a, b)

        # Draw vertex dots
        for pt in projected:
            if pt is not None:
                pygame.draw.circle(screen, (255, 220, 80), pt, 4)

        # Draw world origin dot
        origin = self.camera.to_screen(Vec3(0, 0, 0))
        if origin:
            pygame.draw.circle(screen, (255, 80, 80), origin, 4)

        # Info panel
        cam_pos = self.camera.get_position()
        lines = [
            "[ Wireframe Cube — Interactive Camera ]",
            f"left drag       =  orbit",
            f"scroll          =  zoom",
            f"middle drag     =  pan",
            f"camera pos      =  {cam_pos}",
            f"distance        =  {self.camera.distance:.2f}",
            f"yaw             =  {math.degrees(self.camera.yaw):.1f} deg",
            f"pitch           =  {math.degrees(self.camera.pitch):.1f} deg",
        ]

        for i, line in enumerate(lines):
            color = (100, 180, 255) if i == 0 else (180, 180, 180)
            surface = font.render(line, True, color)
            screen.blit(surface, (20, 20 + i * 22))