import os
import re
import traceback

reexecutor = re.compile('([A-Z0-9]+)\.py$')
available = set(i.group(1) for i in map(reexecutor.match,
                                        os.listdir(os.path.dirname(__file__)))
                if i is not None)

package_path = __name__.split('.')[1:]


def load_executor(executor):
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
    def __init__(self):
        super(ExecutorLoader, self).__init__()
        self._available = None
        self._sandbox = True

    def _populate(self):
        if self._available is None:
            from dmoj.conf import only_executors, exclude_executors, env

            executors = available.copy()
            if only_executors:
                executors &= only_executors
            if exclude_executors:
                executors -= exclude_executors
            self._available = sorted(executors)
            self._sandbox = env.get('selftest_sandboxing', True)

    def _load(self, name):
        executor = load_executor(name)
        if executor is None:
            return None
        if hasattr(executor, 'initialize') and not executor.initialize(sandbox=self._sandbox):
            return None
        if hasattr(executor, 'aliases'):
            for alias in executor.aliases():
                self[alias] = executor
        else:
            self[name] = executor
        return executor

    def __missing__(self, key):
        self._populate()
        executor = self._load(key)
        if executor is None:
            raise KeyError()
        return executor

    def load_all(self):
        self._populate()
        for name in self._available:
            self._load(name)


executors = ExecutorLoader()
