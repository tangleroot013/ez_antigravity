#!/usr/bin/env python3

"""agy-shell: interactive sandbox REPL for ez_antigravity."""

from __future__ import annotations

import code
import rlcompleter
import sys
from pathlib import Path

try:
    import readline
except ImportError:
    readline = None


def find_project_root() -> Path:
    """Locate the project root directory."""

    if "__file__" in globals():
        file_path = Path(__file__).resolve()

        if file_path.name != "<string>" and file_path.exists():
            if file_path.parent.name == "scripts":
                return file_path.parent.parent
            return file_path.parent

    cwd = Path.cwd()

    for candidate in [cwd] + list(cwd.parents):
        if (
            (candidate / "src" / "ez_grav.py").exists()
            or (candidate / "ez_grav.py").exists()
        ):
            return candidate

    return cwd


PROJECT_ROOT = find_project_root()
SRC_DIR = PROJECT_ROOT / "src"


def add_import_paths() -> None:
    """Make the project root and src directory importable."""

    for path in (SRC_DIR, PROJECT_ROOT, Path.cwd(), Path.cwd() / "src"):
        path_string = str(path)

        if path.exists() and path_string not in sys.path:
            sys.path.insert(0, path_string)


def load_physics():
    """Import and return the physics API."""

    try:
        from ez_grav import (
            EARTH_MASS,
            EARTH_RADIUS,
            G_CONST,
            STANDARD_G,
            GravEngine,
        )

        return (
            GravEngine,
            G_CONST,
            EARTH_MASS,
            EARTH_RADIUS,
            STANDARD_G,
        )

    except ImportError as first_error:
        try:
            from src.ez_grav import (
                EARTH_MASS,
                EARTH_RADIUS,
                G_CONST,
                STANDARD_G,
                GravEngine,
            )

            return (
                GravEngine,
                G_CONST,
                EARTH_MASS,
                EARTH_RADIUS,
                STANDARD_G,
            )

        except ImportError as second_error:
            print(
                "❌ Could not import GravEngine.\n"
                f"Primary import error: {first_error}\n"
                f"Fallback import error: {second_error}\n"
                "Make sure the project contains src/ez_grav.py.",
                file=sys.stderr,
            )
            raise SystemExit(1)


def print_status(engine) -> None:
    """Print current engine telemetry."""

    state = engine.state

    coil_temp = getattr(state, "coil_temp_k", None)

    if coil_temp is None:
        coil_temp = getattr(state, "temp_k", None)

    if coil_temp is None:
        coil_temp = getattr(engine, "coil_temp_k", None)

    temp_display = (
        f"{coil_temp} K"
        if coil_temp is not None
        else "N/A"
    )

    print("\n--- 🦆 AGY Engine Status ---")
    print(f" Mass: {state.mass_kg} kg")
    print(f" Altitude: {state.altitude_m} m")
    print(f" Coil Temp: {temp_display}")
    print(f" Local Gravity: {engine.local_gravity():.6f} m/s²")
    print(f" Lift Force: {engine.calculate_lift_force():.2f} N")
    print(
        " Orbital Velocity: "
        f"{engine.calculate_orbital_velocity(400):.2f} m/s "
        "(at 400 km)"
    )
    print("-----------------------------\n")


def configure_completion(namespace: dict[str, object]) -> None:
    """Enable readline tab completion if available."""

    if readline is None:
        print("⚠️ Tab completion is unavailable on this platform.")
        return

    completer = rlcompleter.Completer(namespace)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")


def build_banner() -> str:
    return (
        "====================================================\n"
        " 🦆 AGY-SHELL: GravEngine Sandbox REPL 🦆 \n"
        "====================================================\n"
        "Pre-loaded symbols:\n"
        " - GravEngine\n"
        " - engine\n"
        " - status()\n"
        " - G_CONST, EARTH_MASS, EARTH_RADIUS, STANDARD_G\n"
        "\n"
        "Try:\n"
        " >>> engine.calculate_lift_force()\n"
        " >>> engine.local_gravity()\n"
        " >>> engine.state.mass_kg = -70.0\n"
        " >>> status()\n"
        "===================================================="
    )


def main() -> int:
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: python scripts/agy-shell.py")
        print("Launches an interactive GravEngine sandbox REPL.")
        return 0

    add_import_paths()

    (
        GravEngine,
        G_CONST,
        EARTH_MASS,
        EARTH_RADIUS,
        STANDARD_G,
    ) = load_physics()

    engine = GravEngine()

    namespace: dict[str, object] = {
        "GravEngine": GravEngine,
        "engine": engine,
        "status": lambda: print_status(engine),
        "G_CONST": G_CONST,
        "EARTH_MASS": EARTH_MASS,
        "EARTH_RADIUS": EARTH_RADIUS,
        "STANDARD_G": STANDARD_G,
    }

    configure_completion(namespace)

    code.interact(
        banner=build_banner(),
        local=namespace,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
