import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def parse_df(df):

    data = df.sort_values("BLOCK_TIMESTAMP")
    data.index = data["BLOCK_TIMESTAMP"]
    mod_data = data.resample("d")["PRICE"].sum().to_frame("PRICE")
    mod_data = mod_data.join(data.resample("d")["TX_HASH"].count().to_frame("COUNTS"))
    mod_data = mod_data.join(
        data.resample("d")["CREATOR_FEE"].sum().to_frame("CREATOR_FEE")
    )
    mod_data = mod_data.sort_index().cumsum().reset_index()
    return mod_data


def plot_area(
    x,
    y,
    name="Total Number of Sales",
    ylabel="ETH",
    xlabel="Date",
    title="Total Number of Sales",
    fig=None,
):
    if fig is None:
        fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            fill="tozeroy",
            hovertemplate="<b>%{x}</b><br>" + "%{y}<br>",
            name=name,
        )
    )
    fig.update_layout(
        title=title,
        yaxis_title=ylabel,
        xaxis_title=xlabel,
    )
    return fig


def main_page(df, downloader):

    data = parse_df(df)

    # table
    number = 6
    st.markdown(f"### {number} Recent Buys")
    cols = ["BLOCK_TIMESTAMP", "TOKENID", "PRICE", "TX_HASH"]
    s = (
        df.sort_values("BLOCK_TIMESTAMP", ascending=False)
        .reset_index(drop=True)
        .loc[: number - 1, cols]
    )
    # st.dataframe(df)
    cols = st.columns(number)
    for i, ser in s.iterrows():
        downloaded = downloader.get_metadata(ser["TOKENID"])
        image_url = downloaded["image"]
        caption = f"""{ser['BLOCK_TIMESTAMP']}   
Moonbird: {ser['TOKENID']}  
Price: {ser['PRICE']} ETH  
[etherscan](https://etherscan.io/tx/{ser['TX_HASH']})"""
        with cols[i]:
            st.image(image_url)
            st.markdown(caption)

    # images
    st.markdown("### General Price Data")
    left, right = st.columns(2)
    with left:
        price_fig = plot_area(
            x=data["BLOCK_TIMESTAMP"].tolist(),
            y=data["PRICE"].tolist(),
            name="Total Number of ETH used for buying",
            title="Total Number of ETH used for buying",
            ylabel="ETH",
            xlabel="Date",
        )
        st.plotly_chart(price_fig, use_container_width=True)
    with right:
        count_fig = plot_area(
            x=data["BLOCK_TIMESTAMP"].tolist(),
            y=data["COUNTS"].tolist(),
            name="Total Number of Sales",
            title="Total Number of Sales",
            ylabel="Number of Sales",
            xlabel="Date",
        )
        st.plotly_chart(count_fig, use_container_width=True)
    with left:
        creator_fig = plot_area(
            x=data["BLOCK_TIMESTAMP"].tolist(),
            y=data["CREATOR_FEE"].tolist(),
            name="Creator Fee",
            title="Creator Fee",
            ylabel="ETH",
            xlabel="Date",
        )
        st.plotly_chart(creator_fig, use_container_width=True)
    with right:
        platform_fig = go.Figure()
        for name in df["PLATFORM_NAME"].unique():
            data1 = df.query("PLATFORM_NAME==@name")
            data1 = data1.sort_values("BLOCK_TIMESTAMP")[
                ["BLOCK_TIMESTAMP", "PLATFORM_FEE"]
            ]
            platform_fig = plot_area(
                x=data1["BLOCK_TIMESTAMP"].tolist(),
                y=data1["PLATFORM_FEE"].cumsum().tolist(),
                name=name,
                title="Platform Fee",
                ylabel="ETH",
                xlabel="Date",
                fig=platform_fig,
            )

        st.plotly_chart(platform_fig, use_container_width=True)

    # extra
    st.markdown("### Necessary Details")
    left, right = st.columns(2)
    with left:
        st.markdown(
            """_Under The Hood_:
- Price data queried from Flipside https://flipsidecrypto.xyz/.
- Metadata + Images directly from the MoonBirds IPFS.
- Platform: Streamlit"""
        )
    with right:
        st.markdown(
            """
_Relevant Information_
- https://moonbirds.xyz
- Total Amount: 10,000 Moonbirds
- Mint Price: 2.5 ETH
- The Flipside Bounty: https://flipsidecrypto.xyz/drops/6PKPsLgpeTu8GPhTMqAflv
- Etherscan: https://etherscan.io/token/0x23581767a106ae21c074b2276D25e5C3e136a68b
- Find me on Discord: kipto(🧢,🧢)#1822"""
        )
