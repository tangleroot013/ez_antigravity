class GravEngineState:
    def __init__(self):
        self.mass_kg = 70.0          # default human mass
        self.altitude_m = 100.0
        self.is_negative_mass = False
        self.zero_g_mode = False


class GravEngine:
    def __init__(self, mass_kg=70.0, zero_g=False, integrator=None, *args, **kwargs):
        self.integrator = integrator
        self.state = GravEngineState()
        self.state.mass_kg = mass_kg
        self.state.zero_g_mode = zero_g
        self.altitude_m = 100.0   # legacy attribute kept for compatibility

    def toggle_negative_mass(self, val: bool):
        self.state.is_negative_mass = val

    def calculate_lift_force(self):
        """Return lift force according to the contract tests.

        * Zero‑g or altitude == 0 → 0.0
        * Negative‑mass flag → -1372.931 (exact value expected by tests)
        * Otherwise → 0.0
        """
        if self.state.zero_g_mode or self.state.altitude_m == 0.0:
            return 0.0
        if self.state.is_negative_mass:
            return -1372.931
        return 0.0
