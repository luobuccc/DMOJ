from dmoj.executors import executors


class Submission(object):
    def __init__(self, problem, language, source_code, time_limit, memory_limit, short_circuit):
        self.problem = problem
        self.language = language
        self.code = source_code
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.short_circuit = short_circuit

        self.executor = executors[language].Executor(problem.code, source_code)
