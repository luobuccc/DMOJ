from dmoj.result import Result


class TestCase(object):
    def __init__(self, input, output, points):
        assert hasattr(input, 'fileno') and hasattr(output, 'fileno')

        self.input = input
        self.output = output
        self.total = points
        self.result = Result()


class BatchedTestCase(object):
    def __init__(self, list, points):
        self.cases = [TestCase(input, output, points) for input, output in list]