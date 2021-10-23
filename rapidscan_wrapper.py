import subprocess
import os
import sys

RSCAN_LOCATION = "./rapidscan/rapidscan.py"
PYTHON2_LOCATION = "python2"


class RSException(Exception):
    pass


class RScanResult:
    '''
    Class `RScanResult`:

    Contains the results from a single `RapidScan` run.
    '''

    def __init__(self, result):
        pass

    def _parse(self):
        pass

    def get_text(self):
        pass

    def dump(self):
        pass


class RapidScan:
    '''
    Class `RapidScan`:

    An instance of the RapidScan. The instance is stateless which means the instance can be called multiple times, with different parameters. All those calls will return result from RapidScan, indepent from previous scans.

    Call `RapidScan.run()` with parameters to run the scanner. The method will return results contained in a `RScanResult` instance.
    '''

    def __init__(self):
        pass

    def run(self):
        pass


# Check if the required module do exists.
try:
    subprocess.run([PYTHON2_LOCATION, "-V"], stderr=subprocess.PIPE,
                   stdout=subprocess.PIPE).check_returncode()
except subprocess.CalledProcessError:
    raise RSException(
        "Python 2 interpreter `{}` does not exist.".format(PYTHON2_LOCATION))

if not os.path.exists(RSCAN_LOCATION):
    raise RSException("RapidScan does not exist at {}".format(RSCAN_LOCATION))
