import streamlit as st
import json
import requests


def app():
    with open("setting.json") as f:
        conf = json.load(f)

    st.title('お客さま情報')
    url = conf['fastapi']['url']['account']
    request = json.dumps({"address": st.session_state.address})

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
            """
        )
    else:
        st.error(response.json())


if __name__ == '__main__':
    app()
