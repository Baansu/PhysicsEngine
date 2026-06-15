import math
import pygame
from core.vector import Vec3
from physics.particle import Particle
from physics.world import World
from renderer.camera import Camera


# Colors for positive and negative charges
POS_COLOR = (255, 100, 100)   # red   — positive
NEG_COLOR = (100, 160, 255)   # blue  — negative
TRAIL_MAX = 80                # how many trail positions to keep


class EMView:
    """
    Physics sandbox — multiple charged particles interacting via Coulomb's law.
    Watch them attract, repel, and orbit each other in real time.
    """

    def __init__(self):
        self.engine  = None
        self.camera  = None
        self.world   = World()
        self.paused  = False
        self.trails  = {}   # particle id -> list of past positions

        # Add some particles with interesting initial conditions
        self._setup_scene()

    def _setup_scene(self):
        # Two opposite charges — should attract each other
        p1 = Particle(Vec3(-2,  0, 0), mass=1.0, charge=+1.0)
        p2 = Particle(Vec3( 2,  0, 0), mass=1.0, charge=-1.0)

        # Give them perpendicular velocities so they orbit instead of collide
        p1.velocity = Vec3(0,  1.5, 0)
        p2.velocity = Vec3(0, -1.5, 0)

        # A third repulsive charge in the middle
        p3 = Particle(Vec3(0, 2, 0), mass=2.0, charge=+1.0)
        p3.velocity = Vec3(1, 0, 0)

        self.world.add_particle(p1)
        self.world.add_particle(p2)
        self.world.add_particle(p3)

        # Initialise trails
        for p in self.world.particles:
            self.trails[id(p)] = []

    def handle_event(self, event):
        if self.camera:
            self.camera.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.paused = not self.paused
            if event.key == pygame.K_r:
                # Reset scene
                self.world = World()
                self.trails = {}
                self._setup_scene()

    def update(self, dt):
        if self.paused:
            return

        # Step physics — use smaller substeps for stability
        substeps = 10
        sub_dt   = dt / substeps
        for _ in range(substeps):
            self.world.step(sub_dt)

        # Record trail positions
        for p in self.world.particles:
            trail = self.trails[id(p)]
            trail.append(p.position.copy())
            if len(trail) > TRAIL_MAX:
                trail.pop(0)

    def render(self, screen):
        if self.camera is None:
            self.camera = Camera(self.engine.width, self.engine.height)

        font = pygame.font.SysFont("consolas", 16)

        # Draw trails
        for p in self.world.particles:
            trail  = self.trails[id(p)]
            color  = POS_COLOR if p.charge > 0 else NEG_COLOR
            for i in range(1, len(trail)):
                a = self.camera.to_screen(trail[i - 1])
                b = self.camera.to_screen(trail[i])
                if a and b:
                    # Fade trail — older = more transparent
                    alpha = int(255 * (i / len(trail)))
                    faded = (
                        int(color[0] * alpha / 255),
                        int(color[1] * alpha / 255),
                        int(color[2] * alpha / 255),
                    )
                    self.engine.draw_line(screen, faded, a, b)

        # Draw particles
        for p in self.world.particles:
            screen_pos = self.camera.to_screen(p.position)
            if screen_pos is None:
                continue

            color  = POS_COLOR if p.charge > 0 else NEG_COLOR
            radius = max(4, int(6 * abs(p.charge)))
            pygame.draw.circle(screen, color, screen_pos, radius)

            # Draw charge label
            label = f"+{p.charge:.0f}" if p.charge > 0 else f"{p.charge:.0f}"
            surf  = font.render(label, True, color)
            screen.blit(surf, (screen_pos[0] + 8, screen_pos[1] - 8))

        # Draw force vectors
        for p in self.world.particles:
            origin = self.camera.to_screen(p.position)
            if origin is None:
                continue
            force_tip = self.camera.to_screen(p.position + p.force * 0.0005)
            if force_tip:
                pygame.draw.line(screen, (255, 220, 80), origin, force_tip, 1)

        # Info panel
        state = "PAUSED" if self.paused else "RUNNING"
        lines = [
            "[ EM Particle Sandbox ]",
            f"space           =  pause / resume  [{state}]",
            f"r               =  reset scene",
            f"left drag       =  orbit camera",
            f"scroll          =  zoom",
            f"middle drag     =  pan",
            f"particles       =  {len(self.world.particles)}",
        ]

        for i, p in enumerate(self.world.particles):
            lines.append(
                f"  p{i+1}  charge={p.charge:+.1f}  "
                f"pos={p.position}  "
                f"|v|={p.velocity.magnitude():.2f}"
            )

        for i, line in enumerate(lines):
            color = (100, 180, 255) if i == 0 else (180, 180, 180)
            surf  = font.render(line, True, color)
            screen.blit(surf, (20, 20 + i * 22))