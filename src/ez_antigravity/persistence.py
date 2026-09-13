import pickle
from .config import Config
from .telemetry import logger


def save_checkpoint(state, filename="checkpoint.pkl"):
    """Saves the current engine state to the backup directory. Quack!"""
    path = Config.BACKUP_DIR / filename
    try:
        with open(path, 'wb') as f:
            pickle.dump(state, f)
        logger.info(f"Checkpoint saved successfully to {path}")
    except Exception as e:
        logger.error(f"Failed to save checkpoint: {e}")


def load_checkpoint(filename="checkpoint.pkl"):
    """Loads the last known good state from disk."""
    path = Config.BACKUP_DIR / filename
    if not path.exists():
        logger.warning("No checkpoint file found. Starting from scratch.")
        return None
    try:
        with open(path, 'rb') as f:
            state = pickle.load(f)
        logger.info(f"Checkpoint restored from {path}")
        return state
    except Exception as e:
        logger.error(f"Failed to load checkpoint: {e}")
        return None
