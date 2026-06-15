from core.vector import Vec3


class Particle:
    """
    A point in space with mass, charge, position and velocity.
    The fundamental object of the physics simulation.
    """

    def __init__(self, position: Vec3, mass: float, charge: float):
        self.position     = position
        self.mass         = mass
        self.charge       = charge

        self.velocity     = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)
        self.force        = Vec3(0, 0, 0)   # accumulated force this frame

    def reset_force(self):
        """Clear accumulated force at the start of each physics step."""
        self.force = Vec3(0, 0, 0)

    def apply_force(self, f: Vec3):
        """Add a force vector to this particle."""
        self.force = self.force + f

    def integrate_euler(self, dt: float):
        """
        Euler integration — simplest possible integrator.
        F = ma  ->  a = F/m
        v += a * dt
        x += v * dt
        """
        self.acceleration = self.force * (1.0 / self.mass)
        self.velocity     = self.velocity + self.acceleration * dt
        self.position     = self.position + self.velocity * dt

    def __repr__(self):
        return (f"Particle(pos={self.position}, "
                f"vel={self.velocity}, "
                f"charge={self.charge:.2f}, "
                f"mass={self.mass:.2f})")