import pytest
import math
from src.ez_grav import GravEngine

@pytest.mark.parametrize("altitude_km, expected_behavior", [
    (0.0, "stable"),          # Surface level
    (-1.0, "exception"),      # Sub-surface (Invalid)
    (1000.0, "stable"),       # High orbit
    (1e12, "stable"),         # Deep space / Galactic scale
])
def test_orbital_velocity_boundaries(altitude_km, expected_behavior):
    engine = GravEngine()
    
    if expected_behavior == "exception":
        with pytest.raises(ValueError, match="Altitude cannot be negative"):
            engine.calculate_orbital_velocity(altitude_km)
    else:
        result = engine.calculate_orbital_velocity(altitude_km)
        assert not math.isnan(result)
        assert not math.isinf(result)
        assert result > 0

def test_telemetry_report_sanitization():
    # Force a state that might cause issues (Extreme mass)
    engine = GravEngine(mass_kg=1e30) 
    
    # We want to ensure that even if physics goes wild, 
    # the report doesn't crash the TUI.
    report = engine.format_telemetry_report()
    
    assert "nan" not in report.lower()
    assert "inf" not in report.lower()
    assert "Mass:" in report
    assert "Coil Temp:" in report

def test_emergency_cutoff_logic():
    # Initialize engine with zero-g and high temp
    engine = GravEngine(zero_g=True)
    engine.state.coil_temp_c = 100.0 # Above OVERHEAT_CUTOFF (99.0)
    
    # Tick the engine to trigger the safety logic
    logs = engine.state.tick(dt=1.0)
    
    assert engine.state.zero_g_mode is False
    assert engine.state.altitude_m == 0.0
    assert any("EMERGENCY AUTO-CUTOFF" in log for log in logs)

print("\nTelemetry gauntlet completed. Quack!")
