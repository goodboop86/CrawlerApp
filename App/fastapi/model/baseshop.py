from pydantic import BaseModel, Field, HttpUrl


class Shop(BaseModel):
    fb_app_id: int = Field(..., description='サイトID')
    og_description: str = Field(..., description='説明')
    og_title: str = Field(..., description='タイトル')
    og_image: HttpUrl = Field(..., description='画像URL')
    og_url: HttpUrl = Field(..., description='サイトURL')
    og_site_name: str = Field(..., description='サイト名')
    og_type: str = Field(..., description='？？')
    content_type: str = Field('Shop', description='サイトID')


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
    content_type: str = Field('Item', description='クロール種')
