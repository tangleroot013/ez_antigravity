#!/usr/bin/env bash

==============================================================================

setup_project.sh

Automates directory creation, Devcontainer setup, script generation,

reference documentation creation, executable permissions, and Git initialization.

==============================================================================

set -e

echo "==> Creating project directory 'ez_grav_project' and structure..."
mkdir -p ez_grav_project/.devcontainer
cd ez_grav_project

echo "==> Initializing Git repository..."
git init

echo "==> Generating .devcontainer/devcontainer.json..."
cat << 'EOF' > .devcontainer/devcontainer.json
{
"name": "ez_grav Development Environment",
"image": "mcr.microsoft.com/devcontainers/python:1-3.11-bullseye",
"customizations": {
"vscode": {
"extensions": [
"ms-python.python",
"ms-python.vscode-pylance",
"streetsidesoftware.code-spell-checker"
]
}
},
"postCreateCommand": "pip3 install --user -r requirements.txt || true"
}
EOF

echo "==> Creating requirements.txt..."
cat << 'EOF' > requirements.txt

Core dependencies for ez_grav

pytest>=7.0.0
EOF

echo "==> Generating ez_grav.py executable script..."
cat << 'EOF' > ez_grav.py
#!/usr/bin/env python3
"""
ez_grav.py - Executable TUI & CLI Engine for Python Antigravity Ecosystem
"""

import sys
import os
import math
import time
import argparse
import webbrowser
import readline
from dataclasses import dataclass

Physical Constants

G_CONST = 6.67430e-11  # m^3 kg^-1 s^-2
EARTH_MASS = 5.972e24   # kg
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
verbose: bool = False

class GravEngine:
"""Core physics calculations and telemetry state for ez_grav."""

def __init__(self, mass_kg: float = 70.0, zero_g: bool = False, verbose: bool = False):
    self.state = PhysicsState(mass_kg=mass_kg, zero_g_mode=zero_g, verbose=verbose)
    self.log_buffer = []

def log(self, msg: str):
    timestamp = time.strftime("%H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    self.log_buffer.append(formatted)
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
    """Computes net lift force in Newtons."""
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
"""Interactive TUI and Command Handler."""

def __init__(self, engine: GravEngine):
    self.engine = engine
    self.running = True

def clear_screen(self):
    os.system("cls" if os.name == "nt" else "clear")

def print_header(self):
    print("\033[1;36m========================================================================\033[0m")
    print("\033[1;33m                        ez_grav CLI & TUI System                        \033[0m")
    print("\033[1;36m========================================================================\033[0m")

def render_telemetry(self):
    st = self.engine.state
    lift = self.engine.calculate_lift_force()
    mass_display = f"-{st.mass_kg}" if st.is_negative_mass else f"{st.mass_kg}"

    print("\033[1;32m--- SYSTEM TELEMETRY ---\033[0m")
    print(f" Payload Mass (m)    : {mass_display} kg")
    print(f" Hover Altitude      : {st.altitude_m} m")
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

def execute_slash_command(self, cmd_str: str):
    parts = cmd_str.strip().split()
    if not parts:
        return

    cmd = parts[0].lower()
    args = parts[1:]

    if cmd == "/fly":
        alt = float(args[0]) if args else 100.0
        self.engine.state.altitude_m = alt
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
        self.engine.log(f"Container Status: CPU Load {cpu_load}%, RAM {ram_mb}MB | Coil Temp: {self.engine.state.coil_temp_c}°C")

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
        self.running = False

    else:
        self.engine.log(f"Unknown command '{cmd}'. Type /help for assistance.")

def run_loop(self):
    self.engine.log("Session initialized. Ready for interaction.")
    while self.running:
        self.clear_screen()
        self.print_header()
        self.render_telemetry()
        self.render_logs()

        try:
            user_input = input("\033[1;35mez_grav> \033[0m").strip()
            if user_input.startswith("/"):
                self.execute_slash_command(user_input)
            elif user_input:
                self.engine.log(f"Raw Input: '{user_input}'. Use '/' for commands.")
        except (KeyboardInterrupt, EOFError):
            print("\nDisengaging lift coils...")
            self.running = False


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


def main():
args = parse_cli_args()
engine = GravEngine(mass_kg=args.mass, zero_g=args.zero_g, verbose=args.verbose)

if args.gui:
    webbrowser.open("https://xkcd.com/353/")

tui = TerminalUI(engine)
tui.run_loop()


if name == "main":
main()
EOF

echo "==> Generating ez_grav_cli_reference.md..."
cat << 'EOF' > ez_grav_cli_reference.md

ez_grav CLI & TUI Reference Manual

ez_grav is a lightweight Terminal User Interface (TUI) and Command-Line Interface (CLI) engine designed for Python's antigravity ecosystem.

1. Global CLI Startup Flags

Flag

Short

Value Type

Default Value

Description

--gui

-g

Boolean

false

Automatically opens the Python antigravity browser hook (xkcd.com/353) on startup.

--zero-g

-z

Boolean

false

Initializes the session with zero-gravity field simulation active.

--config

-c

File Path

~/.config/ez_grav.yaml

Specifies a custom YAML configuration file for user-defined defaults.

--mass

-m

Float (kg)

70.0

Sets the initial payload mass ($m$) used for net lift force calculations.

--verbose

-v

Boolean

false

Enables detailed debug log output in the bottom event panel.

--help

-h

None

N/A

Prints the command-line usage summary and exits.

2. Interactive TUI Slash Commands

Command

Arguments

Arg Types

Default

Functionality & Effect

/fly

[altitude_m]

Float

100.0

Engages hover coils and sets target levitation height in meters.

/xkcd

[comic_num]

Integer/String

353

Triggers the browser hook to open the specified xkcd comic.

/zero-g

[on|off]

String/Bool

on

Toggles the zero-gravity anti-gravitational field matrix on or off.

/mass-swap

[mass_kg]

Float

(current)

Updates payload mass $m_0$ and flips mass tensor sign ($+m \leftrightarrow -m$).

/orbit

[altitude_km]

Float

400.0

Calculates required circular orbital velocity ($v = \sqrt{\frac{GM}{r}}$) at altitude.

/metric

[flat|curved]

String

flat

Switches local spacetime metric tensor parameterization ($g_{\mu\nu}$).

/status

None

N/A

N/A

Telemeters container host CPU/RAM utilization and coil temperatures.

/config

[key] [val]

Key-Value Pair

N/A

Reads or dynamically updates runtime configuration settings in memory.

/clear

None

N/A

N/A

Flushes all entries from the lower TUI event log buffer.

/quit

None

N/A

N/A

Safely disengages lift coils and exits the ez_grav shell interface.

EOF









echo "==> Generating README.md..."
cat << 'EOF' > README.md

ez_grav Project

Lightweight TUI and CLI companion for Python's antigravity ecosystem.

Quickstart

./ez_grav.py --mass 85 --zero-g


See ez_grav_cli_reference.md for full documentation and command palette options.
EOF

echo "==> Setting executable permissions..."
chmod +x ez_grav.py

echo "==> Staging and committing files to Git..."
git add .
git commit -m "Initial commit: Set up ez_grav engine, devcontainer, and documentation"

echo "==> Setup completed successfully!"
EOF
