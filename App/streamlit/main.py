import streamlit as st
from view import register
from view import marketing
from view import account
from view import top
from logic.auth_handler import AuthHandler
import requests


def signout():
    auth = AuthHandler()
    auth.signout()

# デバッグ用(後で消す)


def user_info():
    headers = {'Authorization': 'Bearer {}'.format(
        st.session_state.access_token)}
    res = requests.get("http://127.0.0.1:8000/users/me", headers=headers)
    st.info(res.content)


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
        st.button('ログアウト', on_click=signout)
        st.button("ユーザ情報", on_click=user_info)

page.app()
