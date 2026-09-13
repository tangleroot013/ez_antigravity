import logging
from .config import Config


def setup_telemetry(level=logging.INFO):
    """Configures the global logger for engine resilience."""
    log_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

    # File Handler for persistence
    file_handler = logging.FileHandler(Config.LOG_DIR / "engine.log")
    file_handler.setFormatter(log_format)

    # Console Handler for real-time monitoring
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)

    logger = logging.getLogger("ez_antigravity")
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Global instance for easy import
logger = setup_telemetry()


class FlightTelemetry:
    """Collects simulation telemetry and writes it as JSON."""

    def __init__(self, filename=None):
        from pathlib import Path

        self.filename = (
            Path(filename)
            if filename is not None
            else Path("logs") / "flight_log.json"
        )
        self.records = []

    @staticmethod
    def _serialize(value):
        """Convert NumPy-like values into JSON-compatible values."""
        if hasattr(value, "tolist"):
            return value.tolist()

        if isinstance(value, dict):
            return {
                str(key): FlightTelemetry._serialize(item)
                for key, item in value.items()
            }

        if isinstance(value, (list, tuple)):
            return [FlightTelemetry._serialize(item) for item in value]

        return value

    def record(self, step, pos, vel, net_accel, status):
        """Store one simulation telemetry record."""
        self.records.append(
            {
                "step": int(step),
                "position": self._serialize(pos),
                "velocity": self._serialize(vel),
                "net_acceleration": self._serialize(net_accel),
                "status": self._serialize(status),
            }
        )

    def finalize(self):
        """Persist all collected records to JSON."""
        import json
        from pathlib import Path

        path = Path(self.filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as handle:
            json.dump(self.records, handle, indent=2)

        logger.info("Flight telemetry finalized: %s", path)
        return path
