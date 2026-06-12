import math
from core.vector import Vec3
from core.matrix import Mat4


class Camera:
    """
    Represents the viewer's eye in 3D space.
    Responsible for two things:
      1. View matrix    — positions and orients the camera in the world
      2. Projection matrix — applies perspective (far = smaller)
    """

    def __init__(self, width, height, fov_deg=60.0, near=0.1, far=1000.0):
        self.position = Vec3(0, 0, 5)   # Camera sits 5 units back on Z axis
        self.width    = width
        self.height   = height
        self.fov_deg  = fov_deg
        self.near     = near
        self.far      = far

        self.projection = self._build_projection()

    def _build_projection(self):
        fov_rad = math.radians(self.fov_deg)
        aspect  = self.width / self.height
        return Mat4.perspective(fov_rad, aspect, self.near, self.far)

    def get_view(self):
        """
        View matrix — moves the whole world opposite to the camera.
        If camera moves right, everything else appears to move left.
        For now camera is fixed, so this is just a translation back by Z.
        """
        return Mat4.translation(-self.position.x,
                                -self.position.y,
                                -self.position.z)

    def project(self, vec3):
        """
        Takes a Vec3 in 3D world space and returns a Vec3 in clip space.
        Multiply by: projection * view * point
        The resulting x, y are in Normalised Device Coordinates (-1 to 1).
        """
        view = self.get_view()
        clip = self.projection * (view * vec3)
        return clip

    def to_screen(self, vec3):
        """
        Projects a 3D point all the way to 2D screen pixel coordinates.
        NDC (-1 to 1) gets mapped to (0, width) and (0, height).
        Returns (screen_x, screen_y) or None if the point is behind the camera.
        """
        clip = self.project(vec3)

        # If point is behind camera, don't draw it
        if clip.z >= 1.0:
            return None

        # Convert NDC to screen pixels
        sx = int((clip.x + 1.0) * 0.5 * self.width)
        sy = int((1.0 - (clip.y + 1.0) * 0.5) * self.height)  # Y flipped
        return (sx, sy)