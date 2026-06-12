import math


class Vec3:
    """
    A 3D vector with x, y, z components.
    The building block of everything in this engine.
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    # -------------------------
    # Basic Arithmetic
    # -------------------------

    def __add__(self, other):
        """v1 + v2"""
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """v1 - v2"""
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        """v * scalar — scale the vector"""
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar):
        """scalar * v — same thing, both orders work"""
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        """v / scalar"""
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __neg__(self):
        """-v — flip direction"""
        return Vec3(-self.x, -self.y, -self.z)

    # -------------------------
    # Vector Operations
    # -------------------------

    def dot(self, other):
        """
        Dot product: v1 . v2
        Returns a scalar. Tells you how aligned two vectors are.
        0 = perpendicular, positive = same direction, negative = opposite.
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        """
        Cross product: v1 x v2
        Returns a NEW vector perpendicular to both.
        Critical for 3D normals, rotations, and the Lorentz force (q * v x B).
        """
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def magnitude(self):
        """Length of the vector — Pythagoras in 3D."""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def magnitude_squared(self):
        """
        Length squared — no square root, so much faster.
        Use this when you only need to compare lengths, not the actual value.
        """
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def normalize(self):
        """
        Returns a unit vector (length = 1) pointing in the same direction.
        Used constantly — for directions, normals, and EM field directions.
        """
        mag = self.magnitude()
        if mag == 0:
            return Vec3(0, 0, 0)
        return self / mag

    def distance_to(self, other):
        """Straight line distance between two points in 3D space."""
        return (self - other).magnitude()

    # -------------------------
    # Utilities
    # -------------------------

    def copy(self):
        """Returns a new Vec3 with the same values."""
        return Vec3(self.x, self.y, self.z)

    def __repr__(self):
        """How it prints — Vec3(1.00, 2.00, 3.00)"""
        return f"Vec3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z