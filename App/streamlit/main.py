import streamlit as st
from view import register, marketing, account, top
from logic.auth_handler import AuthHandler
import requests
import json


def signout():
    auth = AuthHandler()
    auth.signout()


with open("setting.json") as f:
    conf = json.load(f)

signedin_pages = {"ショップ登録": register,
                  "分析": marketing,
                  "お客さま情報": account}
top_page = {"ログイン/登録": top}

if 'is_signedin' not in st.session_state:
    st.session_state.is_signedin = False

if 'access_token' not in st.session_state:
    st.session_state.access_token = ""

with st.sidebar:
    pages = signedin_pages if st.session_state.is_signedin else top_page

    selection = st.selectbox("select", list(pages.keys()))
    page = pages[selection]

    if st.session_state.is_signedin:
        st.button('ログアウト', on_click=AuthHandler.signout)
        st.button("ユーザ情報", on_click=AuthHandler.user_info,
                  args=([conf['fastapi']['url']['users_me']]))

page.app()
