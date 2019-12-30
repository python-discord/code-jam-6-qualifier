import argparse

import testsuite.runner


parser = argparse.ArgumentParser(
    prog="python -m testsuite",
    description="Python Discord Code Jam: Qualifier Test Suite"
)
testsuite.runner.run_testsuite()
