class DataProxy(object):
    def load(self):
        """
        Load the proxied data into memory.
        """
        raise NotImplementedError()

    def release(self):
        """
        Perform any action necessary to clean up.
        """
        pass


class StreamDataProxy(object):
    def __init__(self, stream):
        self.stream = stream

    def load(self):
        with self.stream:
            return self.stream.read()