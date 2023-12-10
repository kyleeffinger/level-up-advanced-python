# Source of data: https://www.arrs.run/
# This dataset has race times for women 10k runners from the Association of Road Racing Statisticians

import re
import datetime


def get_data() -> str:
    """Return content from the 10k_racetimes.txt file"""
    with open("challenge/10k_racetimes.txt", "rt") as file:
        content: str = file.read()
    return content


def get_rhines_times() -> list[str]:
    """Return a list of Jennifer Rhines' race times"""
    # Capture time portion only if Jennifer Rhines is next to the time stamp
    pattern: str = "(\\d+:\\d+(?:\\.\\d+)?)\\s+Jennifer\\sRhines"
    races: str = get_data()
    rhimes_times: list[str] = re.findall(pattern, races)
    return rhimes_times


def get_average():
    """Return Jennifer Rhines' average race time in the format:
    mm:ss:M where :
    m corresponds to a minutes digit
    s corresponds to a seconds digit
    M corresponds to a milliseconds digit (no rounding, just the single digit)"""
    racetimes: list[str] = get_rhines_times()
    total_time: datetime.timedelta = datetime.timedelta()  # Initializes to 0:00:00

    # Extract minutes, seconds and [optional] milliseconds
    minutes: int
    seconds: int
    milliseconds: int

    # Iterate over found race times
    for time in racetimes:
        # Split by either ":" or "."
        try:
            minutes, seconds, milliseconds = re.split(r"[:.]", time)
        # Catch cases where milliseconds are missing in input data
        except ValueError:
            minutes, seconds = re.split(r"[:]", time)
            milliseconds = 0

        # Add to total as timedelta
        total_time += datetime.timedelta(
            minutes=int(minutes),
            seconds=int(seconds),
            milliseconds=int(milliseconds),
        )

    # Format timedelta to remove hours (2:) and trim decimals (:-5)
    return f"{total_time / len(racetimes)}"[2:-5]


if __name__ == "__main__":
    print(get_average())
