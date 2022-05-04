import pandas as pd
import requests

import streamlit as st

@st.cache()
def read_flipside(url):
    r = requests.get(url)
    r = r.json()
    df =  pd.DataFrame(r).sort_values('BLOCK_TIMESTAMP',ascending=False)
    df['BLOCK_TIMESTAMP'] = pd.to_datetime(df['BLOCK_TIMESTAMP'])
    df['TOKENID'] = df['TOKENID'].astype('int')
    return df

@st.cache()
def load_metadata(path='data/metadata.hdf',key='df'):
    return pd.read_hdf(path,key=key)
