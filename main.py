#!/usr/bin/env python3
"""
main.py
-------
Command-line interface for the ISA & True Airspeed Calculator.

All modules (constants.py, isa_engine.py, pitot_solver.py, etc.) must sit
in the SAME folder as this file. Run it from inside that folder:

    cd isa_tas_calculator
    python main.py atmosphere --altitude 5000

Usage examples:
    python main.py atmosphere --altitude 5000
    python main.py profile --start 0 --end 20000 --step 1000
    python main.py tas --ias 250 --altitude 10000 --model compressible
    python main.py plot --start 0 --end 30000 --step 500
    python main.py plot-tas --ias 250 --end 15000
"""

import argparse
import os
import sys

from cli_reporter import (
    print_airspeed_result, print_atmosphere_table, print_single_atmosphere,
)
from isa_engine import get_atmosphere, get_atmosphere_profile
from pitot_solver import tas_compressible, tas_incompressible
from validators import InputValidationError

OUTPUT_DIR = "output"


def cmd_atmosphere(args):
    state = get_atmosphere(args.altitude)
    print_single_atmosphere(state)


def cmd_profile(args):
    states = get_atmosphere_profile(args.start, args.end, args.step)
    print_atmosphere_table(states)


def cmd_tas(args):
    if args.model == "incompressible":
        result = tas_incompressible(args.ias, args.altitude)
    else:
        result = tas_compressible(args.ias, args.altitude)
    print_airspeed_result(result)


def cmd_plot(args):
    from visualizer import plot_profile
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = plot_profile(args.start, args.end, args.step,
                         save_path=os.path.join(OUTPUT_DIR, "isa_profile.png"))
    print(f"Saved atmosphere profile plot to: {path}")


def cmd_plot_tas(args):
    from visualizer import plot_tas_vs_altitude
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = plot_tas_vs_altitude(args.ias, args.start, args.end, args.step,
                                 save_path=os.path.join(OUTPUT_DIR, "tas_profile.png"))
    print(f"Saved TAS-vs-altitude plot to: {path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="isa-tas-calculator",
        description="International Standard Atmosphere (ISA) & True Airspeed Calculator",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_atm = sub.add_parser("atmosphere", help="Compute ISA conditions at one altitude")
    p_atm.add_argument("--altitude", type=float, required=True, help="Geometric altitude in metres")
    p_atm.set_defaults(func=cmd_atmosphere)

    p_prof = sub.add_parser("profile", help="Print an ISA table over an altitude range")
    p_prof.add_argument("--start", type=float, default=0)
    p_prof.add_argument("--end", type=float, default=20000)
    p_prof.add_argument("--step", type=float, default=1000)
    p_prof.set_defaults(func=cmd_profile)

    p_tas = sub.add_parser("tas", help="Convert IAS/CAS to True Airspeed")
    p_tas.add_argument("--ias", type=float, required=True, help="Indicated/calibrated airspeed in knots")
    p_tas.add_argument("--altitude", type=float, required=True, help="Altitude in metres")
    p_tas.add_argument("--model", choices=["incompressible", "compressible"], default="compressible")
    p_tas.set_defaults(func=cmd_tas)

    p_plot = sub.add_parser("plot", help="Save a PNG plot of T/P/rho vs altitude")
    p_plot.add_argument("--start", type=float, default=0)
    p_plot.add_argument("--end", type=float, default=47000)
    p_plot.add_argument("--step", type=float, default=500)
    p_plot.set_defaults(func=cmd_plot)

    p_plot_tas = sub.add_parser("plot-tas", help="Save a PNG plot of TAS vs altitude for constant IAS")
    p_plot_tas.add_argument("--ias", type=float, required=True)
    p_plot_tas.add_argument("--start", type=float, default=0)
    p_plot_tas.add_argument("--end", type=float, default=15000)
    p_plot_tas.add_argument("--step", type=float, default=500)
    p_plot_tas.set_defaults(func=cmd_plot_tas)

    return parser


def interactive_menu():
    """
    Shown when the script is run with NO command-line arguments at all
    (e.g. clicking the VS Code "Run" button instead of using a terminal
    with flags). Avoids the argparse SystemExit crash and lets the user
    pick an action instead.
    """
    print("ISA & True Airspeed Calculator")
    print("No command-line arguments were given, so here is a simple menu.")
    print("(Tip: run from a terminal instead for full options, e.g.")
    print(" python main.py atmosphere --altitude 8000)")
    print()
    print("1) Atmosphere at an altitude")
    print("2) Atmosphere table over a range")
    print("3) Convert IAS/CAS to True Airspeed")
    print("4) Save an atmosphere profile plot (needs matplotlib)")
    print("5) Quit")
    choice = input("Choose an option [1-5]: ").strip()

    if choice == "1":
        alt = float(input("Altitude in metres: "))
        print_single_atmosphere(get_atmosphere(alt))
    elif choice == "2":
        start = float(input("Start altitude (m) [0]: ") or 0)
        end = float(input("End altitude (m) [20000]: ") or 20000)
        step = float(input("Step (m) [1000]: ") or 1000)
        print_atmosphere_table(get_atmosphere_profile(start, end, step))
    elif choice == "3":
        ias = float(input("IAS/CAS in knots: "))
        alt = float(input("Altitude in metres: "))
        print_airspeed_result(tas_compressible(ias, alt))
    elif choice == "4":
        from visualizer import plot_profile
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        path = plot_profile(save_path=os.path.join(OUTPUT_DIR, "isa_profile.png"))
        print(f"Saved plot to: {path}")
    else:
        print("Goodbye.")


def main():
    # If launched with no arguments (e.g. the VS Code Run button), fall
    # back to an interactive menu instead of letting argparse raise
    # SystemExit for a missing required subcommand.
    if len(sys.argv) == 1:
        try:
            interactive_menu()
        except InputValidationError as exc:
            print(f"Input error: {exc}", file=sys.stderr)
        return

    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except InputValidationError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
