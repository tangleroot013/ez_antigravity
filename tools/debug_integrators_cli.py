#!/usr/bin/env python3
import argparse
from ez_antigravity.integrators import FastEuler, PreciseRK4
from ez_antigravity.grav_engine import GravEngine
from ez_antigravity.constants import G_CONST, EARTH_MASS


def energy(r, v):
    gm = G_CONST * EARTH_MASS
    return 0.5 * v * v - gm / r


def run(steps, dt, r_init, v_init, verbose_every):
    euler = GravEngine(integrator=FastEuler())
    rk4 = GravEngine(integrator=PreciseRK4())

    pe = pr = r_init
    ve = vr = v_init
    e0 = energy(r_init, v_init)

    print(f"initial: r={r_init:.6f} v={v_init:.6f} e0={e0:.12e}")
    for i in range(1, steps + 1):
        pe, ve = euler.update(pe, ve, dt)
        pr, vr = rk4.update(pr, vr, dt)

        if verbose_every and i % verbose_every == 0:
            ee = energy(pe, ve)
            er = energy(pr, vr)
            print(
                f"step {i:5d} | "
                f"euler r={pe:.6f} v={ve:.6f} drift={(ee-e0)/abs(e0):+.6e} | "
                f"rk4 r={pr:.6f} v={vr:.6f} drift={(er-e0)/abs(e0):+.6e}"
            )

    ee = energy(pe, ve)
    er = energy(pr, vr)
    print("\nfinal:")
    print(f"euler r={pe:.6f} v={ve:.6f} drift={(ee-e0)/abs(e0):+.12e}")
    print(f"rk4   r={pr:.6f} v={vr:.6f} drift={(er-e0)/abs(e0):+.12e}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=1000)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--r-init", type=float, default=6.771e6)
    ap.add_argument("--v-init", type=float, default=0.0)
    ap.add_argument("--verbose-every", type=int, default=100)
    args = ap.parse_args()
    run(args.steps, args.dt, args.r_init, args.v_init, args.verbose_every)
