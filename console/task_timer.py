#!/usr/bin/env python3

import argparse
import subprocess
import sys
import time
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(
        description="Wait until a target time today, then run a script once."
    )
    parser.add_argument("script_path", help="Path to the script to run")
    parser.add_argument("hour", type=int, help="Target hour (0-23)")
    parser.add_argument("minute", type=int, help="Target minute (0-59)")
    return parser.parse_args()


def main():
    args = parse_args()

    if not (0 <= args.hour <= 23):
        print(f"Error: hour must be 0-23, got {args.hour}", file=sys.stderr)
        sys.exit(1)
    if not (0 <= args.minute <= 59):
        print(f"Error: minute must be 0-59, got {args.minute}", file=sys.stderr)
        sys.exit(1)

    now = datetime.now()
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Script started", flush=True)

    run_time = now.replace(
        hour=args.hour,
        minute=args.minute,
        second=0,
        microsecond=0,
    )

    if now >= run_time:
        print(
            f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Today {args.hour:02d}:{args.minute:02d} has already passed. Exiting.",
            flush=True,
        )
        return

    wait_seconds = (run_time - now).total_seconds()

    print(
        f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] "
        f"Will run at {run_time.strftime('%Y-%m-%d %H:%M:%S')}",
        flush=True,
    )

    time.sleep(wait_seconds)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running script", flush=True)

    try:
        subprocess.run(["/bin/bash", args.script_path], check=True)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Finished successfully", flush=True)
    except subprocess.CalledProcessError as e:
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Failed with exit code {e.returncode}",
            flush=True,
        )


if __name__ == "__main__":
    main()
