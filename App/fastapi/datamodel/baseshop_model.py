from pydantic import BaseModel, Field, HttpUrl


class Shop(BaseModel):
    fb_app_id: int = Field(..., description='サイトID')
    og_description: str = Field(..., description='説明')
    og_title: str = Field(..., description='タイトル')
    og_image: HttpUrl = Field(..., description='画像URL')
    og_url: HttpUrl = Field(..., description='サイトURL')
    og_site_name: str = Field(..., description='サイト名')
    og_type: str = Field(..., description='？？')
    content_type: str = Field('Shop', description='クロール種類')

    class Config:
        schema_extra = {
            "example": {
                "fb_app_id": 350947278320210,
                "og_description": "本サイトは、BASEデザインマーケットのテンプレート「shoot」のデモサイトです。shootは、直感的でダイナミックなグリッドレイアウトデザインです。レスポンシブ対応で、スマートフォン、タブレットにも最適化しております。【機能紹介】◆フォントデザイン機能16種類のフォントからお選びできます。ロゴの他、メニューや見出しタイトルもフォントの選択ができます。◆カラーリング機能メインカラーを設定すれば、様々な場所に配色されます。◆模様機能ストライプや水玉やチェック、千鳥格子など14種類の模様をつける事ができます。◆スライドショー機能トップ画面にスライドショーを設置できます。（最大5枚）画像が小さくならないようにスマートフォン用と分けて設置できます。また、横幅もフルスクリーンかレイアウトに合わせるか選ぶ事ができる他、スライド時の種類をお選びできます。◆レイアウト機能デスクトップ画面時の商品列を、4列か3列かにお選びできます。◆ABOUT画面画像と動画が設置できます。動画はYOUTUBEやVIMEOに対応しています。◆インフォメーション機能トップ画面にインフォメーションを設置できます。（最大3件）◆重要なお知らせ機能災害の遅延など重要なお知らせがある時に、赤字で表示する機能です。◆フッター最適化フッターにロゴや外部サイトなどを貼り付ける事ができます。◆BLOG→NEWS表記変更詳しい使用方法は、こちらを参照してください。http://reo.thebase.in/blog/2017/04/10/232435_3動画の埋め込み方法のご説明http://reo.thebase.in/blog/2015/09/01/174651サイトの色決めを助ける無料サービスの紹介http://reo.thebase.in/blog/2017/04/10/221938他参考ショップhttp://outlet.unde.jp/",
                "og_title": "SHOOT デモサイト powered by BASE",
                "og_image": "https://static.thebase.in/img/shop/ogp.png",
                "og_url": "https://reo.thebase.in/",
                "og_site_name": "SHOOT デモサイト powered by BASE",
                "og_type": "website",
                "content_type": "Shop"}
        }


class Item(BaseModel):
    fb_app_id: int = Field(..., description='サイトID')
    og_description: str = Field(..., description='説明')
    og_title: str = Field(..., description='タイトル')
    og_image: HttpUrl = Field(..., description='画像URL')
    og_url: HttpUrl = Field(..., description='サイトURL')
    og_site_name: str = Field(..., description='サイト名')
    og_type: str = Field(..., description='？？')
    product_price_amount: int = Field(..., description='価格')
    product_price_currency: str = Field(..., description='通貨')
    product_product_link: str = Field(..., description='商品URL')
    content_type: str = Field('Item', description='クロール種類')


class ItemList(BaseModel):
    item_list: list[Item] = Field(..., description='商品リスト')
    content_type: str = Field('ItemList', description='クロール種類')


class CrawlList(BaseModel):
    crawl_list: list[HttpUrl] = Field(..., description='商品URLリスト')
    content_type: str = Field('CrawlList', description='クロール種類')
