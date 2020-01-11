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
        """Accepts valid date strings."""
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
            # Additional test cases that were not published with the qualifier
            TestCase(
                input="1791-12-26",
                expected_output=datetime.datetime(year=1791, month=12, day=26)
            ),
            TestCase(
                input="1701-04-15",
                expected_output=datetime.datetime(year=1701, month=4, day=15)
            ),
            TestCase(
                input="1994-09-19",
                expected_output=datetime.datetime(year=1994, month=9, day=19)
            ),
        )

        self._run_test_cases(test_cases)

    def test_002_accepts_valid_datetime_strings(self) -> None:
        """Accepts valid datetime strings."""
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
            # Additional test cases that were not published with the qualifier
            TestCase(
                input="1991-09-17T08:57:08",
                expected_output=datetime.datetime(
                    year=1991, month=9, day=17, hour=8, minute=57, second=8
                )
            ),
            TestCase(
                input="1969-07-20T20:17",
                expected_output=datetime.datetime(
                    year=1969, month=7, day=20, hour=20, minute=17
                )
            ),
        )

        self._run_test_cases(test_cases)

    def test_003_rejects_invalid_datetime_stings(self) -> None:
        """Raises ValueError for invalid strings."""
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
            "1677-09-03T12.31.05",  # `.` is not a valid separator for the <time> part
            "1677-09-03T12-31-05",  # `-` is not a valid separator for the <time> part
            "1677-09-03T12:3105",  # Combining the partial and truncated format is not allow
            "1677-09-03T1231:05",  # Combining the partial and truncated format is not allow

            # Additional test cases that were not published with the qualifier
            " ",
            "All the ducks are swimming in the water",
            "1999-21-09",  # Invalid value for the month
            "2000-12-64",  # Invalid value for the day
            "1887&12&01",  # Invalid date separator
            "1994-04-05K15:15:15",  # Invalid part separator
            "2020-01-01T100:100:100",  # Invalid time
        )

        for invalid_datestring in test_cases:
            with self.subTest(input=invalid_datestring):
                with self.assertRaises(ValueError):
                    parse_iso8601(invalid_datestring)


class Part002_AdvancedRequirements(unittest.TestCase):
    """Advanced Requirements."""

    def _run_test_cases(self, test_cases: typing.Tuple[TestCase]) -> None:
        for test_case in test_cases:
            with self.subTest(**test_case._asdict()):
                actual_output = parse_iso8601(test_case.input)

                self.assertIsInstance(actual_output, datetime.datetime)
                self.assertEqual(test_case.expected_output, actual_output)

                # The strings for the basic requirements do not contain timezone information
                self.assertIsNone(actual_output.tzinfo)

    def test_001_accepts_truncated_date_strings(self) -> None:
        """Accepts truncated date strings."""
        test_cases = (
            TestCase(
                input="15830101",
                expected_output=datetime.datetime(year=1583, month=1, day=1)
            ),
            TestCase(
                input="99991231",
                expected_output=datetime.datetime(year=9999, month=12, day=31)
            ),
            TestCase(
                input="20170108",
                expected_output=datetime.datetime(year=2017, month=1, day=8)
            ),
            TestCase(
                input="20081203",
                expected_output=datetime.datetime(year=2008, month=12, day=3)
            ),
            TestCase(
                input="19550608",
                expected_output=datetime.datetime(year=1955, month=6, day=8)
            ),
            TestCase(
                input="18151210",
                expected_output=datetime.datetime(year=1815, month=12, day=10)
            ),
            TestCase(
                input="19060428",
                expected_output=datetime.datetime(year=1906, month=4, day=28)
            ),
        )

        self._run_test_cases(test_cases)

    def test_002_accepts_truncated_datetime_strings(self) -> None:
        """Accepts truncated datetime strings."""
        test_cases = (
            # HHMMSS
            TestCase(
                input="19060615T120931",
                expected_output=datetime.datetime(
                    year=1906, month=6, day=15, hour=12, minute=9, second=31
                )
            ),
            TestCase(
                input="20001016T000001",
                expected_output=datetime.datetime(
                    year=2000, month=10, day=16, hour=0, minute=0, second=1
                )
            ),
            TestCase(
                input="19741219T1313",
                expected_output=datetime.datetime(
                    year=1974, month=12, day=19, hour=13, minute=13
                )
            ),
            TestCase(
                input="19711103T2022",
                expected_output=datetime.datetime(year=1971, month=11, day=3, hour=20, minute=22)
            ),
            TestCase(
                input="19810727T01",
                expected_output=datetime.datetime(year=1981, month=7, day=27, hour=1)
            ),
            TestCase(
                input="19110925T19",
                expected_output=datetime.datetime(year=1911, month=9, day=25, hour=19)
            ),
        )

        self._run_test_cases(test_cases)

    def test_003_accepts_untruncated_fractional_seconds(self) -> None:
        """Accepts fractional seconds (untruncated format)."""
        test_cases = (
            # Untruncated
            TestCase(
                input="1862-01-23T11:12:33.1",
                expected_output=datetime.datetime(
                    year=1862, month=1, day=23, hour=11, minute=12, second=33, microsecond=100_000
                )
            ),
            TestCase(
                input="1815-11-02T09:10:21.21",
                expected_output=datetime.datetime(
                    year=1815, month=11, day=2, hour=9, minute=10, second=21, microsecond=210_000
                )
            ),
            TestCase(
                input="1905-08-16T16:15:14.321",
                expected_output=datetime.datetime(
                    year=1905, month=8, day=16, hour=16, minute=15, second=14, microsecond=321_000
                )
            ),
            TestCase(
                input="1930-05-11T19:23:49.4321",
                expected_output=datetime.datetime(
                    year=1930, month=5, day=11, hour=19, minute=23, second=49, microsecond=432_100
                )
            ),
            TestCase(
                input="1942-01-01T23:59:59.54321",
                expected_output=datetime.datetime(
                    year=1942, month=1, day=1, hour=23, minute=59, second=59, microsecond=543_210
                )
            ),
            TestCase(
                input="1941-09-09T11:11:11.654321",
                expected_output=datetime.datetime(
                    year=1941, month=9, day=9, hour=11, minute=11, second=11, microsecond=654_321
                )
            ),
            TestCase(
                input="1941-09-09T11:11:11.000001",
                expected_output=datetime.datetime(
                    year=1941, month=9, day=9, hour=11, minute=11, second=11, microsecond=1
                )
            ),
        )

        self._run_test_cases(test_cases)

    def test_004_accepts_truncated_fractional_seconds(self) -> None:
        """Accepts fractional seconds (truncated format)."""
        test_cases = (
            # Truncated
            TestCase(
                input="18620123T111233.9",
                expected_output=datetime.datetime(
                    year=1862, month=1, day=23, hour=11, minute=12, second=33, microsecond=900_000
                )
            ),
            TestCase(
                input="18151102T091021.98",
                expected_output=datetime.datetime(
                    year=1815, month=11, day=2, hour=9, minute=10, second=21, microsecond=980_000
                )
            ),
            TestCase(
                input="19050816T161514.987",
                expected_output=datetime.datetime(
                    year=1905, month=8, day=16, hour=16, minute=15, second=14, microsecond=987_000
                )
            ),
            TestCase(
                input="19300511T192349.9876",
                expected_output=datetime.datetime(
                    year=1930, month=5, day=11, hour=19, minute=23, second=49, microsecond=987_600
                )
            ),
            TestCase(
                input="19420101T235959.98765",
                expected_output=datetime.datetime(
                    year=1942, month=1, day=1, hour=23, minute=59, second=59, microsecond=987_650
                )
            ),
            TestCase(
                input="19410909T111111.987654",
                expected_output=datetime.datetime(
                    year=1941, month=9, day=9, hour=11, minute=11, second=11, microsecond=987_654
                )
            ),
            TestCase(
                input="19410909T111111.000001",
                expected_output=datetime.datetime(
                    year=1941, month=9, day=9, hour=11, minute=11, second=11, microsecond=1
                )
            ),
        )

        self._run_test_cases(test_cases)

    def test_005_accepts_timezones(self) -> None:
        """Supports timezones."""
        test_cases = (
            # Truncated
            TestCase(
                input="1902-08-02T12:30:24Z",
                expected_output=datetime.datetime(
                    year=1902, month=8, day=2, hour=12, minute=30, second=24,
                    tzinfo=datetime.timezone.utc
                )
            ),
            TestCase(
                input="2022-12-12T11:10:09Z",
                expected_output=datetime.datetime(
                    year=2022, month=12, day=12, hour=11, minute=10, second=9,
                    tzinfo=datetime.timezone.utc
                )
            ),
            TestCase(
                input="1902-08-02T12:30:24+01",
                expected_output=datetime.datetime(
                    year=1902, month=8, day=2, hour=12, minute=30, second=24,
                    tzinfo=datetime.timezone(datetime.timedelta(hours=1))
                )
            ),
            TestCase(
                input="2022-12-12T11:10:09+12",
                expected_output=datetime.datetime(
                    year=2022, month=12, day=12, hour=11, minute=10, second=9,
                    tzinfo=datetime.timezone(datetime.timedelta(hours=12))
                )
            ),
            TestCase(
                input="1902-08-02T12:30:24-03",
                expected_output=datetime.datetime(
                    year=1902, month=8, day=2, hour=12, minute=30, second=24,
                    tzinfo=datetime.timezone(datetime.timedelta(hours=-3))
                )
            ),
            TestCase(
                input="2022-12-12T11:10:09-11",
                expected_output=datetime.datetime(
                    year=2022, month=12, day=12, hour=11, minute=10, second=9,
                    tzinfo=datetime.timezone(datetime.timedelta(hours=-11))
                )
            ),
            TestCase(
                input="1902-08-02T12:30:24+01:15",
                expected_output=datetime.datetime(
                    year=1902, month=8, day=2, hour=12, minute=30, second=24,
                    tzinfo=datetime.timezone(datetime.timedelta(hours=1, minutes=15))
                )
            ),
            TestCase(
                input="2022-12-12T11:10:09+12:59",
                expected_output=datetime.datetime(
                    year=2022, month=12, day=12, hour=11, minute=10, second=9,
                    tzinfo=datetime.timezone(datetime.timedelta(hours=12, minutes=59))
                )
            ),
            TestCase(
                input="1902-08-02T12:30:24-03:01",
                expected_output=datetime.datetime(
                    year=1902, month=8, day=2, hour=12, minute=30, second=24,
                    tzinfo=datetime.timezone(datetime.timedelta(hours=-3, minutes=-1))
                )
            ),
            TestCase(
                input="2022-12-12T11:10:09-11:31",
                expected_output=datetime.datetime(
                    year=2022, month=12, day=12, hour=11, minute=10, second=9,
                    tzinfo=datetime.timezone(datetime.timedelta(hours=-11, minutes=-31))
                )
            ),
            TestCase(
                input="19020802T123024+0226",
                expected_output=datetime.datetime(
                    year=1902, month=8, day=2, hour=12, minute=30, second=24,
                    tzinfo=datetime.timezone(datetime.timedelta(hours=2, minutes=26))
                )
            ),
            TestCase(
                input="20221212T111009+1101",
                expected_output=datetime.datetime(
                    year=2022, month=12, day=12, hour=11, minute=10, second=9,
                    tzinfo=datetime.timezone(datetime.timedelta(hours=11, minutes=1))
                )
            ),
            TestCase(
                input="19020802T123024-0509",
                expected_output=datetime.datetime(
                    year=1902, month=8, day=2, hour=12, minute=30, second=24,
                    tzinfo=datetime.timezone(datetime.timedelta(hours=-5, minutes=-9))
                )
            ),
            TestCase(
                input="20221212T111009-1059",
                expected_output=datetime.datetime(
                    year=2022, month=12, day=12, hour=11, minute=10, second=9,
                    tzinfo=datetime.timezone(datetime.timedelta(hours=-10, minutes=-59))
                )
            ),
        )

        for test_case in test_cases:
            with self.subTest(**test_case._asdict()):
                actual_output = parse_iso8601(test_case.input)

                self.assertEqual(test_case.expected_output.utcoffset(), actual_output.utcoffset())
                self.assertEqual(test_case.expected_output, actual_output)


class Part003_BonusTests(unittest.TestCase):
    """Bonus Tests."""

    def _run_test_cases(self, test_cases: typing.Tuple[TestCase]) -> None:
        for test_case in test_cases:
            with self.subTest(**test_case._asdict()):
                actual_output = parse_iso8601(test_case.input)

                self.assertIsInstance(actual_output, datetime.datetime)
                self.assertEqual(test_case.expected_output, actual_output)

    def test_001_accepts_fractional_minutes_and_hours(self) -> None:
        """Accepts fractional minutes/hours."""
        test_cases = (
            # Fractional hours
            TestCase(
                input="1999-09-09T12.5",
                expected_output=datetime.datetime(
                    year=1999, month=9, day=9, hour=12, minute=30
                )
            ),
            TestCase(
                input="1715-10-08T12.125",
                expected_output=datetime.datetime(
                    year=1715, month=10, day=8, hour=12, minute=7, second=30
                )
            ),
            TestCase(
                input="1905-08-16T16.03125",
                expected_output=datetime.datetime(
                    year=1905, month=8, day=16, hour=16, minute=1, second=52, microsecond=500_000
                )
            ),
            TestCase(
                input="1905-08-16T16.015625",
                expected_output=datetime.datetime(
                    year=1905, month=8, day=16, hour=16, minute=0, second=56, microsecond=250_000
                )
            ),
            TestCase(
                input="1905-08-16T16.000001",
                expected_output=datetime.datetime(
                    year=1905, month=8, day=16, hour=16, minute=0, second=0, microsecond=3_600
                )
            ),
            # Fractional minutes
            TestCase(
                input="1999-09-09T00:01.5",
                expected_output=datetime.datetime(
                    year=1999, month=9, day=9, hour=0, minute=1, second=30
                )
            ),
            TestCase(
                input="1715-10-08T00:02.125",
                expected_output=datetime.datetime(
                    year=1715, month=10, day=8, hour=0, minute=2, second=7, microsecond=500_000
                )
            ),
            TestCase(
                input="1905-08-16T19:15.078125",
                expected_output=datetime.datetime(
                    year=1905, month=8, day=16, hour=19, minute=15, second=4, microsecond=687_500
                )
            ),
            TestCase(
                input="1905-08-16T19:15.000001",
                expected_output=datetime.datetime(
                    year=1905, month=8, day=16, hour=19, minute=15, second=0, microsecond=60
                )
            ),
        )

        self._run_test_cases(test_cases)
