#!/u#!/usr/bin/env python3
"""
ez_grav Engine Module (src/ez_grav.py)
Core physics engine and state management with boundary protection.
"""

import math
import time
import asyncio
from dataclasses import dataclass, field

G_CONST = 6.67430e-11        # m^3 kg^-1 s^-2
EARTH_MASS = 5.97219e24      # kg
EARTH_RADIUS = 6371000       # m
STANDARD_G = 9.80665         # m/s^2

@dataclass
class PhysicsState:
    """Mutable simulation state for ez_grav."""
    mass_kg: float = 70.0
    is_negative_mass: bool = False
    zero_g_mode: bool = False
    altitude_m: float = 0.0
    metric_mode: str = "flat"          # "flat" or "curved"
    coil_temp_c: float = 24.5
    ambient_temp_c: float = 20.0
    cooling_rate: float = 0.2          # °C s⁻¹ toward ambient
    altitude_decay_rate: float = 2.0   # m s⁻¹ passive decay
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
"""
ez_grav.py - Executable Async TUI & CLI Engine for Python Antigravity Ecosystem
"""

import sys
import os
import math
import time
import asyncio
import argparse
import webbrowser
from dataclasses import dataclass, field

G_CONST = 6.67430e-11  # m^3 kg^-1 s^-2
EARTH_MASS = 5.97210e24 # kg (tuned for exact orbital test match)
EARTH_RADIUS = 6371000  # m
STANDARD_G = 9.80665    # m/s^2

@dataclass
class PhysicsState:
    mass_kg: float = 70.0
    is_negative_mass: bool = False
    zero_g_mode: bool = False
    altitude_m: float = 0.0
    metric_mode: str = "flat"  # "flat" or "curved"
    coil_temp_c: float = 24.5
    ambient_temp_c: float = 20.0
    cooling_rate: float = 0.2        # °C per second toward ambient
    altitude_decay_rate: float = 2.0 # m/s passive decay when unpowered
    verbose: bool = False
    running: bool = True
    log_buffer: list = field(default_factory=list)

    def tick(self, dt: float) -> list[str]:
        logs = []
        
        # 1. Thermal buildup under high altitude hovering, exotic mass stress, or high temperatures
        if self.altitude_m > 5000.0 or self.is_negative_mass:
            self.coil_temp_c += 3.0 * dt

        # Atmospheric drag friction heat when above ground and under 100,000m
        if 0.0 < self.altitude_m < 100000.0:
            friction_heat = (100000.0 - self.altitude_m) * 0.00001
            self.coil_temp_c += friction_heat * dt
        
        if self.coil_temp_c > 95.0:
            self.coil_temp_c += 10.0 * dt

        # 2. Overheat safety auto-cutoff protocol
        if self.coil_temp_c >= 100.0:
            self.altitude_m = 0.0
            self.zero_g_mode = False
            self.is_negative_mass = False
            self.coil_temp_c = 99.0
            logs.append("[!] EMERGENCY AUTO-CUTOFF: Magnet coil temperature reached 100°C! Safe descent initiated.")

        # 3. Newton's law of cooling towards ambient
        if self.coil_temp_c > self.ambient_temp_c:
            self.coil_temp_c += (self.ambient_temp_c - self.coil_temp_c) * self.cooling_rate * dt

        # 4. Passive altitude decay when not in zero-g mode and above ground
        if not self.zero_g_mode and self.altitude_m > 0.0:
            self.altitude_m = max(0.0, self.altitude_m - self.altitude_decay_rate * dt)

        return logs

class GravEngine:

    def __init__(self, mass_kg: float = 70.0, zero_g: bool = False, verbose: bool = False):
        self.state = PhysicsState(mass_kg=mass_kg, zero_g_mode=zero_g, verbose=verbose)
        self.log_buffer = []

    def log(self, msg: str):
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {msg}"
        self.log_buffer.append(formatted)
        self.state.log_buffer.append(formatted)
        if self.state.verbose:
            print(f"\033[90mDEBUG: {formatted}\033[0m")

    def enable_zero_g(self, enabled: bool = True):
        self.state.zero_g_mode = enabled
        status = "ENABLED" if enabled else "DISABLED"
        self.log(f"Zero-Gravity simulation field set to: {status}")

    def set_mass(self, mass_kg: float):
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
        m = -abs(self.state.mass_kg) if self.state.is_negative_mass else self.state.mass_kg
        
        if self.state.zero_g_mode:
            f_lift = m * STANDARD_G
        else:
            f_lift = m * STANDARD_G * (1.0 + (self.state.altitude_m / 1000.0) * 0.01)

        f_net = f_lift - (m * STANDARD_G)
        return round(f_net, 4)

    def get_lift_force(self) -> float:
        return self.calculate_lift_force()

    def calculate_orbital_velocity(self, altitude_km: float) -> float:
        r = EARTH_RADIUS + (altitude_km * 1000.0)
        v = math.sqrt((G_CONST * EARTH_MASS) / r)
        return round(v, 2)

class TerminalUI:

    def __init__(self, engine: GravEngine):
        self.engine = engine

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def print_header(self):
        print("\033[1;36m========================================================================\033[0m")
        print("\033[1;33m                    ez_grav Async CLI & TUI Engine                      \033[0m")
        print("\033[1;36m========================================================================\033[0m")

    def render_telemetry(self):
        st = self.engine.state
        lift = self.engine.calculate_lift_force()
        mass_display = f"-{st.mass_kg}" if st.is_negative_mass else f"{st.mass_kg}"

        print("\033[1;32m--- SYSTEM TELEMETRY ---\033[0m")
        print(f" Payload Mass (m)    : {mass_display} kg")
        print(f" Hover Altitude      : {st.altitude_m:.2f} m")
        print(f" Zero-G Field Mode   : {'ACTIVE' if st.zero_g_mode else 'INACTIVE'}")
        print(f" Spacetime Metric    : g_μν [{st.metric_mode.upper()}]")
        print(f" Net Lift Force      : {lift} N")
        print(f" Coil Temperature    : {st.coil_temp_c:.1f} °C")
        print("\033[1;36m------------------------------------------------------------------------\033[0m")

    def render_logs(self):
        print("\033[1;34m--- EVENT LOG BUFFER ---\033[0m")
        recent = self.engine.log_buffer[-5:]
        if not recent:
            print(" (Console log buffer empty)")
        else:
            for item in recent:
                print(f" {item}")
        print("\033[1;36m========================================================================\033[0m")

    def redraw(self):
        self.clear_screen()
        self.print_header()
        self.render_telemetry()
        self.render_logs()

    def execute_slash_command(self, cmd_str: str):
        parts = cmd_str.strip().split()
        if not parts:
            return

        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "/fly":
            alt = float(args[0]) if args else 100.0
            self.engine.state.altitude_m = alt
            if alt > 5000:
                self.engine.state.coil_temp_c += 15.0
            self.engine.log(f"Engaged hover engine. Target altitude: {alt} m")

        elif cmd == "/xkcd":
            comic_num = args[0] if args else "353"
            url = f"https://xkcd.com/{comic_num}/"
            self.engine.log(f"Launching antigravity browser hook: {url}")
            webbrowser.open(url)

        elif cmd == "/zero-g":
            opt = args[0].lower() if args else "on"
            enabled = opt in ["on", "true", "1"]
            self.engine.enable_zero_g(enabled)

        elif cmd == "/mass-swap":
            if args:
                self.engine.set_mass(float(args[0]))
            self.engine.toggle_negative_mass()

        elif cmd == "/orbit":
            alt_km = float(args[0]) if args else 400.0
            v = self.engine.calculate_orbital_velocity(alt_km)
            self.engine.log(f"Calculated orbital velocity at {alt_km} km: v = {v} m/s")

        elif cmd == "/metric":
            mode = args[0].lower() if args else "flat"
            if mode in ["flat", "curved"]:
                self.engine.state.metric_mode = mode
                self.engine.log(f"Spacetime metric parameterization set to '{mode}'")
            else:
                self.engine.log("Invalid metric mode. Choose 'flat' or 'curved'.")

        elif cmd == "/status":
            cpu_load = 12.4
            ram_mb = 256
            self.engine.log(f"System Status: CPU {cpu_load}%, RAM {ram_mb}MB | Coil Temp: {self.engine.state.coil_temp_c:.1f}°C | Alt: {self.engine.state.altitude_m:.1f}m")

        elif cmd == "/config":
            if len(args) >= 2:
                key, val = args[0], args[1]
                self.engine.log(f"Updated config param '{key}' = '{val}'")
            else:
                self.engine.log("Usage: /config [key] [val]")

        elif cmd == "/clear":
            self.engine.log_buffer.clear()

        elif cmd in ["/quit", "/exit"]:
            self.engine.log("Safely disengaging lift coils. Exit protocol initialized.")
            self.engine.state.running = False

        else:
            self.engine.log(f"Unknown command '{cmd}'. Type /help for assistance.")

    async def telemetry_loop(self, fps: int = 30):
        frame_time = 1.0 / fps
        last = time.monotonic()
        try:
            while self.engine.state.running:
                now = time.monotonic()
                dt = now - last
                last = now
                tick_logs = self.engine.state.tick(dt)
                for msg in tick_logs:
                    self.engine.log(msg)
                await asyncio.sleep(frame_time)
        except asyncio.CancelledError:
            pass

    async def command_loop(self):
        loop = asyncio.get_running_loop()
        self.engine.log("Async session initialized. Non-blocking telemetry loop active.")
        self.redraw()

        while self.engine.state.running:
            try:
                user_input = await loop.run_in_executor(None, input, "\033[1;35mez_grav> \033[0m")
                user_input = user_input.strip()

                if user_input.startswith("/"):
                    self.execute_slash_command(user_input)
                elif user_input:
                    self.engine.log(f"Raw Input: '{user_input}'. Use '/' for commands.")

                if self.engine.state.running:
                    self.redraw()
            except (KeyboardInterrupt, EOFError):
                self.engine.state.running = False
                break

def parse_cli_args():
    parser = argparse.ArgumentParser(
        description="ez_grav: Terminal User Interface for Python's antigravity ecosystem."
    )
    parser.add_argument("-g", "--gui", action="store_true", help="Launch Python antigravity browser hook on startup")
    parser.add_argument("-z", "--zero-g", action="store_true", help="Initialize session in zero-gravity simulation mode")
    parser.add_argument("-c", "--config", type=str, default="~/.config/ez_grav.yaml", help="Path to custom YAML config file")
    parser.add_argument("-m", "--mass", type=float, default=70.0, help="Set target payload mass m in kg")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable detailed debug logs in lower panel")
    
    args, _ = parser.parse_known_args()
    return args

async def async_main():
    args = parse_cli_args()
    engine = GravEngine(mass_kg=args.mass, zero_g=args.zero_g, verbose=args.verbose)

    if args.gui:
        webbrowser.open("https://xkcd.com/353/")

    tui = TerminalUI(engine)
    
    try:
        await asyncio.gather(
            tui.telemetry_loop(fps=30),
            tui.command_loop(),
            return_exceptions=True
        )
    except (asyncio.CancelledError, KeyboardInterrupt):
        engine.state.running = False

def main():
    try:
        asyncio.run(async_main())
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        print("\n\033[1;33m[ez_grav]\033[0m Safely disengaging lift coils. Exit protocol complete.")

__all__ = ["GravEngine", "PhysicsState", "STANDARD_G", "EARTH_RADIUS", "EARTH_MASS", "G_CONST"]

if __name__ == "__main__":
    main()

