import subprocess
from pathlib import Path

# Define the payloads for the workspace
DEVCONTAINER_JSON = """{
    "name": "ez-antigravity-dev",
    "build": { "dockerfile": "Dockerfile" },
    "customizations": {
        "vscode": {
            "extensions": ["ms-python.python", "ms-python.vscode-pylance"]
        }
    }
}"""

DOCKERFILE = """FROM mcr.microsoft.com/devcontainers/python:3.11
RUN apt-get update && apt-get install -y git
WORKDIR /workspace
"""

REQUIREMENTS_TXT = "numpy\npytest\n"

# This is the updated vector-support content for the integrators
INTEGRATORS_PY = '''class FastEuler:
    """Fast Euler numerical integrator with vector support."""
    def __init__(self, dt=0.01):
        self.dt = dt

    def step(self, *args, **kwargs):
        if len(args) >= 4:
            pos, vel, accel_fn, dt = args[0], args[1], args[2], args[3]
            accel = accel_fn(pos, vel)
            new_vel = tuple(v + a * dt for v, a in zip(vel, accel))
            new_pos = tuple(p + v * dt for p, v in zip(pos, new_vel))
            return new_pos, new_vel
        elif len(args) == 2:
            engine, dt = args[0], args[1]
            for entity in getattr(engine, 'entities', []):
                if hasattr(entity, 'update_position'):
                    entity.update_position(dt)
            return engine
        return None

class PreciseRK4:
    """Precise Runge-Kutta 4th order numerical integrator."""
    def __init__(self, dt=0.01):
        self.dt = dt

    def step(self, *args, **kwargs):
        if len(args) >= 4:
            pos, vel, accel_fn, dt = args[0], args[1], args[2], args[3]
            k1_v = accel_fn(pos, vel)
            k1_p = vel
            k2_v = accel_fn(
                tuple(p + 0.5 * kp * dt for p, kp in zip(pos, k1_p)),
                tuple(v + 0.5 * kv * dt for v, kv in zip(vel, k1_v))
            )
            k2_p = tuple(v + 0.5 * kv * dt for v, kv in zip(vel, k1_v))
            k3_v = accel_fn(
                tuple(p + 0.5 * kp * dt for p, kp in zip(pos, k2_p)),
                tuple(v + 0.5 * kv * dt for v, kv in zip(vel, k2_v))
            )
            k3_p = tuple(v + 0.5 * kv * dt for v, kv in zip(vel, k2_v))
            k4_v = accel_fn(
                tuple(p + kp * dt for p, kp in zip(pos, k3_p)),
                tuple(v + kv * dt for v, kv in zip(vel, k3_v))
            )
            k4_p = tuple(v + kv * dt for v, kv in zip(vel, k3_v))
            new_pos = tuple(p + (dt / 6.0) * (k1_p[i] + 2 * k2_p[i] + 2 * k3_p[i] + k4_p[i]) for i, p in enumerate(pos))
            new_vel = tuple(v + (dt / 6.0) * (k1_v[i] + 2 * k2_v[i] + 2 * k3_v[i] + k4_v[i]) for i, v in enumerate(vel))
            return new_pos, new_vel
        elif len(args) == 2:
            engine, dt = args[0], args[1]
            for entity in getattr(engine, 'entities', []):
                if hasattr(entity, 'update_position'):
                    entity.update_position(dt)
            return engine
        return None
'''

def create_workspace():
    print("Quack! Starting atomic workspace deployment...")
    files = {
        Path(".devcontainer/devcontainer.json"): DEVCONTAINER_JSON,
        Path(".devcontainer/Dockerfile"): DOCKERFILE,
        Path("requirements.txt"): REQUIREMENTS_TXT,
        Path("src/ez_antigravity/integrators.py"): INTEGRATORS_PY
    }

    for filepath, content in files.items():
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"✅ Written file: {filepath}")

    # Final OPSEC touch: Stage everything to Git and fix permissions
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["chmod", "-R", "644", "src/ez_antigravity"], check=True)
        print("🎉 Workspace setup and Git staging completed successfully! Quack!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git staging failed: {e}")

if __name__ == "__main__":
    create_workspace()
