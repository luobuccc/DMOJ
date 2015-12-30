from .C import Executor as CExecutor
from dmoj.conf import env


class Executor(CExecutor):
    command = env['runtime'].get('clang')
    name = 'CLANG'

initialize = Executor.initialize
