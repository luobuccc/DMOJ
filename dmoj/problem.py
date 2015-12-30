import json

from dmoj.data_loader import ZippedDataLoader, FileDataLoader
from dmoj.exception import DataNotFoundError
from dmoj.test_case import TestCase, BatchedTestCase


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

    def _load_data(self, name):
        for loader in self.data_loaders:
            try:
                return loader.load(name)
            except DataNotFoundError:
                pass
        raise DataNotFoundError()
