import subprocess
import os
import sslyze


class Module:
    def __init__(self, params):
        self.params = params
        self.name = "SSL Scan"
        self.description = "SSL Scan"
        self.version = "1.0"
        self.pip_dependencies = ["sslyze"]

    def invoke(self):
        try:
            assert self.params["target"] is not None
        except AssertionError:
            return {"error": "Invalid parameters"}, 400

        scan_result = sslyze.scan_target(self.params["target"])
        return {"result": scan_result}

    def install_dependencies(self):
        for dependency in self.pip_dependencies:
            subprocess.call(["pip3", "install", dependency]).check_returncode()
