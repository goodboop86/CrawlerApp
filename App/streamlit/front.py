import streamlit as st
import json
import requests

def main():

    #import pdb;pdb.set_trace()
    
    with open("setting.json") as f:
        conf = json.load(f)
    #link = '[Hello World]({})'.format(conf['fastapi']['url']+"/item?foo=Foo&bar=Bar")

    st.title('Hello World')
    #st.markdown(link, unsafe_allow_html=True)

    url = st.text_input('url', conf['fastapi']['url']+"/item")
    foo = st.text_input('foo', "Foo")
    bar = st.text_input('bar', "Bar")

    responce = requests.get(url, {"foo":foo, "bar":bar})
    #import pdb; pdb.set_trace()
    st.write(responce.content)



if __name__ == '__main__':
    main()
