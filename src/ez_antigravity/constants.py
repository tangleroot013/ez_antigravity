"""Physical constants for the ez_antigravity package.
These are imported by every other module, so they must **not** import
any other ez_antigravity code – that’s what breaks the circular import.
"""

# Fundamental
G_CONST = 6.67430e-11          # m³·kg⁻¹·s⁻²
LIGHT_SPEED = 299_792_458.0   # m·s⁻¹
AU = 1.495_978_707e11         # astronomical unit, m

# Solar system bodies
SUN_MASS = 1.988_47e30        # kg
SUN_RADIUS = 6.963_40e8       # m

EARTH_MASS = 5.972_2e24       # kg
EARTH_RADIUS = 6.371_0e6      # m

MOON_MASS = 7.342e22          # kg
MOON_RADIUS = 1.737_4e6       # m

MARS_MASS = 6.417_1e23        # kg
MARS_RADIUS = 3.389_5e6       # m

JUPITER_MASS = 1.898_2e27     # kg
JUPITER_RADIUS = 6.991_1e7    # m

# Unit conversion helpers
KM_TO_M = 1_000.0
M_TO_KM = 0.001
DAY_TO_SEC = 86_400.0
HOUR_TO_SEC = 3_600.0

# Engine defaults
DEFAULT_TIME_STEP = 60.0          # s
DEFAULT_SOFTENING = 1.0e-9        # m (softening length)

# Real-world resilience constants
RHO_0 = 1.225            # Sea level air density (kg/m^3)
SCALE_HEIGHT = 8500.0    # Atmospheric scale height (m)
J2_CONSTANT = 1.0826e-3  # Earth's second zonal harmonic (oblateness)
DRAG_COEFF = 2.2         # Typical satellite drag coefficient
CROSS_SECTION_AREA = 10.0  # Satellite cross-section (m^2)
