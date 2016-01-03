from dmoj.problem import Problem


class Grader(object):
    def __init__(self, problem, submission):
        self.problem = problem  # type: Problem
        self.submission = submission

    def grade(self):
        for test_case in self.problem.cases:
            test_case.grade(self)

    def on_batch_begin(self):
        pass

    def on_batch_end(self):
        pass

    def on_test_case(self, result):
        pass
