import streamlit as st
import json
import requests
from logic.auth_handler import AuthHandler


def app():
    with open("setting.json") as f:
        conf = json.load(f)

    st.title('お客さま情報')
    response = AuthHandler.account_info(
        url=conf['fastapi']['url']['account_info'])

    res = response.json()

    if response.ok:
        for elem in res:
            st.header(elem)
            st.text(res[elem])

    else:
        st.error(response.json())

    with st.expander("パスワード変更"):
        old_password = st.text_input("古いパスワード", type='password')
        password = st.text_input("新しいパスワード", type='password')

        submitted = st.button("更新")


if __name__ == '__main__':
    app()
