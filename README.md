# Code Jam 6: Qualifier

- **Deadline:** 2020-01-10 12:00 UTC
- **Submission form:** link to form here

The qualifier task for the upcoming Winter Code Jam is to write an ISO-8601 timestamp parser function. We have provided you with a stub function in [qualifier.py](./qualifier.py) and it is your job to write the function body. To qualify for the code jam, your function needs to pass all of the basic requirements listed below. Additional points will be awarded if your function also passes (some of) the advanced requirements.

While you are allowed to rewrite the docstring of the function, please make sure to keep the function signature as it is.

### Basic Requirements
  - Must return an instance of `datetime.datetime` that is equivalent to the given ISO-8601 timestamp
  - Must parse date strings in the format `YYYY-MM-DD`
  - Must parse combined datetime strings in the format `<date>T<time>`, where `<time>` can be one of:
     - `hh:mm:ss`
     - `hh:mm`
     - `hh`
  - If given invalid input, raise a `ValueError` explaining what went wrong.

### Advanced Requirements (optional, for extra points)
  - Support the truncated date format `YYYYMMDD`
  - Support fractional seconds `hh:mm:ss.sss`
  - Support the truncated time formats `hhmmss.ssss`, `hhmmss`, `hhmm`
  - Support time zones
    - Timestamps without a timezone are local time
    - Timestamps with a timezone are relative to the UTC
      - Supported formats are `Z`, `±hh:mm`, `±hhmm` and `±hh`

## Examples

```py
>>> parse_iso8601("2019-12-16")
datetime.datetime(2019, 12, 16, 0, 0)
>>> parse_iso8601("2017-01-08T12")
datetime.datetime(2017, 1, 8, 12, 0)
>>> parse_iso8601("2008-12-03T08:15")
datetime.datetime(2008, 12, 3, 8, 15)
>>> parse_iso8601("1991-02-20T11:23:58")
datetime.datetime(1991, 2, 20, 11, 23, 58)
>>> parse_iso8601("2000-10-16T09:23:61")
Traceback (most recent call last):
  File "<stdin>", line 7, in parse_iso8601
ValueError: Invalid value for seconds
```

## Notes
- Due to the limitations of Python's `datetime` module, some dates specified in the ISO-8601 standard are impossible to be represented as a `datetime.datetime`. Therefore, those formats have not been included in the challenge.

- We are aware that `datetime.datetime` has a built-in classmethod, `datetime.fromisostring`, to parse ISO-8601 timestamps. Since it is your task to write a parser, using the built-in parser will lead to you not passing the qualifier.
