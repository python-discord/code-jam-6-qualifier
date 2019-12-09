code-jam-6-qualifier
====================

For this Code Jam, we have provided you with the empty body for an ISO-8601 timestamp parser function. Your qualifier task is to write the function body so that it passes all the tests.

The function must fulfill the following criteria to qualify you for the code jam:
---------------------------------------------------------------------------------

  - Must return an instance of `datetime.datetime` that is equivalent to the given ISO-8601 timestamp
  - Must parse dates in the format `YYYY-MM-DD` and `YYYY-MM`
  - Must combined datetimes in the format `<date>T<time>`, where `<time>` can be one of:
     - `hh:mm:ss`
     - `hh:mm`
     - `hh`
  - If given invalid input, raise a `ValueError` explaining what went wrong.

The following criteria are optional, but will net you extra points:
-------------------------------------------------------------------

  - Support the truncated date format `YYYYMMDD`
  - Support fractional seconds `hh:mm:ss.sss`
  - Support the truncated time formats `hhmmss.ssss`, `hhmmss`, `hhmm`
  - Support time zones
    - Timestamps without a timezone are local time
    - Timestamps with a timezone are relative to the UTC
      - Supported formats are `Z`, `±hh:mm`, `±hhmm` and `±hh`



NOTE
----
Due to the limitations of Python's datetime module, some dates are impossible to represent as a `datetime.datetime`. Therefore, those formats have not been included in the challenge.

We are aware that `datetime.fromisoformat` is a function that exists. The challenge is to write a parser, and thus using the function will lead to not passing the qualifier.
