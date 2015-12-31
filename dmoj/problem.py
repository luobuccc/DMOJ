import json
import os
from functools import partial

from dmoj import checkers
from dmoj.data_loader import ZippedDataLoader, FileDataLoader
from dmoj.test_case import TestCase, BatchedTestCase
from dmoj.utils.module import load_module


class Problem(object):
    def __init__(self, code, loader=None):
        self.code = code
        self.loader = loader
        self.init = init = json.load(loader.open_text('init.json'))

        self.data_loaders = [FileDataLoader(loader)]  # type: list[DataLoader]
        if 'archive' in init:
            self.data_loaders.append(ZippedDataLoader(loader.open_binary(init['archive'])))
        if 'generator' in init:
            # Perform magic
            # self.data_loaders.append(...)
            pass

        self.cases = cases = []
        for case in init['test_cases']:
            if 'data' in case:
                cases.append(BatchedTestCase([
                    (self._load_data(item['input']), self._load_data(item['output']))
                    for item in case['data']
                ], case['points']))
            else:
                cases.append(TestCase(self._load_data(case['input']),
                                      self._load_data(case['output']),
                                      case['points']))

        self._checker = self._load_checker()

    def _load_data(self, name):
        for loader in self.data_loaders:
            try:
                return loader.load(name)
            except IOError:
                pass
        raise IOError('Failed to load problem data file: %s' % name)

    def _load_checker(self):
        try:
            name = self.init.get('checker', 'standard')
            if isinstance(name, dict):
                params = name.get('parameters', {})
                name = name['name']
            else:
                params = {}
            if '.' in name:
                try:
                    with self.loader.open_text(name) as f:
                        checker = load_module(os.path.splitext(os.path.split(name)[1])[0],
                                              f.read(), getattr(f, 'name', name))
                except IOError:
                    raise IOError('Checker module path does not exist: %s' % name)
            else:
                checker = getattr(checkers, name)
        except AttributeError:
            raise RuntimeError('Error loading checker')
        if not hasattr(checker, 'check') or not callable(checker.check):
            raise RuntimeError('Malformed checker: no check method found')

        return partial(checker.check, **params)
