import streamlit as st
import json
import requests


def app():

    with open("setting.json") as f:
        conf = json.load(f)

    st.title('ショップ登録ツール')

    url = st.text_input('url', conf['fastapi']['url']+"/crawl/baseshop")
    shop = st.text_input(
        'あなたのショップのURLを教えてください。(https://example.myshop.com)', 'https://reo.thebase.in/')

    response = requests.post(url, json.dumps({"target": shop}))
    st.write(response.json())

    product = st.text_input(
        'あなたの製品のURLを教えてください。(https://example.myshop.com/items/1234567)', 'https://reo.thebase.in/items/6019347')

    response = requests.post(url, json.dumps({"target": product}))
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
