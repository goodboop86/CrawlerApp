
from audioop import add
import streamlit as st
import json
import requests


class AuthHandler(object):

    @staticmethod
    def oauth2_signup(username, password, is_check, url):
        params = json.dumps(
            {"username": username, "password": password})
        response = requests.post(url, params)

        st.success(f"{response.text}") if response.ok else st.error(
            f"{response.text}")

    @staticmethod
    def oauth2_signin(username, password, url):
        params = {"username": username,
                  "password": password, "grant_type": "password"}
        response = requests.post(url, params)
        if response.ok:
            st.info(f"{response.text}")
            st.session_state.is_signedin = True
            st.session_state.access_token = response.json()["access_token"]
        else:
            st.error(f"{response.text}")

    @staticmethod
    def signout():
        st.session_state.is_signedin = False
        st.session_state.access_token = None

    @staticmethod
    def user_info(url):
        headers = {'Authorization': 'Bearer {}'.format(
            st.session_state.access_token)}

        res = requests.get(url, headers=headers)
        st.info(res.content)

    @staticmethod
    def account_info(url):
        headers = {'Authorization': 'Bearer {}'.format(
            st.session_state.access_token)}

        res = requests.get(url, headers=headers)
        return res

    @staticmethod
    def register(params, url):
        headers = {'Authorization': 'Bearer {}'.format(
            st.session_state.access_token)}
        res = requests.post(url, params, headers=headers)
        st.info(res.content)
