import streamlit as st
import json
import requests


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
    gender_result = st.multiselect(
        gender["question"] +
        " ({}個まで)".format(str(gender["max_choice"])),
        gender["choice"].keys())

    st.write(", ".join(gender_result))
    is_filled_gender = len(gender_result) <= gender["max_choice"]

    age = conf["streamlit"]["question"]["age"]

    age_result = st.multiselect(
        age["question"] +
        " ({}個まで)".format(str(age["max_choice"])),
        age["choice"].keys())
    st.write(", ".join(age_result))
    is_filled_age = len(age_result) <= age["max_choice"]

    feature = conf["streamlit"]["question"]["feature"]
    feature_result = st.multiselect(
        feature["question"] +
        " ({}個まで)".format(str(feature["max_choice"])),
        feature["choice"].keys(),
        [])
    st.write(", ".join(feature_result))
    is_filled_feature = len(feature_result) <= feature["max_choice"]

    if is_filled_age & is_filled_gender & is_filled_feature:
        # TODO accessTokenを利用してアクセスする様に更新
        if st.button('登録'):
            url = conf['fastapi']['url']['register']
            request_ = json.dumps({
                "address": "dummy",
                "registration": {
                    "gender": {key: gender["choice"][key] for key in gender_result},
                    "age": {key: age["choice"][key] for key in age_result},
                    "feature":  {key: feature["choice"][key] for key in feature_result}
                }})
            st.info(request_)
            response = requests.post(url, request_)
            st.info(response.text)
    else:
        st.error("記入に誤りがあります。")


if __name__ == '__main__':
    app()
