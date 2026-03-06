#!/usr/bin/env python3
"""Simple alarm clock that plays a sound at the specified time."""

import time
import sys
import threading
from datetime import datetime


def beep():
    """Print a bell character to trigger a terminal beep."""
    print("\a", end="", flush=True)


def play_alarm(duration=5):
    """Play repeated beeps for the given duration in seconds."""
    end_time = time.time() + duration
    while time.time() < end_time:
        beep()
        time.sleep(0.5)
    print("\nAlarm finished!")


def wait_until(target_time):
    """Wait until the target time, showing a countdown."""
    while True:
        now = datetime.now()
        remaining = (target_time - now).total_seconds()
        if remaining <= 0:
            break
        mins, secs = divmod(int(remaining), 60)
        hrs, mins = divmod(mins, 60)
        print(f"\rTime until alarm: {hrs:02d}:{mins:02d}:{secs:02d}", end="", flush=True)
        time.sleep(1)


def parse_time(time_str):
    """Parse a time string in HH:MM or HH:MM:SS format."""
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            parsed = datetime.strptime(time_str, fmt)
            now = datetime.now()
            target = now.replace(
                hour=parsed.hour,
                minute=parsed.minute,
                second=parsed.second if fmt == "%H:%M:%S" else 0,
                microsecond=0,
            )
            if target <= now:
                print("That time has already passed today. Setting alarm for tomorrow.")
                target = target.replace(day=target.day + 1)
            return target
        except ValueError:
            continue
    return None


def set_timer(seconds):
    """Set a countdown timer for the given number of seconds."""
    target = datetime.now().replace(microsecond=0)
    target = datetime.fromtimestamp(target.timestamp() + seconds)
    return target


def main():
    print("=== Simple Alarm Clock ===\n")
    print("Options:")
    print("  1. Set alarm for a specific time (HH:MM or HH:MM:SS)")
    print("  2. Set a countdown timer (in seconds)")
    print()

    choice = input("Choose option (1 or 2): ").strip()

    if choice == "1":
        time_str = input("Enter alarm time (HH:MM or HH:MM:SS, 24h format): ").strip()
        target = parse_time(time_str)
        if target is None:
            print("Invalid time format. Use HH:MM or HH:MM:SS.")
            sys.exit(1)
        print(f"Alarm set for {target.strftime('%H:%M:%S')}")
    elif choice == "2":
        try:
            seconds = int(input("Enter countdown in seconds: ").strip())
            if seconds <= 0:
                print("Please enter a positive number.")
                sys.exit(1)
            target = set_timer(seconds)
            print(f"Timer set for {seconds} seconds")
        except ValueError:
            print("Invalid number.")
            sys.exit(1)
    else:
        print("Invalid option.")
        sys.exit(1)

    print("Press Ctrl+C to cancel.\n")

    try:
        wait_until(target)
        print("\n\n*** ALARM! WAKE UP! ***\n")
        play_alarm(duration=5)
    except KeyboardInterrupt:
        print("\nAlarm cancelled.")
        sys.exit(0)


if __name__ == "__main__":
    main()
