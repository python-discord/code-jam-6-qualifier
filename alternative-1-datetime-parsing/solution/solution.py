import datetime
import re

from typing import Dict, Tuple, Optional


DATE_PATTERN = re.compile(
    r"(?P<year>\d\d\d\d)"     # A date should start with a four-digit year
    r"(?P<dateseparator>-?)"  # Optionally followed by a `-` separator
    r"(?P<month>\d\d)"        # Then we should get a two-digit month
    r"(?P=dateseparator)"     # If we previously had a `-` separator, we should have one again
    r"(?P<day>\d\d)"          # Finally, a two-digit day
)

TIME_PATTERN = re.compile(
    r"(?P<hour>\d\d)"                              # A time part always starts with a two-digit hour
    r"(?:(?P<timeseparator>:?)(?P<minute>\d\d))?"  # Optionally followed by a two-digit minute
    r"(?:(?P=timeseparator)(?P<second>\d\d))?"     # Optionally followed by a two-digit second
    r"(?:\.(?P<fraction>\d{1,6}))?"                # Optionally followed by 1-6 decimals
)

TIMEZONE_PATTERN = re.compile(
    # Either match a `Z` or an offset formatted as ±HH:MM, ±HHMM, or ±HH
    r"(?P<utc>Z)|(?:(?P<sign>[-\+])(?P<hours>\d\d)(:?:?(?P<minutes>\d\d))?)"
)

TIME_UNIT_CONVERSION = {
    "hour": (60, "minute"),
    "minute": (60, "second"),
    "second": (1_000_000, "microsecond")
}


class InvalidFormat(ValueError):
    """Raised when (a part of) the timestamp was provided in an invalid format."""


def apply_pattern(timestamp: str, pattern: str, error_message: str) -> Tuple[re.Match, str]:
    """
    Match a regex pattern and return a Match object and the unmatched remainder.

    If no match was found, this function will raise an InvalidFormat exception with the provided
    `error_message`.
    """
    match = pattern.match(timestamp)
    if not match:
        raise InvalidFormat(error_message)

    return match, timestamp[match.end():]


def extract_date(timestamp: str) -> Tuple[Dict[str, int], str]:
    """
    Extract the date from a timestamp and return it as a dictionary plus the remaining string.

    If `timestamp` does not start with a valid date part, then an InvalidFormat exception will be
    raised.
    """
    match, remainder = apply_pattern(
        timestamp,
        pattern=DATE_PATTERN,
        error_message="the date part of a timestamp should be formatted as YYYY-MM-DD",
    )

    # Store the digits we've observed for our date units as `int` objects
    date = {unit: int(match[unit]) for unit in ("year", "month", "day")}

    return date, remainder


def calculate_fractional_time(fraction: str, time_unit: str) -> Dict[str, int]:
    """
    Calculate fractional time given the relevant `time_unit` the fraction applies to.

    To avoid floating point inaccuracies, the function use fractions combined with `divmod` to
    calculate the values for the additional time units we need to add.
    """
    units = {}

    # A fraction of 0.1 is 1/10; 0.01 = 1/100; and so on.
    numerator = int(fraction)
    denominator = 10**len(fraction)

    # We do not convert to smaller time units than microsecond
    while time_unit != "microsecond":
        # Get the conversation rate of the current time unit into the next smaller time unit
        conversion, time_unit = TIME_UNIT_CONVERSION[time_unit]

        # Store the amount needed of this time unit in the dict and the remainder as `numerator`
        units[time_unit], numerator = divmod(numerator * conversion, denominator)

        # If we don't have anything left to convert, break
        if not numerator:
            break

    return units


def extract_time(timestamp: str) -> Tuple[Dict[str, int], str]:
    """
    Extract the time from a timestamp and return it as a dictionary plus the remaining string.

    This function expects a string of which the date part has already been extracted.

    If `timestamp` is an empty string, this function will return an empty dictionary to indicate
    that no time part was present. If `timestamp` is non-empty, the function will first validate the
    presence of the `T` separator and then it will attempt to extract the time. If errors were found
    during the extraction process, an InvalidFormat exception will be raised.
    """
    if not timestamp:
        # If `timestamp` is empty, then this timestamp did not contain a time part
        return {}, timestamp

    if timestamp[0] != "T":
        # We could have made the `T` part of the regex pattern for time, but we wanted to raise an
        # exception with a specific message in case the `T` was missing.
        raise InvalidFormat("the date and time part should be separated by a `T` character")

    match, remainder = apply_pattern(
        timestamp[1:],
        pattern=TIME_PATTERN,
        error_message="the time part should be formatted as HH[:MM[:SS[.f+]]]"
    )

    time = {}

    for unit in ("hour", "minute", "second"):
        # If we don't have a time unit this small, break
        if not (amount := match[unit]):
            break

        # Store the amount of this time unit as an int
        time[unit] = int(match[unit])

        # This is currently the smallest time unit we've seen. This is important to keep track of in
        # order to know  which time unit a potential fraction applies to. If your solution only
        # deals with fractional seconds, you obviously know what the smallest time unit is and you
        # don't need something like this.
        smallest_unit = unit

    if (fraction := match["fraction"]):
        units = calculate_fractional_time(fraction, time_unit=smallest_unit)
        time.update(units)

    return time, remainder


def extract_timezone(timestamp: str) -> Optional[datetime.timezone]:
    """
    Extract the timezone from the remaining `timestamp`.

    This function extracts the timezone from the remaining `timestamp` after the date and time parts
    have been extracted. If no timestamp remains, then we assume that the timestamp did not contain
    a timezone deignation.

    If the timezone designator is `Z`, we return `datetime.timezone.utc`, otherwise we return a
    `datetime.timezone` with an offset created with a `datetime.timedelta` equal to the provided
    units. This function raises an `InvalidFormat` exception when either the timezone designator was
    not recognized or if additional characters were detected after the timezone designation.
    """
    if not timestamp:
        # If `timestamp` is empty, we don't have a timezone part in this timestamp
        return None

    match, remainder = apply_pattern(
        timestamp,
        pattern=TIMEZONE_PATTERN,
        error_message="invalid timezone designator detected"
    )

    # We should no longer have a remainder, since the timezone should be the last part
    if remainder:
        raise InvalidFormat("a valid timestamp was followed by invalid characters")

    # If we matched a `Z`, return `timezone.utc`
    if match["utc"]:
        return datetime.timezone.utc

    # Get the sign of the specified offset
    sign = match["sign"]

    # Create `int` objects from each non-zero timedelta unit with the correct sign
    units = {unit: int(sign + amount) for unit in ("hours", "minutes") if (amount := match[unit])}

    return datetime.timezone(datetime.timedelta(**units))


def parse_iso8601(timestamp: str) -> datetime.datetime:
    """
    Parse an ISO-8601 formatted time stamp.

    This function parses a subset of formats specified by the `ISO 8601` standard. The formats it
    parses start with a date, optionally followed by a time. The time part of the `timestamp` may
    include timezone information specified in terms of offset from UTC. Dates and times may be
    provided in a truncated format (without the `-` and `:` unit separators). If both a date and
    time part are present, they must be separated by a `T` character.

    Date format:
    - yyyy-mm-dd

    Time formats:
    - HH
    - HH:MM
    - HH:MM:SS

      The smallest unit in each time format may have a decimal fraction of up to six digits.

    Timezone formats:
    - Z
    - ±HH
    - ±HH:SS
    """
    date, remainder = extract_date(timestamp)
    time, remainder = extract_time(remainder)
    timezone = extract_timezone(remainder)

    return datetime.datetime(**date, **time, tzinfo=timezone)
