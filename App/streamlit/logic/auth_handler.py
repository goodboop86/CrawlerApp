
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

    def signup(self):
        url = self.conf['fastapi']['url']['signup']
        request = json.dumps(
            {"address": self.address, "password": self.password})
        response = requests.post(url, request)
        if response.ok:
            st.info(f"{response.text}")
        else:
            st.error(f"{response.text}")

    def oauth2_signin(self):
        url = self.conf['fastapi']['url']['oauth2_signin']
        params = {"username": self.address,
                  "password": self.password, "grant_type": "password"}
        response = requests.post(url, params)
        if response.ok:
            st.info(f"{response.text}")
            st.session_state.access_token = response.json()["access_token"]
        else:
            st.error(f"{response.text}")

    def signin(self):
        response = self._auth()

        if response.ok:
            st.info(f"{response.text}")
            if response.json()["status"] == "success":
                self._session_signin()
        else:
            st.error(f"{response.text}")

    def signout(self):
        self._session_signout()

    def update_password(self):
        response = self._auth()

    def update_context(self):
        response = self._auth()

    def _auth(self):
        url = self.conf['fastapi']['url']['signin']
        request = json.dumps(
            {"address": self.address, "password": self.password})
        response = requests.post(url, request)
        return response

    def _session_signin(self):
        st.session_state.is_signedin = True
        st.session_state.address = self.address

    def _session_signout(self):
        st.session_state.is_signedin = False
