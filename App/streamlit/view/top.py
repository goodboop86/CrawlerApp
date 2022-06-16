import streamlit as st
import json
import requests
from logic.auth_handler import AuthHandler


def app():
    with open("setting.json") as f:
        conf = json.load(f)

    username = st.text_input("ログインアドレス")
    password = st.text_input("ログインパスワード", type='password')

    st.button("ログイン", on_click=AuthHandler.oauth2_signin,
              args=(username, password,  conf['fastapi']['url']['oauth2_signin']))

    with st.expander("未登録の方"):
        st.write("こちらからご登録ください")
        username = st.text_input("メールアドレス")
        password = st.text_input("パスワード (半角英数字8文字以上64文字以下)", type='password')
        is_check = st.checkbox("規約に合意する")

        st.button("登録", on_click=AuthHandler.oauth2_signup,
                  args=(username, password, is_check, conf['fastapi']['url']['oauth2_signup']))

    res = requests.get(conf["streamlit"]["url"]["term"])
    with st.expander("利用規約"):
        st.markdown(res.content.decode('utf-8'), unsafe_allow_html=True)


if __name__ == '__main__':
    app()
