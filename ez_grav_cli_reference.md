ez_grav CLI & TUI Reference Manual

ez_grav is a lightweight Terminal User Interface (TUI) and Command-Line Interface (CLI) engine designed for Python's antigravity ecosystem. It combines real-time system telemetry monitoring, relativistic spacetime metric adjustments, and an interactive slash-command palette within a unified shell interface.

1. Global CLI Startup Flags

When launching ez_grav from a terminal shell, the following flags control session initialization parameters and runtime defaults:

Flag

Short

Value Type

Default Value

Description

--gui

-g

Boolean

false

Automatically opens the Python antigravity browser hook (xkcd.com/353) on startup.

--zero-g

-z

Boolean

false

Initializes the session with zero-gravity field simulation active.

--config

-c

File Path

~/.config/ez_grav.yaml

Specifies a custom YAML configuration file for user-defined defaults.

--mass

-m

Float (kg)

70.0

Sets the initial payload mass ($m$) used for net lift force calculations.

--verbose

-v

Boolean

false

Enables detailed debug log output in the bottom event panel.

--help

-h

None

N/A

Prints the command-line usage summary and exits.

2. Interactive TUI Slash Commands

Inside an active ez_grav session, typing / accesses the interactive command palette. All available slash commands and their parameters are detailed below:

Command

Arguments

Arg Types

Default

Functionality & Effect

Example Usage

/fly

[altitude_m]

Float

100.0

Engages hover coils and sets target levitation height in meters.

/fly 250.5

/xkcd

[comic_num]

Integer/String

353

Triggers the browser hook to open the specified xkcd comic.

/xkcd 353

/zero-g

[on|off]

String/Bool

on

Toggles the zero-gravity anti-gravitational field matrix on or off.

/zero-g off

/mass-swap

[mass_kg]

Float

(current)

Updates payload mass $m_0$ and flips the mass tensor sign ($+m \leftrightarrow -m$).

/mass-swap 85

/orbit

[altitude_km]

Float

400.0

Calculates required circular orbital velocity ($v = \sqrt{\frac{GM}{r}}$) at altitude.

/orbit 400

/metric

[flat|curved]

String

flat

Switches local spacetime metric tensor parameterization ($g_{\mu\nu}$).

/metric curved

/status

None

N/A

N/A

Telemeters Crostini container host CPU/RAM utilization and coil temperatures.

/status

/config

[key] [val]

Key-Value Pair

N/A

Reads or dynamically updates runtime configuration settings in memory.

/config coil_temp 22.0

/clear

None

N/A

N/A

Flushes all entries from the lower TUI event log buffer.

/clear

/quit

None

N/A

N/A

Safely disengages lift coils and exits the ez_grav shell interface.

/quit

/exit

None

N/A

N/A

Alias for /quit. Initiates clean shutdown protocol.

/exit

3. Default Keyboard Shortcuts

ez_grav includes home-row friendly hotkeys for fast control without interrupting terminal workflow:

Key Combination

Command Scope

Primary Action

Triggered Effect

Ctrl + G

Global

Quick Zero-G Field Toggle

Immediately toggles zero-gravity simulation mode.

Space

Global

Pause / Resume Physics Loop

Freezes active altitude drift and telemetry calculations.

Up Arrow / Down Arrow

Input Field

Slash Command History

Cycles backward and forward through previous command inputs.

j / k

Navigation

Log Scroll (Down / Up)

Scrolls the lower event log buffer line by line.

Shift + L

Global

Direct Browser Shortcut

Opens https://xkcd.com/353/ in the default system browser.

Ctrl + R

Global

Spatial Recalibration

Resets spacetime metric parameters and vector fields.

Ctrl + L

Global

Screen Redraw

Clears the terminal screen and redraws telemetry panels.

Tab

Input Field

Autocomplete

Auto-completes matching slash commands and keywords.

Ctrl + C / q

Global

Emergency Disengage

Triggers safe descent sequence and terminates process.

4. System Telemetry & Monitoring Panel

The top panel of the ez_grav TUI updates continuously with live telemetry data:

Telemetry Field

Display Format

Unit

Description

Payload Mass ($m$)

+70.0 / -70.0

kg

Current mass tensor value; negative indicates exotic mass mode.

Hover Altitude

0.0 to 10000.0

m

Active calculated levitation height above sea level.

Zero-G Field Mode

ACTIVE / INACTIVE

N/A

Status indicator for zero-gravity field generation.

Spacetime Metric

g_μν [FLAT] / [CURVED]

N/A

Active geometric model for gravity calculations.

Net Lift Force ($F_{\text{net}}$)

+686.4655

N

Net upward thrust after accounting for gravimetric pull.

Coil Temperature

24.5

°C

Superconducting magnetic coil thermal sensor readings.

5. Physics Engine & Mathematical Specifications

ez_grav models anti-gravitational dynamics using both standard Newtonian mechanics and General Relativistic metric adjustments:

1. Net Lift Force Calculation

When negative mass tensor or zero-g mode is engaged, net lift force $F_{\text{net}}$ is derived as:

$$F_{\text{lift}} = m \cdot g \cdot \left(1.0 + \frac{h}{1000} \cdot 0.01\right)$$

$$F_{\text{net}} = F_{\text{lift}} - (m \cdot g)$$

Where:

$m$: Payload mass in kilograms ($\text{kg}$)

$g$: Standard earth gravity acceleration ($9.80665 \text{ m/s}^2$)

$h$: Altitude in meters ($\text{m}$)

2. Circular Orbital Velocity

Required orbital speed $v$ for stable low-Earth orbit simulation:

$$v = \sqrt{\frac{G \cdot M_{\text{Earth}}}{R_{\text{Earth}} + h_{\text{orbit}}}}$$

Where:

$G = 6.67430 \times 10^{-11} \text{ m}^3 \text{kg}^{-1} \text{s}^{-2}$

$M_{\text{Earth}} = 5.972 \times 10^{24} \text{ kg}$

$R_{\text{Earth}} = 6,371,000 \text{ m}$

6. Python API Integration Quickstart

The ez_grav engine can also be invoked programmatically inside custom Python scripts:

import ez_grav

# 1. Instantiate physics engine with default parameters
engine = ez_grav.GravEngine(mass_kg=85.0, zero_g=True, verbose=True)

# 2. Engage zero-gravity simulation field
engine.enable_zero_g(True)

# 3. Calculate net lift force output
lift_force = engine.get_lift_force()
print(f"Engine Lift Force: {lift_force} N")

# 4. Compute orbital velocity at LEO altitude (400 km)
v_orbit = engine.calculate_orbital_velocity(altitude_km=400.0)
print(f"Orbital Velocity at 400 km: {v_orbit} m/s")
