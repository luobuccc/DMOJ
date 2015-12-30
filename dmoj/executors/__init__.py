import os
import re
import traceback

from judgeenv import env, only_executors, exclude_executors

reexecutor = re.compile('([A-Z0-9]+)\.py$')
available = set(i.group(1) for i in map(reexecutor.match,
                                        os.listdir(os.path.dirname(__file__)))
                if i is not None)
if only_executors:
    available &= only_executors
if exclude_executors:
    available -= exclude_executors
available = sorted(available)

package_path = __name__.split('.')[1:]


def load_module(executor):
    try:
        module = __import__('%s.%s' % (__name__, executor))
    except ImportError as e:
        if e.message not in ('No module named _cptbox',
                             'No module named msvcrt',
                             'No module named _wbox'):
            traceback.print_exc()
        return None
    for part in package_path:
        module = getattr(module, part)
    return getattr(module, executor)


class ExecutorLoader(dict):
    def __init__(self, available):
        super(ExecutorLoader, self).__init__()
        self._available = available

    def _load(self, name):
        executor = load_module(name)
        if executor is None:
            return None
        if hasattr(executor, 'initialize') and not executor.initialize(sandbox=env.get('selftest_sandboxing', True)):
            return None
        if hasattr(executor, 'aliases'):
            for alias in executor.aliases():
                self[alias] = executor
        else:
            self[name] = executor
        return executor

    def __missing__(self, key):
        executor = self._load(key)
        if executor is None:
            raise KeyError()
        return executor

    def load_all(self):
        for name in self._available:
            self._load(name)


executors = ExecutorLoader(available)
