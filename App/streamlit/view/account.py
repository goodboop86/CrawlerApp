import streamlit as st
import json
import requests


def app():
    with open("setting.json") as f:
        conf = json.load(f)

    st.title('お客さま情報')
    url = conf['fastapi']['url']['account']
    request = json.dumps({"address": "dummy"})

    response = requests.post(url, request)
    res = response.json()

    if response.ok:
        st.markdown(
            f"""
            ---
            ### メールアドレス
            #### {res['address']}

            ---


            ### パスワード
            \********

            ---

            ### 対象のお客さま
            {"・".join([k for k in res['gender']])}

            ---
            
            ### 年齢
            {"・".join([k for k in res['age']])}

            ---
            
            ### ショップの特徴
            {"・".join([k for k in res['feature']])}
            
            ---
            """
        )
    else:
        st.error(response.json())

    with st.expander("パスワード変更"):
        old_password = st.text_input("古いパスワード", type='password')
        password = st.text_input("新しいパスワード", type='password')

        submitted = st.button("更新")


if __name__ == '__main__':
    app()
