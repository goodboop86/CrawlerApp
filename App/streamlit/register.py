import streamlit as st
import json
import requests


def app():

    with open("setting.json") as f:
        conf = json.load(f)

    st.title('ショップ登録ツール')

    url = st.text_input('url', conf['fastapi']['url']+"/crawl")
    target = st.text_input(
        'クロールしたいURLを教えてください。(https://example.myshop.com)', 'https://reo.thebase.in/')

    crawl_domain = st.radio('crawl_domain', ['baseshop'])
    crawl_type = st.radio(
        'crawl_type', ["item_from_itempage", "items_from_itempagelist",
                       "item_from_toppage", "itemurls_from_sitemap"])

    request = json.dumps(
        {
            "target": target,
            "strategy": {
                "crawl_domain": crawl_domain,
                "crawl_type": crawl_type
            }
        })

    print(request)

    response = requests.post(url, request)
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
