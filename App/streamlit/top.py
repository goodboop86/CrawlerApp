import streamlit as st
import json
import requests
import hashlib


def signin(_address):
    st.session_state.is_signedin = True
    st.session_state.address = _address


def signout():
    st.session_state.is_signedin = False


def auth(_address, _password, _conf):
    url = _conf['fastapi']['url']['signin']
    request = json.dumps({"address": _address, "password": _password})
    response = requests.post(url, request)

    if response.ok:
        st.info(f"{response.text}")
        if response.json()["status"] == "success":
            signin(_address)
    else:
        st.error(f"{response.text}")


def regist(_address, _password, c_v, _conf):
    url = _conf['fastapi']['url']['signup']
    request = json.dumps({"address": _address, "password": _password})
    response = requests.post(url, request)
    if response.ok:
        st.info(f"{response.text}")
    else:
        st.error(f"{response.text}")


def app():

    with open("setting.json") as f:
        conf = json.load(f)

    address = st.text_input("ログインアドレス")
    password = st.text_input("ログインパスワード", type='password')

    submitted = st.button(
        "ログイン", on_click=auth, args=(address, password, conf))

    with st.expander("未登録の方"):
        st.write("こちらからご登録ください")
        address = st.text_input("メールアドレス")
        password = st.text_input("パスワード (半角英数字8文字以上64文字以下)", type='password')
        checkbox_val = st.checkbox("規約に合意する")

        submitted = st.button("登録", on_click=regist,
                              args=(address, password, checkbox_val, conf))

    res = requests.get(conf["streamlit"]["url"]["term"])
    with st.expander("利用規約"):
        st.markdown(res.content.decode('utf-8'), unsafe_allow_html=True)


if __name__ == '__main__':
    app()
