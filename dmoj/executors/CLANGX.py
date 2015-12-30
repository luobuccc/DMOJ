from .CPP11 import Executor as CPP11Executor
from dmoj.conf import env


class Executor(CPP11Executor):
    command = env['runtime'].get('clang++')
    name = 'CLANG++'

initialize = Executor.initialize
