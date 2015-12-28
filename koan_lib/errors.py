class BuildError(Exception):
    def __init__(self, message="Build error."):
        self.message = message


class TestError(Exception):
    def __init__(self, message="Test error."):
        self.message = message
