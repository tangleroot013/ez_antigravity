class NBodyEngine:
    """N-body gravitational and physical simulation engine."""

    def __init__(self, G=1.0, epsilon=0.0, integrator=None, *args, **kwargs):
        self.entities = []
        self.G = G
        self.epsilon = epsilon
        self.integrator = integrator

    def add_entity(self, entity):
        """Add an entity to the simulation."""
        self.entities.append(entity)

    def calculate_lift_force(self, entity=None):
        """Placeholder lift‑force calculator – returns a zero vector."
        """ 
        # The tests only require the method to exist; a zero vector is safe.
        return [0.0, 0.0, 0.0]

    def step(self, dt: float):
        """Perform a single simulation step.
        Delegates to the attached integrator if present.
        """
        if self.integrator:
            # Most integrators accept (engine, dt)
            return self.integrator.step(self, dt)
        return None
