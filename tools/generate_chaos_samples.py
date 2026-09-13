import json
import os


def generate_adversarial_samples():
    samples_dir = "tests/real_world_samples"
    os.makedirs(samples_dir, exist_ok=True)

    scenarios = {
        "singularity": {"mass": 1e30, "dist": 0.0},
        "vacuum": {"mass": 0.0, "dist": 1e10},
        "nan_injection": {"mass": float("nan"), "dist": 1.0},
        "extreme_velocity": {"mass": 1.0, "dist": 1e-5, "vel": 299792458},
    }

    for name, data in scenarios.items():
        path = f"{samples_dir}/{name}.json"
        with open(path, "w") as f:
            json.dump(data, f)
        print(f"Quack! Generated chaos sample: {path}")


if __name__ == "__main__":
    generate_adversarial_samples()
