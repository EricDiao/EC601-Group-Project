class Module:

    def __init__(self, params):
        pass

    def invoke(self):
        raise NotImplementedError

    def install_dependencies(self):
        raise NotImplementedError

    def clean_up(self):
        raise NotImplementedError
