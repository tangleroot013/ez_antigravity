import math


# Physical constants
G_CONST = 6.67430e-11
EARTH_MASS = 5.972e24
EARTH_RADIUS = 6_371_000.0
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
        self.mass_kg = float(mass_kg)
        self.altitude_m = float(altitude_m)
        self.coil_temp_c = float(coil_temp_c)
        self.ambient_temp_c = float(ambient_temp_c)
        self.cooling_rate = float(cooling_rate)
        self.zero_g_mode = bool(zero_g_mode)
        self.is_negative_mass = bool(is_negative_mass)

    def tick(self, dt=1.0):
        """Advance thermal state and return event log messages."""
        if self.altitude_m < 0:
            raise ValueError("Altitude cannot be negative")

        if dt < 0:
            raise ValueError("dt cannot be negative")

        logs = []

        # Check the incoming temperature before applying cooling.
        if self.coil_temp_c >= 99.5:
            self.coil_temp_c = 99.0
            self.altitude_m = 0.0
            self.zero_g_mode = False
            logs.append("EMERGENCY AUTO-CUTOFF: Temperature critical")
            return logs

        self.coil_temp_c -= (
            (self.coil_temp_c - self.ambient_temp_c)
            * self.cooling_rate
            * dt
        )

        return logs


class GravEngine:
    def __init__(self, mass_kg=70.0, zero_g=False):
        self.state = PhysicsState(
            mass_kg=mass_kg,
            zero_g_mode=zero_g,
        )

    def toggle_negative_mass(self, flag):
        self.state.is_negative_mass = bool(flag)

    def calculate_lift_force(self) -> float:
        """Calculates net lift force using local gravity based on altitude."""
        if self.state.zero_g_mode:
            return 0.0
        if self.state.altitude_m <= 0:
            return 0.0
        
        # Unified gravity: g_local = (G * M_earth) / r^2
        r = EARTH_RADIUS + self.state.altitude_m
        g_local = (G_CONST * EARTH_MASS) / (r ** 2)
        force = self.state.mass_kg * g_local
        
        if self.state.is_negative_mass:
            force = -force
        
        return round(force, 4)
    def get_lift_force(self):
        return self.calculate_lift_force()

    def calculate_orbital_velocity(self, altitude_km):
        if altitude_km < 0:
            raise ValueError("Altitude cannot be negative")

        radius_m = EARTH_RADIUS + (float(altitude_km) * 1000.0)

        if radius_m <= 0:
            raise ValueError("Orbital radius must be positive")

        velocity = math.sqrt((G_CONST * EARTH_MASS) / radius_m)
        return round(velocity, 2)

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
