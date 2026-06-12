import math
from core.vector import Vec3
from core.matrix import Mat4


class Camera:
    """
    Orbital camera — orbits around a target point in 3D space.
    Controls:
      Left mouse drag   -> orbit (yaw + pitch)
      Scroll wheel      -> zoom
      Middle mouse drag -> pan target point
    """

    def __init__(self, width, height, fov_deg=60.0, near=0.1, far=1000.0):
        self.width    = width
        self.height   = height
        self.fov_deg  = fov_deg
        self.near     = near
        self.far      = far

        # Orbital parameters
        self.target   = Vec3(0, 0, 0)
        self.distance = 5.0
        self.yaw      = 0.0
        self.pitch    = 0.3

        # Mouse state
        self._last_mouse  = None
        self._left_down   = False
        self._middle_down = False

        # Sensitivity
        self.orbit_speed = 0.005
        self.pan_speed   = 0.001
        self.zoom_speed  = 0.3

        self.projection = self._build_projection()

    def _build_projection(self):
        fov_rad = math.radians(self.fov_deg)
        aspect  = self.width / self.height
        return Mat4.perspective(fov_rad, aspect, self.near, self.far)

    def get_position(self):
        """Compute camera position from spherical coordinates."""
        x = self.target.x + self.distance * math.sin(self.yaw) * math.cos(self.pitch)
        y = self.target.y + self.distance * math.sin(self.pitch)
        z = self.target.z + self.distance * math.cos(self.yaw) * math.cos(self.pitch)
        return Vec3(x, y, z)

    def get_view(self):
        """Build view matrix using look-at math."""
        pos    = self.get_position()
        target = self.target

        forward  = (target - pos).normalize()
        world_up = Vec3(0, 1, 0)
        right    = forward.cross(world_up).normalize()
        up       = right.cross(forward).normalize()

        m = Mat4([
             right.x,    right.y,    right.z,   -right.dot(pos),
             up.x,       up.y,       up.z,      -up.dot(pos),
            -forward.x, -forward.y, -forward.z,  forward.dot(pos),
             0,          0,          0,           1
        ])
        return m

    def to_screen(self, vec3):
        """Projects a 3D world point to 2D screen coordinates."""
        view = self.get_view()
        clip = self.projection * (view * vec3)

        if clip.z >= 1.0:
            return None

        sx = int((clip.x + 1.0) * 0.5 * self.width)
        sy = int((1.0 - (clip.y + 1.0) * 0.5) * self.height)
        return (sx, sy)

    def handle_event(self, event):
        import pygame

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._left_down  = True
                self._last_mouse = event.pos
            if event.button == 2:
                self._middle_down = True
                self._last_mouse  = event.pos
            if event.button == 4:   # scroll up — zoom in
                self.distance = max(1.0, self.distance - self.zoom_speed)
            if event.button == 5:   # scroll down — zoom out
                self.distance += self.zoom_speed

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self._left_down = False
            if event.button == 2:
                self._middle_down = False

        if event.type == pygame.MOUSEMOTION:
            if self._last_mouse is None:
                self._last_mouse = event.pos
                return

            dx = event.pos[0] - self._last_mouse[0]
            dy = event.pos[1] - self._last_mouse[1]
            self._last_mouse = event.pos

            if self._left_down:
                # Flipped to match Blender convention
                self.yaw   -= dx * self.orbit_speed
                self.pitch += dy * self.orbit_speed
                self.pitch  = max(-math.pi / 2 + 0.05,
                                   min(math.pi / 2 - 0.05, self.pitch))

            if self._middle_down:
                pos      = self.get_position()
                forward  = (self.target - pos).normalize()
                world_up = Vec3(0, 1, 0)
                right    = forward.cross(world_up).normalize()
                up       = right.cross(forward).normalize()

                pan_amount  = self.distance * self.pan_speed
                self.target = self.target - right * (dx * pan_amount)
                self.target = self.target + up    * (dy * pan_amount)