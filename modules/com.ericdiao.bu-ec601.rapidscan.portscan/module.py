class Module:
    def __init__(self, params):
        self.params = params
        self.name = "Quick Scan"
        self.description = "Quick Scan"
        self.version = "1.0"
        self.rapidscan = None

    def invoke(self):
        try:
            assert self.params["target"] is not None
        except AssertionError:
            return {"error": "Invalid parameters"}, 400
        try:
            assert self.rapidscan is not None
        except AssertionError:
            return {"error": "Rapidscan not installed"}, 500

        return self.rapidscan.scan(self.params["target"])

    def install_dependencies(self):
        self.rapidscan = __import__("rapidscan_wrapper")
