import streamlit as st
import json
import requests
import register
import marketing
import top

pages = {"top": top, "register": register, "marketing": marketing}

selection = st.sidebar.selectbox("select", list(pages.keys()))
page = pages[selection]
page.app()
