import datetime

from qualifier import parse_iso8601


def raises(timestamp):
    try:
        parse_iso8601(timestamp)
    except Exception as e:
        return isinstance(e, ValueError)


parses_yyyy_mm_dd = (
    parse_iso8601("2019-12-24") == datetime.datetime(2019, 12, 24),
    "Must parse YYYY-MM-DD.",
)

raises_on_invalid_year = raises("123-12-24"), "Must not accept invalid years."
raises_on_invalid_month = raises("2019-1-24"), "Must not accept invalid months."
raises_on_invalid_day = raises("2019-12-1"), "Must not accept invalid days."

parses_time_hhmmss = (
    parse_iso8601("2019-12-24T12:20:19") == datetime.datetime(2019, 12, 24, 12, 20, 19),
    "Must parse hh:mm:ss.",
)
parses_time_hhmm = (
    parse_iso8601("2019-12-24T12:20") == datetime.datetime(2019, 12, 24, 12, 20),
    "Must parse hh:mm.",
)
parses_time_hh = (
    parse_iso8601("2019-12-24T12") == datetime.datetime(2019, 12, 24, 12),
    "Must parse hh.",
)

raises_on_invalid_hh = (
    raises(parse_iso8601("2019-12-24T2:20:19")),
    "Must not accept invalid hours.",
)
raises_on_invalid_mm = (
    raises(parse_iso8601("2019-12-24T12:5:10")),
    "Must not accept invalid minutes.",
)
raises_on_invalid_ss = (
    raises(parse_iso8601("2019-12-24T12:50:123")),
    "Must not accept invalid seconds.",
)


needed_for_basic_requirements = (
    parses_yyyy_mm_dd,
    raises_on_invalid_year,
    raises_on_invalid_month,
    raises_on_invalid_day,
    parses_time_hhmmss,
    parses_time_hhmm,
    parses_time_hh,
    raises_on_invalid_hh,
    raises_on_invalid_mm,
    raises_on_invalid_ss,
)


if all(passed for passed, _ in needed_for_basic_requirements):
    print("You have passed all the basic requirements")
else:
    print("Your parser did not meed the following requirements:")
    for _, error in needed_for_basic_requirements:
        print("*", error)
