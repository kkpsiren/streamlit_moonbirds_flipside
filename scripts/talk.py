import requests
import streamlit as st

@st.cache()
class Downloader:
    def __init__(self,
                 url = 'https://live---metadata-5covpqijaa-uc.a.run.app/metadata/'):
        self.url = url
    
    def get_metadata(self, idx):
        r = requests.get(''.join([self.url,str(idx)]))
        return r.json()

