
from audioop import add
import streamlit as st
import json
import requests


class AuthHandler(object):

    def __init__(self, address=None, password=None, conf=None, is_check=None):
        self.address = address
        self.password = password
        self.conf = conf
        self.is_check = is_check

    def oauth2_signup(self):
        url = self.conf['fastapi']['url']['oauth2_signup']
        params = json.dumps(
            {"address": self.address, "password": self.password})
        response = requests.post(url, params)

        st.success(f"{response.text}") if response.ok else st.error(
            f"{response.text}")

    def oauth2_signin(self):
        url = self.conf['fastapi']['url']['oauth2_signin']
        params = {"username": self.address,
                  "password": self.password, "grant_type": "password"}
        response = requests.post(url, params)
        if response.ok:
            st.info(f"{response.text}")
            st.session_state.is_signedin = True
            st.session_state.access_token = response.json()["access_token"]
        else:
            st.error(f"{response.text}")

    def signout(self):
        st.session_state.is_signedin = False
        st.session_state.access_token = None

    def user_info(self):
        headers = {'Authorization': 'Bearer {}'.format(
            st.session_state.access_token)}
        url = self.conf['fastapi']['url']['users_me']
        res = requests.get(url, headers=headers)
        st.info(res.content)

    def register(self, params):
        headers = {'Authorization': 'Bearer {}'.format(
            st.session_state.access_token)}
        url = self.conf['fastapi']['url']['register']
        res = requests.post(url, params, headers=headers)
        st.info(res.content)
