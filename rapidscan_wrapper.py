from genericpath import exists
import subprocess
import os
import sys
from typing import Tuple

RSCAN_LOCATION = "./rapidscan/rapidscan.py"
PYTHON2_LOCATION = "python2"


class RSException(Exception):
    pass


class RScanResult:
    '''
    Class `RScanResult`:

    Contains the results from a single `RapidScan` run.
    '''

    def __init__(self, result, is_ok=True):
        self._result = result
        self._status = is_ok
        self._parse()

    def _parse(self):
        if self._status:
            raise NotImplementedError

    def get_text(self):
        return self._result

    def dump(self):
        raise NotImplementedError


class RapidScan:
    '''
    Class `RapidScan`:

    An instance of the RapidScan. The instance is stateless which means the instance can be called multiple times, with different parameters. All those calls will return result from RapidScan, indepent from previous scans.

    Call `RapidScan.run()` with parameters to run the scanner. The method will return results contained in a `RScanResult` instance.
    '''

    def __init__(self):
        pass

    def _do_run(self, target):
        assert isinstance(target, str)
        cmd = [PYTHON2_LOCATION, RSCAN_LOCATION, target]

        try:
            rscan = subprocess.run(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            rscan.check_returncode()
            ret = RScanResult(rscan.stdout, is_ok=True)
        except subprocess.SubprocessError as e:
            return RScanResult(str(e), is_ok=False)

        return ret

    def run(self, target):
        '''
        Method `RapidScan.run()`:

        Run RapidScan on target `target`, return the result in `RScanResult` instance.
        '''
        # TODO: support target in a subnet.
        if isinstance(target, str):
            target = [target]

        ret = []
        for t in target:
            ret.append(self._do_run(t))

        if len(ret) == 1:
            ret = ret[0]

        return ret


# Check if the required module do exists.
try:
    subprocess.run([PYTHON2_LOCATION, "-V"], stderr=subprocess.PIPE,
                   stdout=subprocess.PIPE).check_returncode()
except subprocess.CalledProcessError:
    raise RSException(
        "Python 2 interpreter `{}` does not exist.".format(PYTHON2_LOCATION))

if not os.path.exists(RSCAN_LOCATION):
    raise RSException("RapidScan does not exist at {}".format(RSCAN_LOCATION))
