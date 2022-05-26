import streamlit as st
import json
import requests
import register
import marketing
import top

loggedin_pages = {"ショップ登録": register, "分析": marketing}
top_page = {"ログイン/登録": top}

if 'username' not in st.session_state:
    st.session_state.username = ""

if 'password' not in st.session_state:
    st.session_state.password = ""

if 'is_loggedin' not in st.session_state:
    st.session_state.is_loggedin = False

with st.sidebar:
    pages = loggedin_pages if st.session_state.is_loggedin else top_page

    selection = st.selectbox("select", list(pages.keys()))
    page = pages[selection]

    if st.session_state.is_loggedin:
        st.button('ログアウト', on_click=top.logout)

page.app()
