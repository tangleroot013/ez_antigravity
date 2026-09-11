#!/usr/bin/env python3
"""
ez_grav async engine scaffold — Enhancement #1: Async Event Loop.

Demonstrates converting the synchronous `while input()` loop into
an asyncio-based architecture with:
  - non-blocking command input
  - background telemetry tick at ~30 FPS
  - live coil cooldown + altitude decay

This is a runnable reference, not a patch onto your existing
TerminalUI class — wire your real GravEngine physics calls in
where marked below.
"""

import asyncio
import time
from dataclasses import dataclass


@dataclass
class GravState:
    mass: float = 1000.0              # kg, payload mass tensor
    altitude: float = 0.0             # meters
    t_coil: float = 20.0              # deg C
    t_ambient: float = 20.0           # deg C
    cooling_rate: float = 0.5         # deg C / tick toward ambient
    altitude_decay_rate: float = 2.0  # m / tick when unpowered
    running: bool = True

    def tick(self, dt: float) -> None:
        """One physics step. Called every frame by the telemetry loop."""
        # Newton's law of cooling: T -> T_ambient exponentially
        self.t_coil += (self.t_ambient - self.t_coil) * self.cooling_rate * dt

        # Passive altitude decay when not actively hovering
        if self.altitude > 0:
            self.altitude = max(0.0, self.altitude - self.altitude_decay_rate * dt)

        # Overheat safety (Enhancement #3, wired in early since it's cheap)
        if self.t_coil >= 100.0:
            print("\n[!] COIL OVERHEAT — forcing safe descent")
            self.altitude = 0.0


async def telemetry_loop(state: GravState, fps: int = 30) -> None:
    """Background task: recalculates physics at a fixed tick rate."""
    frame_time = 1.0 / fps
    last = time.monotonic()
    while state.running:
        now = time.monotonic()
        dt = now - last
        last = now
        state.tick(dt)
        await asyncio.sleep(frame_time)


async def command_loop(state: GravState) -> None:
    """Non-blocking input loop. Runs input() in a thread so it never
    blocks the telemetry task."""
    loop = asyncio.get_running_loop()
    print("ez_grav async shell — commands: /fly <alt>, /status, /quit")
    while state.running:
        cmd = await loop.run_in_executor(None, input, "ez_grav> ")
        cmd = cmd.strip()

        if cmd == "/quit":
            state.running = False

        elif cmd == "/status":
            print(f"  alt={state.altitude:.1f}m  "
                  f"t_coil={state.t_coil:.1f}C  "
                  f"mass={state.mass:.1f}kg")

        elif cmd.startswith("/fly"):
            try:
                target = float(cmd.split()[1])
                state.altitude = target
                # exotic altitudes heat the coil — cheap stand-in for
                # Enhancement #3's real thermodynamic model
                if target > 5000:
                    state.t_coil += 15.0
                print(f"  -> altitude set to {target}m")
            except (IndexError, ValueError):
                print("  usage: /fly <meters>")

        elif cmd:
            print(f"  unknown command: {cmd}")


async def main() -> None:
    state = GravState()
    await asyncio.gather(
        telemetry_loop(state),
        command_loop(state),
    )


if __name__ == "__main__":
    asyncio.run(main())
