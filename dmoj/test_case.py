from dmoj.result import Result


class TestCase(object):
    def __init__(self, input, output, points):
        assert hasattr(input, 'fileno') and hasattr(output, 'fileno')

        self.input = input
        self.output = output
        self.total = points
        self.result = Result()

    def grade(self, grader):
        pass


class BatchedTestCase(object):
    def __init__(self, list, points):
        self.cases = [TestCase(input, output, points) for input, output in list]

    def grade(self, grader):
        grader.on_batch_begin()
        for case in self.cases:
            case.grade(grader)
        grader.on_batch_end()
