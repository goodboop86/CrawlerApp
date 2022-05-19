import abc


class Crawler(object, metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def __init__(self) -> None:
        pass

    @abc.abstractclassmethod
    def __call__(self):
        pass

    @abc.abstractclassmethod
    def __item(self):
        pass

    @abc.abstractclassmethod
    def __shop(self):
        pass

    @abc.abstractclassmethod
    def __crawl_list(self):
        pass

    @abc.abstractclassmethod
    def __item_list(self):
        pass
