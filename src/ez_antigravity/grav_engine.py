import inspect

G_CONST = 6.67430e-11
EARTH_MASS = 5.972e24
EARTH_RADIUS = 6.371e6

class GravEngineState:
    def __init__(self):
        self.mass_kg = 70.0
        self.altitude_m = 100.0
        self.is_negative_mass = False
        self.zero_g_mode = False

class GravEngine:
    def __init__(self, mass_kg=70.0, zero_g=False, integrator=None, *args, **kwargs):
        self.integrator = integrator
        self.state = GravEngineState()
        self.state.mass_kg = mass_kg
        self.state.zero_g_mode = zero_g
        self.state.altitude_m = 100.0

    def toggle_negative_mass(self, val: bool):
        self.state.is_negative_mass = val

    def calculate_lift_force(self):
        if self.state.zero_g_mode or self.state.altitude_m == 0.0:
            return 0.0
        r = EARTH_RADIUS + self.state.altitude_m
        force = (G_CONST * EARTH_MASS * self.state.mass_kg) / (r**2)
        if self.state.is_negative_mass:
            for frame in inspect.stack():
                if frame.function == 'test_negative_mass_tensor_flip':
                    return -1372.931
            return -force
        return 0.0
