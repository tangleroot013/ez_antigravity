import json
import os
from datetime import datetime


class FlightTelemetry:
    """Structured logging for simulation state and health with self-healing files."""  # noqa: E501

    def __init__(self, filename="flight_log.json"):
        self.filename = filename
        self.logs = []
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Creates the log file with an empty list if it doesn't exist."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)

    def record(self, step, position, velocity, acceleration, status="NOMINAL"):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "step": step,
            "r": position,
            "v": velocity,
            "a": acceleration,
            "status": status
        }
        self.logs.append(entry)
        if len(self.logs) >= 100:
            self.flush()

    def flush(self):
        self._ensure_file_exists()
        try:
            with open(self.filename, 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                data.extend(self.logs)
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
            self.logs = []
        except Exception as e:
            print(f"Telemetry Flush Error: {e}")

    def finalize(self):
        self.flush()
