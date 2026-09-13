import math

# Physical constants
G_CONST = 6.67430e-11
EARTH_MASS = 5.972e24
EARTH_RADIUS = 6371000.0
# Retained for reference / backward-compat; no longer used in lift force
STANDARD_G = 9.80665


class PhysicsState:
    def __init__(
        self,
        mass_kg=70.0,
        altitude_m=0.0,
        coil_temp_c=20.0,
        ambient_temp_c=20.0,
        cooling_rate=0.1,
        zero_g_mode=False,
        is_negative_mass=False,
    ):
        self.mass_kg = mass_kg
        self.altitude_m = altitude_m
        self.coil_temp_c = coil_temp_c
        self.ambient_temp_c = ambient_temp_c
        self.cooling_rate = cooling_rate
        self.zero_g_mode = zero_g_mode
        self.is_negative_mass = is_negative_mass

    def tick(self, dt=1.0):
        """Advance thermal state by dt seconds. Returns a list of log messages."""  # noqa: E501
        logs = []

        if self.altitude_m < 0:
            raise ValueError("Altitude cannot be negative")

        if self.coil_temp_c >= 99.5:
            # Overheat condition caught before cooling is applied this tick.
            self.coil_temp_c = 99.0
            self.altitude_m = 0.0
            self.zero_g_mode = False
            logs.append("EMERGENCY AUTO-CUTOFF: Temperature critical")
        else:
            self.coil_temp_c -= (
                (self.coil_temp_c - self.ambient_temp_c) * self.cooling_rate * dt  # noqa: E501
            )

        return logs


class GravEngine:
    def __init__(self, mass_kg=70.0, zero_g=False):
        self.state = PhysicsState(mass_kg=mass_kg, zero_g_mode=zero_g)

    def toggle_negative_mass(self, flag):
        self.state.is_negative_mass = bool(flag)

    def local_gravity(self):
        """Inverse-square gravitational acceleration at the current altitude (m/s^2)."""  # noqa: E501
        r = EARTH_RADIUS + self.state.altitude_m
        return (G_CONST * EARTH_MASS) / (r**2)

    def calculate_lift_force(self):
        if self.state.zero_g_mode:
            return 0.0
        if self.state.altitude_m <= 0:
            return 0.0

        g_local = self.local_gravity()
        force = self.state.mass_kg * g_local

        if self.state.is_negative_mass:
            force = -force

        return round(float(force), 4)

    def get_lift_force(self):
        return self.calculate_lift_force()

    def calculate_orbital_velocity(self, altitude_km):
        mu = G_CONST * EARTH_MASS
        radius = EARTH_RADIUS + (altitude_km * 1000.0)
        velocity = math.sqrt(mu / radius)
        return round(float(velocity), 2)

    def get_telemetry(self):
        return "\n".join(
            (
                f"Mass: {self.state.mass_kg:g}",
                f"Altitude: {self.state.altitude_m:g}",
                f"Coil Temp: {self.state.coil_temp_c:g}",
                f"Zero-G: {self.state.zero_g_mode}",
                f"Negative Mass: {self.state.is_negative_mass}",
            )
        )
