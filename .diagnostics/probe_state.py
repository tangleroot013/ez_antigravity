from src.ez_grav import (
    PhysicsState,
    GravEngine,
    G_CONST,
    EARTH_MASS,
    EARTH_RADIUS,
)

print("constants:")
print("G_CONST =", G_CONST)
print("EARTH_MASS =", EARTH_MASS)
print("EARTH_RADIUS =", EARTH_RADIUS)

print("\nconstructor probe:")
state = PhysicsState(
    coil_temp_c=99.5,
    altitude_m=1000.0,
    zero_g_mode=True,
)

print(state)
print("coil_temp_c =", state.coil_temp_c)
print("altitude_m =", state.altitude_m)
print("zero_g_mode =", state.zero_g_mode)

print("\ntick probe:")
try:
    logs = state.tick(dt=1.0)
    print("logs =", logs)
    print("state after tick =", state)
except Exception as exc:
    print(type(exc).__name__, str(exc))

print("\nengine probe:")
engine = GravEngine(mass_kg=70.0, zero_g=False)
print("initial state =", engine.state)
engine.toggle_negative_mass(True)
print("negative-mass state =", engine.state)
print("lift force =", engine.calculate_lift_force())

print("\norbital probe:")
for altitude in (400.0, -1.0):
    try:
        print(altitude, "=>", engine.calculate_orbital_velocity(altitude))
    except Exception as exc:
        print(altitude, "=>", type(exc).__name__, str(exc))

print("\ntelemetry probe:")
try:
    print(engine.format_telemetry_report())
except Exception as exc:
    print(type(exc).__name__, str(exc))
