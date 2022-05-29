import streamlit as st
import json
import requests
from logic.auth_handler import AuthHandler


def app():
    def signup(_address, _password, _is_check, _conf):
        auth = AuthHandler(address=_address, password=_password,
                           conf=_conf, is_check=_is_check)
        auth.signup()

    def signin(_address, _password, _conf):
        auth = AuthHandler(address=_address, password=_password,
                           conf=_conf)
        auth.signin()

    with open("setting.json") as f:
        conf = json.load(f)

    address = st.text_input("ログインアドレス")
    password = st.text_input("ログインパスワード", type='password')

    submitted = st.button(
        "ログイン", on_click=signin, args=(address, password, conf))

    with st.expander("未登録の方"):
        st.write("こちらからご登録ください")
        address = st.text_input("メールアドレス")
        password = st.text_input("パスワード (半角英数字8文字以上64文字以下)", type='password')
        is_check = st.checkbox("規約に合意する")

        submitted = st.button("登録", on_click=signup,
                              args=(address, password, is_check, conf))

    res = requests.get(conf["streamlit"]["url"]["term"])
    with st.expander("利用規約"):
        st.markdown(res.content.decode('utf-8'), unsafe_allow_html=True)


if __name__ == '__main__':
    app()
