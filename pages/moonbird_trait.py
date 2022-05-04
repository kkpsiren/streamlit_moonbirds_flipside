import streamlit as st
from random import randint
from .utils import filter_data, get_most_recent_price, number_of_times_sold
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from .utils import *


def trait_page(data_prob, idx, data_combined, trait_choice, downloader):

    # data_price = data_combined.groupby("trait_type")["PRICE"].mean().loc[idx].reset_index()

    left, right = st.columns(2)
    with left:
        fig = plot_bar(
            data_prob,
            x="trait_type",
            y="trait_type_rarity",
            title="Rarity via Probability",
            yaxis_title="Probability",
            xaxis_title="Trait",
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = plot_bar(
            get_price_data(data_combined, idx),
            x="trait_type",
            y="PRICE",
            title="Average Price (ETH)",
            yaxis_title="Average Price (ETH)",
            xaxis_title="Trait",
        )
        st.plotly_chart(fig, use_container_width=True)

    fig = plot_bar(
        # get_price_data_buy_sell(data_change, idx),
        get_price_data_buy_sell(data_combined, idx),
        x="trait_type",
        y="PRICE",
        title="Average Profit Generated (ETH)",
        yaxis_title="Average Price Generated (ETH)",
        xaxis_title="Trait",
    )
    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        fig = plot_bar(
            get_number_bought(data_combined, idx),
            x="trait_type",
            y="TX_HASH",
            title="Number of Sales",
            yaxis_title="Count",
            xaxis_title="Trait",
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = plot_bar(
            get_unique_number_bought(data_combined, idx),
            x="trait_type",
            y="name",
            title="Number of Unique Moonbirds Sold",
            yaxis_title="Count",
            xaxis_title="Trait",
        )
        st.plotly_chart(fig, use_container_width=True)

    # daily price

    x, y = get_median_price_data_full(data_combined)
    fig = plot_main_price(x, y, name="All traits", fig=None)

    # single starts here
    max_val = data_combined["trait_type_rarity"].max() + 0.05
    min_val = data_combined["trait_type_rarity"].min()
    for single_trait in idx:
        selected_data_ = data_combined.query("trait_type==@single_trait")
        val = selected_data_["trait_type_rarity"].iloc[0]
        selected_data_.index = selected_data_["BLOCK_TIMESTAMP"]
        selected_data_ = (
            selected_data_.resample("d")["PRICE"].mean().to_frame("PRICE").reset_index()
        )
        y = selected_data_["PRICE"].tolist()
        x = selected_data_["BLOCK_TIMESTAMP"].tolist()
        text = [single_trait for i in x]
        fig = plot_single_price(
            x,
            y,
            text,
            val,
            name=single_trait,
            max_val=max_val,
            min_val=min_val,
            fig=fig,
        )
    fig.update_layout(
        title=f"Daily Prices for {trait_choice}",
        yaxis_title="ETH",
        xaxis_title="Date",
        hovermode="x",
    )
    st.plotly_chart(fig, use_container_width=True)

    # final

    #    token_prices = get_token_prices(df)
    #    data_change = metadata.merge(
    #        token_prices, left_on="name", right_index=True, how="left"
    #    )


def trait_page2(downloader, metadata, df, trait_choice):
    traits = get_traits(metadata)

    """     
    
    
    selected_trait = st.selectbox('Select Traits',
                            traits)
    
    attributes = get_attributes(selected_trait, metadata)
    
    selected_attribute = st.multiselect('Select Attributes',
                            attributes)
    
    st.subheader(f"{selected_trait}: {', '.join(selected_attribute)}")
    selected_data = metadata.query('trait_type==@selected_trait')
    if len(selected_attribute)>0:
        selected_data = selected_data.query('value in @selected_attribute')
    unique_ids_og = set(selected_data['name'].unique())
    max_len = len(unique_ids_og)
    st.write(f'{max_len} Moonbirds have this trait with these attributes')
    st.write(f'total number of sales {df.shape[0]}')
    st.write('cumulative eth plot of this')

    
    # download three examples
    image_list = []
    image_list_ids = []
    num_images = 7
    b = max_len
    if num_images > max_len:
        num_images = max_len
    unique_ids = unique_ids_og.copy()
    for i in range(num_images):
        selected = randint(a=1,b=b)-1
        chosen = list(unique_ids)[selected]
        downloaded = downloader.get_metadata(chosen)
        image_list.append(downloaded['image'])
        image_list_ids.append(downloaded['name'])
        b = b-1
        unique_ids.remove(chosen)
 

    opts = [int(i[1:]) for i in image_list_ids]

    selected_moonbirds = st.multiselect('Moonbird IDs',unique_ids_og,default=opts) """
    sold = number_of_times_sold(df, selected_moonbirds)
    # recent_prices = get_most_recent_price(df,selected_moonbirds)
    filtered_data = filter_data(df, list(unique_ids_og))
    # filtered_data2 = filter_data(df,list(unique_ids_og)).groupby('BLOCK_TIMESTAMP')['PRICE'].mean()

    # st.write(selected_moonbirds)
    # st.write(unique_ids_og)
    image_list_ids = [
        f"""Moonbird {i} has been sold {sold.loc[int(i[1:])]} times. 
                      Last price is {get_most_recent_price(df,int(i[1:]))} ETH"""
        for i in image_list_ids
    ]

    st.image(image_list, caption=image_list_ids, width=50 * 3)

    # uus
    fig = px.bar(
        metadata.drop_duplicates(subset=["trait_type"]).sort_values(
            by="trait_type_rarity"
        ),
        x="trait_type",
        y="trait_type_rarity",
        title=f"Traits",
    )
    selected_points = plotly_events(fig, click_event=True, hover_event=False)
    if len(selected_points) > 0:
        selected_points = selected_points[0]["x"]
        # st.write(selected_points)
        plot_data = (
            (
                metadata.query("trait_type==@selected_points")["value"].value_counts()
                / 10000
            )
            .sort_values()
            .reset_index()
        )
        # st.write(plot_data)
        plot_data.columns = ["name", "probability"]
        st.write(plot_data)
        # plot_data['inverse_probability'] = 1 - plot_data['probability']

    ll, rr = st.columns([12, 12])
    with ll:
        fig = px.bar(plot_data, x="name", y="probability", title=f"{selected_points}")
        st.plotly_chart(fig, use_container_width=True)
    # fig = px.bar(attr_data.sort_values(by='probability'), x='attribute', y='probability',title=f"Trait: {selected_trait} - probability: {counts['all']['total_amount']/10000:.3f}")
    with rr:
        ##st.dataframe(metadata.query('trait_type==@selected_points')['value'].value_counts())
        # st.dataframe(df)
        # st.dataframe(metadata)
        combined = metadata.merge(df, left_on="name", right_on="TOKENID", how="left")
        # st.dataframe(combined)
        combined_mean = (
            combined.query("trait_type==@selected_points")
            .groupby("value")["PRICE"]
            .mean()
            .loc[plot_data["name"].values]
            .reset_index()
        )
        fig = px.bar(combined_mean, x="value", y="PRICE", title=f"{selected_points}")
        st.plotly_chart(fig, use_container_width=True)

    # st.write('most recent prices')
    # chart = px.area(filtered_data2.reset_index(),x='BLOCK_TIMESTAMP',y='PRICE',hover)

    # counts = {}

    selected_data_ = metadata.query("trait_type==@selected_points")
    selected_attribute_all = plot_data.sort_values("probability")["name"].tolist()
    #    for at in selected_attribute_all:
    #        counts[at] = {}
    #        counts[at]['total_amount'] = selected_data_.query('value==@at').shape[0]
    #        counts[at]['unique_sold'] = 0
    # st.dataframe(selected_data_)
    filtered_data = filter_data(df, selected_data_["name"].unique().tolist())
    # st.dataframe(filtered_data)
    #    counts['all'] = {'unique_sold': selected_data_['name'].nunique(),
    #                        'total_amount': selected_data_.shape[0],
    #                        'val': selected_points
    #                        }

    filtered_data.index = pd.to_datetime(filtered_data["BLOCK_TIMESTAMP"])
    x = filtered_data.resample("d")["PRICE"].median().reset_index()
    y = x["PRICE"].tolist()
    x = x["BLOCK_TIMESTAMP"].tolist()
    chart = go.Figure()
    chart.add_trace(
        go.Scatter(
            x=x,
            y=y,
            # text=text,
            # fill='tozeroy',
            hovertemplate="Median Price:<br>" + "%{x}<br>" + "%{y:.2f} ETH<br>",
            name=f"All traits for {selected_points}",
        )
    )

    if len(selected_attribute_all) > 0:
        for selected_attribute_one in selected_attribute_all:
            val = plot_data.query("name==@selected_attribute_one")["probability"].iloc[
                0
            ]
            max_val = plot_data["probability"].max()
            min_val = plot_data["probability"].min()
            selected_data_ = combined.query("value in @selected_attribute_one")
            filtered_data = filter_data(df, selected_data_["name"].unique().tolist())
            x = filtered_data["BLOCK_TIMESTAMP"].tolist()
            y = filtered_data["PRICE"].tolist()
            text = filtered_data["TOKENID"].tolist()
            chart.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    text=text,
                    marker={"color": get_color(val, min_val, max_val)},
                    # fill='tozeroy',
                    hovertemplate="ID: %{text}<br>"
                    + "%{x}<br>"
                    + "Sold for %{y:.2f} ETH<br>",
                    name=selected_attribute_one,
                )
            )
    chart.update_layout(
        title=f"Daily Prices for {selected_points}", yaxis_title="ETH", hovermode="x"
    )
    st.plotly_chart(chart, use_container_width=True)
    # attr_data = pd.DataFrame([[i,counts[i]['total_amount']] for i in counts.keys() if i !='all'],columns=['attribute','total_amount'])
    # attr_data['probability'] = attr_data['total_amount']/10000
