import streamlit as st
import json
import requests


def app():

    with open("setting.json") as f:
        conf = json.load(f)

    st.title('ショップ登録ツール')

    url = st.text_input('url', conf['fastapi']['url']+"/crawl")

    domains = {"BASE": "baseshop"}
    crawl_domain = st.radio('取得するドメイン', domains.keys())

    types = {"商品": "item_from_itempage", "複数商品": "items_from_itempagelist",
             "トップページ": "item_from_toppage", "商品リスト": "itemurls_from_sitemap"}

    crawl_type = st.radio('取得する内容', types.keys())

    target = st.text_input(
        f'({crawl_type}) URLを教えてください。: 例:https://example.myshop.com', 'https://reo.thebase.in/')

    request = json.dumps(
        {
            "target": target,
            "strategy": {
                "crawl_domain": domains[crawl_domain],
                "crawl_type": types[crawl_type]
            }
        })

    if st.button('確認'):

        response = requests.post(url, request)
        st.success("OK!") if target == response.json()["og_url"] else st.success(
            "NG...")
        st.write(response.json())

    st.header("あなたのお店について教えてください")
    sex = st.selectbox('お客さまはどちらが多いですか？',
                       ['男性', '女性'])
    st.write(f'Selected: {sex}')
    age = st.selectbox('年齢層は？',
                       ['~10代', '20代', '30代', '40代', '50代', '60代~'])
    st.write(f'Selected: {age}')


if __name__ == '__main__':
    app()
