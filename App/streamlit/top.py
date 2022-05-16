import streamlit as st
import json
import requests


def app():
    st.title('トップページ')
    st.text('こんにちは！この管理画面ではショップの登録や利用されたデータの閲覧が可能です。')
    st.text('このサービスは事業者さまの製品を他のECサイトでも相互的に表示することで、商品が検索されるようになるサービスです。')
    st.text('左側のタブから「ショップを登録」へ移動するとあなたのECショップをこちらの検索サービスに登録できます。')
    st.text(
        '「お客さまデータを見る」へ移動すると、他のECからあなたの商品へアクセスした情報がわかります。これにより商品を選ぶ上でのお客さまのターゲットがわかります。')


if __name__ == '__main__':
    app()
