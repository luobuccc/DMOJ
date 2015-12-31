from zipfile import ZipFile

from dmoj.proxies import StreamDataProxy


class DataLoader(object):
    def load(self, name):
        """
        Load problem data file.
        """
        raise NotImplementedError()

    def close(self):
        """
        Perform any clean up necessary.
        """
        pass


class ZippedDataLoader(DataLoader):
    def __init__(self, stream):
        self.zipfile = ZipFile(stream, 'r', allowZip64=True)

    def load(self, name):
        try:
            return StreamDataProxy(self.zipfile.open(name))
        except KeyError:
            raise IOError()

    def close(self):
        self.zipfile.close()


class FileDataLoader(DataLoader):
    def __init__(self, loader):
        self.loader = loader

    def load(self, name):
        return self.loader.open_proxy(name)


class GeneratorDataLoader(DataLoader):
    def __init__(self, executor):
        self.executor = executor

    def load(self, name):
        # Perform some magic that creates a proxy, which would generate data for every case.
        raise IOError()
