import os
import sys
import subprocess
import re


class Module:
    def __init__(self, params):
        self.params = params
        self.name = "Wireless Scan"
        self.description = "Wireless Scan"
        self.version = "1.0"

    def invoke(self):
        try:
            assert self._check_iw_installation()
            assert len(self._find_ieee80211_interfaces()) > 0
        except AssertionError:
            return {"error": "Cannot find Wireless capbilty on the server."}, 500
        results = []
        for interface in self._find_ieee80211_interfaces():
            output = subprocess.check_output(["iw", interface, "scan"])
            results.append(
                {"interface": interface, "scan_result": output.decode("utf-8"), "advice": self._generate_advice_fromscan_result(self._parse_scan_result(output.decode("utf-8")))})
        return {"results": results}

    def install_dependencies(self):
        assert os.uname()[0] == "Linux"
        assert self._check_iw_installation()
        assert len(self._find_ieee80211_interfaces()) > 0

    def _check_iw_installation(self):
        try:
            subprocess.check_output(["iw"])
        except FileNotFoundError:
            return False
        return True

    def _find_ieee80211_interfaces(self):
        output = subprocess.check_output(["iw", "dev"])
        return re.findall("Interface (.+)", output.decode("utf-8"))

    def _parse_scan_result(self, scan_result):
        return scan_result

    def _generate_advice_fromscan_result(self, scan_result):
        return scan_result
