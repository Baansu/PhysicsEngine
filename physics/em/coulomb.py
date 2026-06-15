from core.vector import Vec3
from physics.particle import Particle

# Coulomb's constant in N⋅m²/C²
# In a real sim this would be 8.99e9 but we scale it down
# so the forces are visible at our scene scale
K = 8.99e3


def coulomb_force(a: Particle, b: Particle) -> Vec3:
    """
    Computes the electrostatic force on particle A due to particle B.
    F = k * q1 * q2 / r² * r̂

    Returns a Vec3 force vector in the direction from B -> A.
    - Same sign charges    -> repulsive  (force points away from B)
    - Opposite sign charges -> attractive (force points toward B)
    """
    # Vector from B to A
    r_vec = a.position - b.position
    r_sq  = r_vec.magnitude_squared()

    # Avoid division by zero if particles overlap
    if r_sq < 0.0001:
        return Vec3(0, 0, 0)

    r_mag = r_sq ** 0.5

    # Unit vector from B to A
    r_hat = r_vec * (1.0 / r_mag)

    # Scalar magnitude of force
    force_mag = K * a.charge * b.charge / r_sq

    # Full force vector — positive = repulsive (pushes A away from B)
    return r_hat * force_mag