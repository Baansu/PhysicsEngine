import math
from core.vector import Vec3


class Mat4:
    """
    A 4x4 matrix for 3D transformations.
    Stored as a flat list of 16 floats, row by row:
    [m00, m01, m02, m03,
     m10, m11, m12, m13,
     m20, m21, m22, m23,
     m30, m31, m32, m33]
    """

    def __init__(self, values=None):
        if values is None:
            # Default: identity matrix (does nothing to a vector)
            self.m = [
                1, 0, 0, 0,
                0, 1, 0, 0,
                0, 0, 1, 0,
                0, 0, 0, 1
            ]
        else:
            self.m = list(values)

    # -------------------------
    # Factory Methods
    # These create specific useful matrices
    # -------------------------

    @staticmethod
    def identity():
        """Identity matrix — multiplying by this changes nothing. Like multiplying by 1."""
        return Mat4()

    @staticmethod
    def translation(tx, ty, tz):
        """
        Moves a point by (tx, ty, tz).
        This is why we need 4x4 — translation can't be done with 3x3.
        """
        return Mat4([
            1, 0, 0, tx,
            0, 1, 0, ty,
            0, 0, 1, tz,
            0, 0, 0,  1
        ])

    @staticmethod
    def scale(sx, sy, sz):
        """Stretches or shrinks along each axis."""
        return Mat4([
            sx,  0,  0, 0,
             0, sy,  0, 0,
             0,  0, sz, 0,
             0,  0,  0, 1
        ])

    @staticmethod
    def rotation_x(angle_rad):
        """Rotate around the X axis by angle_rad radians."""
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Mat4([
            1,  0,  0, 0,
            0,  c, -s, 0,
            0,  s,  c, 0,
            0,  0,  0, 1
        ])

    @staticmethod
    def rotation_y(angle_rad):
        """Rotate around the Y axis by angle_rad radians."""
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Mat4([
             c, 0, s, 0,
             0, 1, 0, 0,
            -s, 0, c, 0,
             0, 0, 0, 1
        ])

    @staticmethod
    def rotation_z(angle_rad):
        """Rotate around the Z axis by angle_rad radians."""
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Mat4([
            c, -s, 0, 0,
            s,  c, 0, 0,
            0,  0, 1, 0,
            0,  0, 0, 1
        ])

    @staticmethod
    def perspective(fov_rad, aspect, near, far):
        """
        Perspective projection matrix.
        This is what makes far things look smaller than near things.
        fov_rad = field of view in radians (how wide the camera sees)
        aspect  = width / height of the screen
        near    = closest distance camera can see
        far     = furthest distance camera can see
        """
        f = 1.0 / math.tan(fov_rad / 2.0)
        return Mat4([
            f / aspect,  0,                              0,  0,
                     0,  f,                              0,  0,
                     0,  0,   (far + near) / (near - far), (2 * far * near) / (near - far),
                     0,  0,                             -1,  0
        ])

    # -------------------------
    # Matrix Multiplication
    # -------------------------

    def __mul__(self, other):
        """
        Multiply two Mat4s together — combines their transforms.
        Order matters: A * B != B * A
        Think of it as: apply B first, then A.
        """
        if isinstance(other, Mat4):
            result = [0.0] * 16
            for row in range(4):
                for col in range(4):
                    for k in range(4):
                        result[row * 4 + col] += self.m[row * 4 + k] * other.m[k * 4 + col]
            return Mat4(result)

        elif isinstance(other, Vec3):
            """
            Multiply Mat4 by Vec3.
            We secretly give Vec3 a 4th component w=1 to make translation work.
            After multiplication we drop w and return a Vec3.
            """
            x, y, z, w = other.x, other.y, other.z, 1.0
            m = self.m
            rx = m[0]*x  + m[1]*y  + m[2]*z  + m[3]*w
            ry = m[4]*x  + m[5]*y  + m[6]*z  + m[7]*w
            rz = m[8]*x  + m[9]*y  + m[10]*z + m[11]*w
            rw = m[12]*x + m[13]*y + m[14]*z + m[15]*w

            # Perspective divide — only matters for projection, safe to always do
            if rw != 0 and rw != 1:
                return Vec3(rx / rw, ry / rw, rz / rw)
            return Vec3(rx, ry, rz)

    def __repr__(self):
        m = self.m
        return (
            f"Mat4(\n"
            f"  {m[0]:7.2f} {m[1]:7.2f} {m[2]:7.2f} {m[3]:7.2f}\n"
            f"  {m[4]:7.2f} {m[5]:7.2f} {m[6]:7.2f} {m[7]:7.2f}\n"
            f"  {m[8]:7.2f} {m[9]:7.2f} {m[10]:7.2f} {m[11]:7.2f}\n"
            f"  {m[12]:7.2f} {m[13]:7.2f} {m[14]:7.2f} {m[15]:7.2f}\n"
            f")"
        )