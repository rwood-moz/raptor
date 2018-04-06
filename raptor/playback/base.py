# abstract class for all playback tools

from abc import ABCMeta, abstractmethod


class Playback(object):
    __metaclass__ = ABCMeta

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
