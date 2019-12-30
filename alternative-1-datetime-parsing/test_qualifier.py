import collections
import datetime
import typing
import unittest

from qualifier import parse_iso8601

TestCase = collections.namedtuple("TestCase", "input expected_output")


class Part001_BasicRequirements(unittest.TestCase):
    """Basic Requirements."""

    def _run_test_cases(self, test_cases: typing.Tuple[TestCase]) -> None:
        for test_case in test_cases:
            with self.subTest(**test_case._asdict()):
                actual_output = parse_iso8601(test_case.input)

                self.assertIsInstance(actual_output, datetime.datetime)
                self.assertEqual(test_case.expected_output, actual_output)

                # The strings for the basic requirements do not contain timezone information
                self.assertIsNone(actual_output.tzinfo)

    def test_001_accepts_valid_date_only_strings(self) -> None:
        """Accepts valid date strings: `yyyy-mm-dd`."""
        test_cases = (
            TestCase(
                input="1583-01-01",  # The standard only requires year 1583+ by default
                expected_output=datetime.datetime(year=1583, month=1, day=1)
            ),
            TestCase(
                input="9999-12-31",
                expected_output=datetime.datetime(year=9999, month=12, day=31)
            ),
            TestCase(
                input="2017-01-08",
                expected_output=datetime.datetime(year=2017, month=1, day=8)
            ),

            TestCase(
                input="2008-12-03",
                expected_output=datetime.datetime(year=2008, month=12, day=3)
            ),
        )

        self._run_test_cases(test_cases)

    def test_002_accepts_valid_datetime_strings(self) -> None:
        """Accepts valid datetime strings: `yyyy-mm-ddT<time>`."""
        test_cases = (
            # <time> = HH:MM:SS
            TestCase(
                input="2019-12-18T21:10:48",
                expected_output=datetime.datetime(
                    year=2019, month=12, day=18, hour=21, minute=10, second=48
                )
            ),
            TestCase(
                input="1956-01-31T00:00:00",
                expected_output=datetime.datetime(
                    year=1956, month=1, day=31, hour=0, minute=0, second=0
                )
            ),
            TestCase(
                input="1994-01-26T23:59:59",  # The standard allows seconds=60; datetime does not
                expected_output=datetime.datetime(
                    year=1994, month=1, day=26, hour=23, minute=59, second=59
                )
            ),
            # <time> = HH:MM
            TestCase(
                input="1996-02-10T08:17",
                expected_output=datetime.datetime(
                    year=1996, month=2, day=10, hour=8, minute=17
                )
            ),
            TestCase(
                input="1910-06-22T11:11",
                expected_output=datetime.datetime(
                    year=1910, month=6, day=22, hour=11, minute=11
                )
            ),
            TestCase(
                input="1905-12-22T23:59",
                expected_output=datetime.datetime(
                    year=1905, month=12, day=22, hour=23, minute=59
                )
            ),
            # <time> = HH
            TestCase(
                input="1912-06-23T00",
                expected_output=datetime.datetime(
                    year=1912, month=6, day=23, hour=0
                )
            ),
            TestCase(
                input="1791-12-26T23",
                expected_output=datetime.datetime(
                    year=1791, month=12, day=26, hour=23
                )
            ),
            TestCase(
                input="1596-03-31T12",
                expected_output=datetime.datetime(
                    year=1596, month=3, day=31, hour=12
                )
            ),
        )

        self._run_test_cases(test_cases)

    def test_003_rejects_invalid_datetime_stings(self) -> None:
        """Parser raises ValueError for invalid datetime strings."""
        test_cases = (
            # Odd strings
            "",  # Empty strings are not valid dateetime strings
            "Python Discord",  # A non-empty string isn't necessarily better

            # Invalid date values in a valid format
            "1989-13-01",  # We don't have a 13th month
            "1990-01-32",  # January doesn't have 32 days

            # Valid date values in an invalid format
            "2345-2-10",  # MONTH should have two characters
            "1788-12-1",  # DAY should have two characters
            "2012/10/02",  # `/` is not a valid separator for dates
            "1999:10:02",  # `:` is not a valid separator for dates
            "2012 10 02",  # ` ` is not a valid separator
            "17-12-2019",  # DD-MM-YYYY is not an accepted format
            "2019-1012",  # Combining the normal and truncated format is not allowed
            "201910-12",  # Combining the normal and truncated format is not allowed

            # The ISO 8601 standard only allows a `T` as the separator
            "2019-10-01 12:23:34",  # According the standard, spaces are not valid separators
            "1965-02-01t19:09:13",  # A lowercase `t` is also not a valid separator
            "2019-03-25\t08:12:59",  # A tab characters is not a valid separator
            "2019-03-25abc08:12:59",  # `abc` is also not a valid separator
            "2019-03-25P08:12:59",  # An `P` isn't either

            # Incorrect values in the <time> part of the datetime string
            "2019-10-01T25",  # Invalid value (25) for hour
            "2019-10-01T31:10",  # Invalid value (31) for hour
            "2019-10-01T74:44:28",  # Invalid value (74) for hour
            "2019-10-01T12:61",  # Invalid value (61) for minutes
            "2019-10-01T07:88:12",  # Invalid value (88) for hour
            "2019-10-01T00:01:65",  # Invalid value (65) for seconds
            "2019-13-66T25:62:88",  # Invalid values for everything but the year

            # Incorrect form in the <time> part of the datetime string
            "1677-09-03T12.31.05"  # `.` is not a valid separator for the <time> part
            "1677-09-03T12-31-05"  # `-` is not a valid separator for the <time> part
            "1677-09-03T12:3105"  # Combining the partial and truncated format is not allow
            "1677-09-03T1231:05"  # Combining the partial and truncated format is not allow
        )

        for invalid_datestring in test_cases:
            with self.subTest(input=invalid_datestring):
                with self.assertRaises(ValueError):
                    parse_iso8601(invalid_datestring)


class Part002_AdvancedRequirements(unittest.TestCase):
    """Advanced Requirements."""
