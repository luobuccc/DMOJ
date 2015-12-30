import codecs
import os

from dmoj.proxies import StreamDataProxy

utf8_reader = codecs.getreader('utf-8')


class Loader(object):
    def open_binary(self, name):
        """
        Open a file with this loader.

        :param name: file name to load
        :return: file-like object
        """
        raise NotImplementedError()

    def open_text(self, name):
        return utf8_reader(self.open_binary(name))

    def open_proxy(self, name):
        return StreamDataProxy(self.open_binary(name))


class FileSystemLoader(Loader):
    def __init__(self, directory):
        """
        Create a loader from file system.
        :param directory: the directory to load from
        """
        self.directory = directory

    def open_binary(self, name):
        return open(os.path.join(self.directory, name))
