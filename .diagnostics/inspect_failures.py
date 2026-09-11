from pathlib import Path
import ast

source_path = Path("src/ez_grav.py")
source = source_path.read_text(encoding="utf-8")
tree = ast.parse(source)

wanted = {
    "PhysicsState",
    "GravEngine",
    "calculate_lift_force",
    "calculate_orbital_velocity",
    "toggle_negative_mass",
    "tick",
    "format_telemetry_report",
}

for node in ast.walk(tree):
    name = getattr(node, "name", None)
    if name in wanted:
        start = node.lineno
        end = getattr(node, "end_lineno", start)
        lines = source.splitlines()
        print(f"\n--- {name}: lines {start}-{end} ---")
        print("\n".join(f"{n:4}: {lines[n - 1]}" for n in range(start, end + 1)))

print("\n--- Constants and declarations ---")
for n, line in enumerate(source.splitlines(), 1):
    if any(token in line for token in (
        "G_CONST",
        "EARTH_MASS",
        "EARTH_RADIUS",
        "GRAVITY",
        "OVERHEAT",
        "cooling_rate",
        "coil_temp",
    )):
        print(f"{n:4}: {line}")
