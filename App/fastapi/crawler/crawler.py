import abc


class Crawler(object, metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def __init__(self) -> None:
        pass

    @abc.abstractclassmethod
    def __call__(self):
        pass

    @classmethod
    def _item_from_itempage(self):
        pass

    @classmethod
    def _items_from_itempagelist(self):
        pass

    @classmethod
    def _item_from_toppage(self):
        pass

    @classmethod
    def _itemurls_from_sitemap(self):
        pass
