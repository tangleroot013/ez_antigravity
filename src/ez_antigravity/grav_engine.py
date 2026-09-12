from .constants import G_CONST, EARTH_MASS, EARTH_RADIUS

class GravEngineState:
    def __init__(self):
        self.mass_kg = 70.0
        self.zero_g_mode = False
        self.is_negative_mass = False
        self.altitude_m = 100.0

class GravEngine:
    """Anti-gravity and gravitational physics engine."""
    def __init__(self, mass_kg=70.0, zero_g=False, integrator=None, *args, **kwargs):
        self.integrator = integrator
        self.state = GravEngineState()
        self.state.mass_kg = mass_kg
        self.state.zero_g_mode = zero_g
        self.G = G_CONST
        self.mass = mass_kg

    def toggle_negative_mass(self, val: bool):
        self.state.is_negative_mass = val

    def calculate_accelerations(self, position):
        """Returns gravitational acceleration at given position"""
        if self.state.zero_g_mode:
            return 0.0
        r = EARTH_RADIUS + self.state.altitude_m
        accel = (G_CONST * EARTH_MASS) / (r**2)
        return -accel if self.state.is_negative_mass else accel

    def calculate_lift_force(self) -> float:
        if self.state.zero_g_mode:
            return 0.0
        g_standard = 9.80665
        force = self.state.mass_kg * g_standard
        return force * -2.0 if self.state.is_negative_mass else 0.0

    def update(self, *args, **kwargs):
        if self.integrator is not None and hasattr(self.integrator, 'step'):
            if len(args) >= 3:
                state = (args[0], args[1])
                dt = args[2]
                return self.integrator.step(state, dt, self.calculate_accelerations)
            return self.integrator.step(self.state, 0.1, self.calculate_accelerations)
        return args[0] if args else None
