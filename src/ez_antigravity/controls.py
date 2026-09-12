class ThrustController:
    """Interface for applying active control forces to the engine."""
    
    def __init__(self, max_thrust_n=500.0):
        self.max_thrust = max_thrust_n
        self.active_thrust = 0.0

    def set_thrust(self, value: float):
        """Sets thrust in Newtons, clamped to max_thrust."""
        self.active_thrust = max(min(value, self.max_thrust), -self.max_thrust)

    def get_acceleration(self, mass_kg):
        """Converts thrust force to acceleration: a = F/m"""
        return self.active_thrust / mass_kg

    def emergency_stop(self):
        """Kills all thrust immediately."""
        self.active_thrust = 0.0
