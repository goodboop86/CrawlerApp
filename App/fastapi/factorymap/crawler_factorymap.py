from enum import Enum
from crawler.baseshop_crawler import BaseShopCrawler
from datamodel.request_model import CrawlDomain, CrawlType
from crawler.crawler import Crawler


class CrawlDomainMap(Enum):
    """
    Factoryで呼び出されるクローラのクラス
    クエリパラメータで指定されたdomainに対応したクローラを返す
    ***Baseshop***:     BASE

    """
    baseshop = BaseShopCrawler

    @classmethod
    def should_match_datamodel(cls):
        """
        各要素は対応するrequest datamodelの要素と一致する必要がある
        """
        if [*cls.__members__] is not CrawlDomain.schema()["properties"]["required"]["default"]:
            raise(f"{cls.__name__} should match schema!")


class CrawlTypeMap(Enum):
    """
    Factoryで呼び出されるクローラの関数に関するクラス
    クエリパラメータで指定されたtypeに対応した関数の名前を返す

    (Input -> Output)
    ***Item***:         商品URL -> アイテム情報
    ***Shop***:         ショップURL -> ショップ情報
    ***CrawlList***:    サイトマップリンク -> 商品URLリスト
    ***ItemList***:     商品URLリスト -> アイテム情報リスト

    """
    item_from_itempage = "_item_from_itempage"
    items_from_itempagelist = "_items_from_itempagelist"
    item_from_toppage = "_item_from_toppage"
    itemurls_from_sitemap = "_itemurls_from_sitemap"

    @classmethod
    def should_match_datamodel(cls):
        """
        各要素は対応するrequest datamodelの要素と一致する必要がある
        """
        if [*cls.__members__] is not CrawlType.schema()["properties"]["required"]["default"]:
            raise(f"[{cls.__name__}] should match schema!")

    @classmethod
    def should_contain_abstract_attribute(cls):
        """
        各要素は対応する抽象クラスの属性に存在する必要がある
        """
        for func in [*cls.__members__.values()]:
            if not hasattr(Crawler, func.value):
                raise(f"[{func.value}] should contain abstract attribute!")
