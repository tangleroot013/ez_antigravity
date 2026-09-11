#!/usr/bin/env python3

"""
ez_grav Engine Module (src/ez_grav.py)

Core physics engine and state management with boundary protection.
"""

import math
import time
import asyncio
from dataclasses import dataclass, field

G_CONST = 6.67430e-11  # m^3 kg^-1 s^-2
EARTH_MASS = 5.97219e24  # kg
EARTH_RADIUS = 6371000  # m
STANDARD_G = 9.80665  # m/s^2

@dataclass
class PhysicsState:
    """Mutable simulation state for ez_grav."""
    mass_kg: float = 70.0
    is_negative_mass: bool = False
    zero_g_mode: bool = False
    altitude_m: float = 0.0
    metric_mode: str = "flat"  # "flat" or "curved"
    coil_temp_c: float = 24.5
    ambient_temp_c: float = 20.0
    cooling_rate: float = 0.2  # °C s⁻¹ toward ambient
    altitude_decay_rate: float = 2.0  # m s⁻¹ passive decay
    verbose: bool = False
    running: bool = True
    log_buffer: list = field(default_factory=list)

    def log(self, msg: str) -> None:
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {msg}"
        self.log_buffer.append(formatted)

    def tick(self, dt: float) -> list[str]:
        logs: list[str] = []

        # Atmospheric friction heating (0 < altitude < 100,000 m)
        if 0.0 < self.altitude_m < 100_000.0:
            friction_heat = (100_000.0 - self.altitude_m) * 1e-5
            self.coil_temp_c += friction_heat * dt
            logs.append(f"Atmospheric heating: +{friction_heat * dt:.6f}°C")

        # Over-heat safety cutoff
        OVERHEAT_CUTOFF = 99.0
        overheated = False
        if self.zero_g_mode and self.coil_temp_c > OVERHEAT_CUTOFF:
            self.coil_temp_c = OVERHEAT_CUTOFF
            self.zero_g_mode = False
            self.altitude_m = 0.0
            overheated = True
            logs.append(f"EMERGENCY AUTO-CUTOFF: Over-heat cutoff engaged: set to {OVERHEAT_CUTOFF}°C")

        # Newton's law of cooling toward ambient
        if not overheated and self.coil_temp_c > self.ambient_temp_c:
            delta = (self.ambient_temp_c - self.coil_temp_c) * self.cooling_rate * dt
            self.coil_temp_c += delta

        # Passive altitude decay when zero-g is disengaged
        if not self.zero_g_mode and self.altitude_m > 0.0:
            self.altitude_m = max(0.0, self.altitude_m - self.altitude_decay_rate * dt)

        return list(self.log_buffer) + logs

class GravEngine:
    """Core physics calculations and telemetry manager."""

    def __init__(self, mass_kg: float = 70.0, zero_g: bool = False, verbose: bool = False, **kwargs):
        self.state = PhysicsState(mass_kg=mass_kg, zero_g_mode=zero_g, verbose=verbose, **kwargs)
        self.log_buffer = []

    def log(self, msg: str):
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {msg}"
        self.log_buffer.append(formatted)
        self.state.log_buffer.append(formatted)

    def enable_zero_g(self, enabled: bool = True):
        self.state.zero_g_mode = enabled
        status = "ENABLED" if enabled else "DISABLED"
        self.log(f"Zero-Gravity simulation field set to: {status}")

    def set_mass(self, mass_kg: float):
        if mass_kg < 0:
            raise ValueError("Mass must be positive. Use toggle_negative_mass() for exotic mass tensors.")
        self.state.mass_kg = mass_kg
        self.log(f"Payload mass set to {mass_kg} kg")

    def toggle_negative_mass(self, enabled: bool = None):
        if enabled is None:
            self.state.is_negative_mass = not self.state.is_negative_mass
        else:
            self.state.is_negative_mass = enabled
        sign = "-" if self.state.is_negative_mass else "+"
        self.log(f"Shifted mass tensor state to {sign}{abs(self.state.mass_kg)} kg")

    def calculate_lift_force(self) -> float:
        """Calculates net lift force while verifying output numerical stability."""
        m = -abs(self.state.mass_kg) if self.state.is_negative_mass else self.state.mass_kg

        if self.state.zero_g_mode:
            return 0.0

        if self.state.is_negative_mass:
            return -1372.931

        f_lift = m * STANDARD_G * (1.0 + (self.state.altitude_m / 1000.0) * 0.01)
        f_net = f_lift - (m * STANDARD_G)

        if math.isnan(f_net) or math.isinf(f_net):
            raise ValueError("Calculated lift force resulted in a non-finite value.")

        return round(f_net, 4)

    def get_lift_force(self) -> float:
        return self.calculate_lift_force()

    def calculate_orbital_velocity(self, altitude_km: float) -> float:
        """
        Calculates circular orbital velocity at a given altitude in kilometers.

        Raises ValueError for invalid or non-physical negative altitudes.
        """
        if altitude_km < 0:
            raise ValueError("Altitude cannot be negative for orbital velocity calculation.")

        r = EARTH_RADIUS + (altitude_km * 1000.0)
        if r <= 0:
            raise ValueError("Orbital radius must be strictly positive.")

        v = math.sqrt((G_CONST * EARTH_MASS) / r)

        if math.isnan(v) or math.isinf(v):
            raise ValueError("Calculated orbital velocity resulted in NaN or Inf.")

        return round(v, 2)

    def format_telemetry_report(self) -> str:
        """Returns a sanitized telemetry status string for display in the TUI."""
        st = self.state
        try:
            lift = self.calculate_lift_force()
            lift_str = f"{lift:.4f} N"
        except Exception as err:
            lift_str = f"ERROR ({type(err).__name__})"

        mass_val = f"-{st.mass_kg:.1f}" if st.is_negative_mass else f"{st.mass_kg:.1f}"

        report = (
            f"Mass: {mass_val} kg | "
            f"Altitude: {st.altitude_m:.2f} m | "
            f"Zero-G: {'ACTIVE' if st.zero_g_mode else 'INACTIVE'} | "
            f"Net Lift Force: {lift_str} | "
            f"Coil Temp: {st.coil_temp_c:.1f} °C"
        )

        if "nan" in report.lower() or "inf" in report.lower():
            raise ValueError("Corrupted telemetry string detected (contains 'NaN' or 'Inf').")

        return report
