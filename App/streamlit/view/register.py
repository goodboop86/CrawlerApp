import streamlit as st
import json
import requests
from logic.auth_handler import AuthHandler


def register(params_, conf_):
    url = conf_['fastapi']['url']['register']
    st.info(params_)
    #response = requests.post(url, params_)
    # st.info(response.text)
    auth = AuthHandler(conf=conf_)
    auth.register(params=params_)


def multiselect_form(elem):
    elem_result = st.multiselect(
        elem["question"] +
        " ({}個まで)".format(str(elem["max_choice"])),
        elem["choice"].keys())

    st.write(", ".join(elem_result))
    is_filled_elem = len(elem_result) <= elem["max_choice"]

    return ({key: elem["choice"][key] for key in elem_result}, is_filled_elem)


def app():

    with open("setting.json") as f:
        conf = json.load(f)

    st.title('ショップ登録ツール')

    url = st.text_input('url', conf['fastapi']['url']["crawl"])

    domains = {"BASE": "baseshop"}
    crawl_domain = st.radio('取得するドメイン', domains.keys())

    types = {"商品": "item_from_itempage", "複数商品": "items_from_itempagelist",
             "トップページ": "item_from_toppage", "商品リスト": "itemurls_from_sitemap"}

    crawl_type = st.radio('取得する内容', types.keys())

    target = st.text_input(
        f'({crawl_type}) URLを教えてください。: 例:https://example.myshop.com', 'https://reo.thebase.in/')

    request = json.dumps(
        {
            "target": target,
            "strategy": {
                "crawl_domain": domains[crawl_domain],
                "crawl_type": types[crawl_type]
            }
        })

    if st.button('確認'):
        response = requests.post(url, request)
        st.success("OK!") if target == response.json()["og_url"] else st.success(
            "NG...")
        st.write(response.json())

    st.header("あなたのお店について教えてください")

    gender = conf["streamlit"]["question"]["gender"]
    gender_result, is_filled_gender = multiselect_form(elem=gender)

    age = conf["streamlit"]["question"]["age"]
    age_result, is_filled_age = multiselect_form(elem=age)

    feature = conf["streamlit"]["question"]["feature"]
    feature_result, is_filled_feature = multiselect_form(elem=feature)

    if is_filled_age & is_filled_gender & is_filled_feature:
        params = json.dumps({
            "address": "dummy",
            "gender": gender_result,
            "age": age_result,
            "feature":  feature_result
        })
        # todo accessTokenを利用してアクセスする様に更新
        st.button('登録', on_click=AuthHandler.register, args=(
            params, conf["fastapi"]["url"]["register"]))

    else:
        st.error("記入に誤りがあります。")


if __name__ == '__main__':
    app()
