import streamlit as st 

from .utils import filter_data, get_most_recent_price, number_of_times_sold

def single_moonbird_page(downloader, metadata, df):
    left,middle,right = st.columns([3,6,6])
    selected = st.number_input('Select Moonbird',
                            min_value=0,
                            max_value=10000,
                            value=0)
    selected = selected if selected!=0 else None
    print_selected = selected if selected is not None else 'all'

    st.subheader(f'Showing {print_selected}')
    if selected is not None:
        downloaded = downloader.get_metadata(selected)
        
        st.image(downloaded['image'],
                caption=downloaded['name'],
                width=128
                )

    with right:
        st.write('full price data')
        st.dataframe(filter_data(df,selected))
    with middle:
        st.write('most recent prices')
        st.write(get_most_recent_price(df,selected))
    with left:
        st.write('number of times sold')
        st.write(number_of_times_sold(df,selected))
        
    st.dataframe(filter_data(metadata,selected)[['trait_type','value','trait_type_rarity','trait_attribute_rarity']]) 

