import collections
import io
import math
import textwrap
import types
import typing
import unittest


TestOutcome = typing.Tuple[typing.Type[BaseException], BaseException, types.TracebackType]
TestClass = collections.namedtuple("TestClass", "type name")


class StreamWrapper:
    """Wrap an `io.TextIOBase` derived stream with utility methods."""

    def __init__(self, stream: io.TextIOBase, max_width: int = 100, verbosity: int = 0) -> None:
        self.stream = stream
        self.max_width = max_width
        self.verbosity = verbosity

    def __getattr__(self, attr: str) -> typing.Any:
        """Delegate attributes to the `io.TextIOBase` derived stream object."""
        return getattr(self.stream, attr)

    def fixed_width_text(self, text: str, width: int) -> str:
        """Create a string with a certain width by truncating and/or right-padding `text`."""
        return f"{text[:width]:<{width}}"

    def writeln(self, text: str = "") -> None:
        """Write a line to the stream."""
        if text:
            self.stream.write(text[:self.max_width])
        self.stream.write("\n")

    def write_separator(self, char: str = "-", length: typing.Optional[int] = None) -> None:
        """Write a separator line to the stream."""
        if not length:
            length = self.max_width
        multiplier = math.ceil(length / len(char))
        separator = char * multiplier
        self.writeln(separator[:self.max_width])

    def write_test_outcome(
        self,
        description: str,
        results: typing.Dict[str, int],
        subtest_outcomes: typing.List[TestOutcome],
    ) -> None:
        """Write a test description."""
        outcome, passed, failed, total = results.values()

        verdict = "[ PASS ]" if outcome else "[ FAIL ]"
        description = self.fixed_width_text(description, self.max_width - 8) + verdict

        self.writeln(description)

        if self.verbosity > 1 and subtest_outcomes:
            for subtest, outcome in subtest_outcomes:
                self.write_subtest_failure(subtest, outcome)
                self.writeln()
                self.write_separator("-")

            self.writeln()

    def write_subtest_failure(self, subtest: unittest.TestCase, outcome: TestOutcome) -> None:
        """Format subtest failure and write it to the stream."""
        self.writeln()
        self.write_separator("-")
        self.writeln("Failing test case:")

        failure_text = []
        kwargs = subtest.params

        if "input" in kwargs:
            description = self.fixed_width_text("Input:", 18)
            failure_text.append(f"{description}{kwargs['input']!r}")

        if "expected_output" in kwargs:
            description = self.fixed_width_text("Expected output:", 18)
            failure_text.append(f"{description}{kwargs['expected_output']!r}")

        _, exception, _ = outcome
        description = self.fixed_width_text("Test result:", 18)
        failure_text.append(f"{description}{exception!r}")
        self.stream.write(textwrap.indent("\n".join(failure_text), prefix="  "))

    def write_section_header(self, section_title: str) -> None:
        """Write a section header, optionally including a subtest result header."""
        title_width = self.max_width - 10
        section_title = self.fixed_width_text(section_title, title_width)

        self.write_separator("=")
        self.write(f"{section_title}\n")
        self.write_separator("=")


class QualifierTestResult(unittest.TestResult):
    """A custom test result class used for testing entries for our Code Jam qualifier."""

    def __init__(self, stream: StreamWrapper, verbosity: int = 0) -> None:
        super().__init__(stream.stream, verbosity)
        self.verbosity = verbosity
        self.stream = stream

        self.current_testclass = TestClass(None, None)
        self.results = {}

    def get_description(self, callable_object: typing.Callable) -> str:
        """Extract a description from the callable by looking at the docstring."""
        if callable_object.__doc__:
            description = callable_object.__doc__.splitlines()[0].rstrip(".!?")
        else:
            description = str(callable_object)
        return description

    def switch_testclass(self, test: unittest.TestCase) -> None:
        """Switch to the new test class and print a section header."""
        test_section = self.get_description(test)
        self.current_testclass = TestClass(type=type(test), name=test_section)

        self.stream.write_section_header(test_section)
        self.results[test_section] = {}

    def startTest(self, test: unittest.TestCase) -> None:
        """Prepare the test phase of an individual test method."""
        super().startTest(test)

        if type(test) != self.current_testclass.type:
            self.switch_testclass(test)

        test_name = test.shortDescription().rstrip(".!?")
        self.results[self.current_testclass.name][test_name] = {
            'passed': True,  # Assume we've passed it, unless we detect a subtest failure
            'subtests passed': 0,
            'subtests failed': 0,
            'subtests total': 0,
        }
        self.current_results = self.results[self.current_testclass.name][test_name]
        self.subtest_outcomes = []

    def stopTest(self, test: unittest.TestCase) -> None:
        """Finalize the test phase of an individual test method."""
        test_description = test.shortDescription().rstrip(".!?")
        self.stream.write_test_outcome(
            test_description,
            self.current_results,
            self.subtest_outcomes
        )

    def addSubTest(
        self,
        test: unittest.TestCase,
        subtest: unittest.TestCase,
        outcome: typing.Optional[TestOutcome],
    ) -> None:
        """Process the result of a subTest."""
        super().addSubTest(test, subtest, outcome)
        self.current_results["subtests total"] += 1
        if outcome:
            self.current_results["passed"] = False
            self.current_results["subtests failed"] += 1
            self.subtest_outcomes.append((subtest, outcome))
            return

        self.current_results["subtests passed"] += 1
