from enum import Enum


class CrawlDomain(Enum):
    """
    クロールするドメイン
    クエリパラメータ = 利用するクラス名(UpperCamel) で指定

    ***Baseshop***:     BASE

    """
    baseshop = "BaseShopCrawler"


class CrawlType(Enum):
    """
    クロールする種類
    クエリパラメータ = 利用するメソッド名(LowerSnake) で指定

    (Input -> Output)
    ***Item***:         商品URL -> アイテム情報
    ***Shop***:         ショップURL -> ショップ情報
    ***CrawlList***:    サイトマップリンク -> 商品URLリスト
    ***ItemList***:     商品URLリスト -> アイテム情報リスト

    """
    item = "__item"
    shop = "__shop"
    crawl_list = "__crawl_list"
    item_list = "__item_list"
