from physics.particle import Particle
from physics.em.coulomb import coulomb_force


class World:
    """
    The physics world — owns all particles and steps the simulation.
    Every frame:
      1. Reset all forces
      2. Compute forces between every pair of particles
      3. Integrate — move particles forward by dt
    """

    def __init__(self):
        self.particles = []

    def add_particle(self, particle: Particle):
        self.particles.append(particle)

    def step(self, dt: float):
        # 1. Reset forces
        for p in self.particles:
            p.reset_force()

        # 2. Compute pairwise Coulomb forces
        # N-body: every particle affects every other particle
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                a = self.particles[i]
                b = self.particles[j]

                # Force on A due to B
                f = coulomb_force(a, b)

                # Newton's 3rd law — equal and opposite
                a.apply_force(f)
                b.apply_force(-f)

        # 3. Integrate
        for p in self.particles:
            p.integrate_euler(dt)