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
