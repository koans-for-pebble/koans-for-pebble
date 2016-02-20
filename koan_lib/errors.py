class BuildError(Exception):
    def __init__(self, message="Build error."):
        self.message = message


class TestError(Exception):
    def __init__(self, message="Test error."):
        self.message = message


class InstallError(Exception):
    def __init__(self, message="Install error."):
        self.message = message
