import datetime
import io
import sys
import timeit
import typing
import unittest

from qualifier import parse_iso8601

import test_qualifier

from testsuite.result import QualifierTestResult, StreamWrapper


class QualifierTestRunner:
    """Test runner for our code jam qualifier test suite."""

    resultclass = QualifierTestResult

    def __init__(
        self,
        stream: typing.Optional[io.TextIOBase] = None,
        verbosity: int = 1,
        resultclass: typing.Optional[typing.Type[unittest.TestResult]] = None,
        console_width: int = 100,
        title: str = "Python Discord Winter Code Jam: Qualifier Test Suite",
        **kwargs,
    ) -> None:
        if stream is None:
            # By default, write to stderr. However, since stream accepts any
            # stream that implements the TextIOBase protocol, we could use this
            # parameter to write to file as well.
            stream = sys.stderr
        self.stream = StreamWrapper(stream, max_width=console_width, verbosity=verbosity)

        self.verbosity = verbosity
        self.title = title

        if resultclass is not None:
            self.resultclass = resultclass

    def instantiate_resultclass(self) -> unittest.TestResult:
        """Create an instance of the result class for a test run."""
        return self.resultclass(self.stream, self.verbosity)

    def write_header(self) -> None:
        """Write a header for this test run."""
        self.stream.write_separator("=")
        self.stream.write(f"{self.title}\n")
        self.stream.write_separator("=")
        self.stream.writeln(
            f"Date: {datetime.datetime.utcnow().strftime(r'%Y-%m-%d %H:%M:%S')} UTC"
        )
        self.stream.writeln()

    def write_footer(self, result: unittest.TestResult, duration: float) -> None:
        """Write a footer for this test run."""
        self.stream.write_separator("=")
        self.stream.writeln(f"Test suite running time: {duration:.3f}s")
        self.stream.writeln()

        self.stream.write_section_header("Function Benchmark")
        if hasattr(result, "results") and all(
            test["passed"] for test in result.results["Basic Requirements"].values()
        ):
            try:
                self.run_benchmark()
            except Exception as e:
                self.stream.writeln(f"Something went wrong while running the benchmark: {e!r}")
                self.stream.writeln("Did your `parse_iso8601` function fail on one of the strings?")
        else:
            self.stream.writeln(
                "Benchmarking will become available once you pass all tests in Basic Requirements."
            )

    def run(self, test: unittest.TestSuite) -> None:
        """Run a test suite containing `unittest.TestCase` tests."""
        result = self.instantiate_resultclass()
        self.write_header()

        # Record the start time
        start = timeit.default_timer()

        # Pass the TestResult instance to the test suite to run the tests
        test(result)

        # Record the end time
        duration = timeit.default_timer() - start

        self.write_footer(result, duration)
        return result.results

    def run_benchmark(self) -> None:
        """Run a benchmark on the `parse_iso8601` function."""
        with open("testsuite/benchmark_strings.txt", "r", encoding="utf-8") as datestrings:
            datestrings = [datestring.rstrip("\n") for datestring in datestrings]

        duration = 0.0
        for run in range(1, 101):
            start = timeit.default_timer()
            for datestring in datestrings:
                parse_iso8601(datestring)
            duration += timeit.default_timer() - start
            if duration > 5:
                break

        cases_tested = run * len(datestrings)
        self.stream.write(f"Number of strings:  {cases_tested}\n")
        self.stream.write(f"Total time:         {duration:.10f}s\n")
        self.stream.write(f"Average time:       {duration/cases_tested:.10f}s\n")


def run_testsuite() -> None:
    """Run an ascii-based test suite."""
    test_loader = unittest.TestLoader()
    test_loader.sortTestMethodsUsing = None
    test_suite = test_loader.loadTestsFromModule(test_qualifier)
    runner = QualifierTestRunner(verbosity=2)
    runner.run(test_suite)
