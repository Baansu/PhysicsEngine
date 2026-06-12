import math
import pygame
from core.vector import Vec3
from core.matrix import Mat4
from renderer.camera import Camera


class CubeView:
    """
    First real 3D scene — a wireframe cube spinning in space.
    Every vertex goes through: model transform -> view -> projection -> screen.
    That's the full 3D render pipeline.
    """

    def __init__(self):
        self.engine  = None
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.camera  = None

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

        # Edges — pairs of vertex indices to connect with lines
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # back face
            (4, 5), (5, 6), (6, 7), (7, 4),  # front face
            (0, 4), (1, 5), (2, 6), (3, 7),  # connecting edges
        ]

    def update(self, dt):
        self.angle_x += dt * math.pi / 4.0   # rotate around X
        self.angle_y += dt * math.pi / 3.0   # rotate around Y slightly faster

    def render(self, screen):
        if self.camera is None:
            self.camera = Camera(self.engine.width, self.engine.height)

        font = pygame.font.SysFont("consolas", 16)

        # Build model matrix — rotate the cube
        rot_x     = Mat4.rotation_x(self.angle_x)
        rot_y     = Mat4.rotation_y(self.angle_y)
        model     = rot_y * rot_x   # apply X rotation first, then Y

        # Project every vertex to screen space
        projected = []
        for v in self.vertices:
            world_pos  = model * v            # apply rotation
            screen_pos = self.camera.to_screen(world_pos)
            projected.append(screen_pos)

        # Draw edges
        for a_idx, b_idx in self.edges:
            a = projected[a_idx]
            b = projected[b_idx]

            # Skip edge if either vertex is behind the camera
            if a is None or b is None:
                continue

            self.engine.draw_line(screen, (100, 180, 255), a, b)

        # Draw vertex dots
        for pt in projected:
            if pt is not None:
                pygame.draw.circle(screen, (255, 220, 80), pt, 4)

        # Info panel
        angle_x_deg = math.degrees(self.angle_x) % 360
        angle_y_deg = math.degrees(self.angle_y) % 360
        lines = [
            "[ Wireframe Cube ]",
            f"pipeline    =  model -> view -> projection -> screen",
            f"rotation X  =  {angle_x_deg:.1f} deg",
            f"rotation Y  =  {angle_y_deg:.1f} deg",
            f"vertices    =  {len(self.vertices)}",
            f"edges       =  {len(self.edges)}",
        ]

        for i, line in enumerate(lines):
            color = (100, 180, 255) if i == 0 else (180, 180, 180)
            surface = font.render(line, True, color)
            screen.blit(surface, (20, 20 + i * 22))