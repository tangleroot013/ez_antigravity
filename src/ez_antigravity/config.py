import os
from pathlib import Path


class Config:
    """OPSEC-hardened configuration for ez_antigravity."""
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    LOG_DIR = BASE_DIR / "logs"
    BACKUP_DIR = BASE_DIR / "backups"

    # Engine Defaults
    DEFAULT_TOLERANCE = float(os.getenv("AGY_TOLERANCE", 1e-9))
    MAX_ITERATIONS = int(os.getenv("AGY_MAX_ITER", 10000))

    # Resilience settings
    ENABLE_CHECKPOINTS = os.getenv("AGY_CHECKPOINTS", "True") == "True"
    CHECKPOINT_INTERVAL = int(os.getenv("AGY_CHECK_INT", 100))

    @classmethod
    def ensure_dirs(cls):
        """Ensure critical directories exist. Quack!"""
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)
        cls.BACKUP_DIR.mkdir(parents=True, exist_ok=True)


Config.ensure_dirs()
