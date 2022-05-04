import streamlit as st
import matplotlib.cm as cm
from matplotlib.colors import rgb2hex
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def get_image(imageid):
    pass


def get_most_recent_price(df, idx=None):
    df = df.sort_values("BLOCK_TIMESTAMP")
    df = df.drop_duplicates(subset=["TOKENID"], keep="last").sort_values(
        "BLOCK_TIMESTAMP", ascending=False
    )
    if idx is not None:
        if type(idx) != type(list()):
            df = df.query("TOKENID==@idx")
        else:
            df = df.query("TOKENID in @idx")
        if df.shape[0] > 0:
            return df["PRICE"].values[0]
        else:
            return 0
    else:
        return df


def number_of_times_sold(df, idx=None):
    df = df.groupby("TOKENID")["BLOCK_TIMESTAMP"].nunique()
    df.name = "TIMES_SOLD"
    if idx is not None:
        if type(idx) == type(list()):
            new_idx = [i for i in idx if i in df.index]
            if len(new_idx) > 0:
                df = df.reindex(idx, axis=0).fillna(0)
            else:
                df = 0
        else:
            if idx in df.index:
                df = df.reindex(idx, axis=0).fillna(0)
            else:
                df = 0
    return df.astype("int").sort_values(ascending=False)


def filter_data(df, idx=None):
    if idx is not None:
        if "name" in df.columns:
            if type(idx) != type(list()):
                df = df.query("name==@idx")
            else:
                df = df.query("name in @idx")
        else:
            if type(idx) != type(list()):
                df = df.query("TOKENID==@idx")
            else:
                df = df.query("TOKENID in @idx")
    return df


def get_traits(df):
    return df["trait_type"].unique()


def get_attributes(trait, df):
    return df.query("trait_type==@trait")["value"].unique()


def get_color(val, min_val, max_val, cmap="magma_r"):
    # note not normalized values
    val = (val - min_val) / (max_val + 0.01 - min_val)
    cmap = cm.get_cmap(cmap)
    return rgb2hex(cmap(val))


@st.cache()
def get_token_prices(df):
    token_prices = {}

    for token_id in df["TOKENID"].unique():
        test = df.query("TOKENID==@token_id")[
            ["BLOCK_TIMESTAMP", "PRICE", "TOKENID"]
        ].sort_values("BLOCK_TIMESTAMP")

        token_prices[token_id] = {
            "price": get_all_transaction_diffs(test),
            "count": test.shape[0],
        }
    token_prices = pd.DataFrame.from_dict(token_prices, orient="index")
    return token_prices


@st.cache()
def get_price_data(data_combined, idx, trait=True):
    if trait:
        grouper = "trait_type"
    else:
        grouper = "value"
    return data_combined.groupby(grouper)["PRICE"].mean().loc[idx].reset_index()


@st.cache()
def get_price_data_buy_sell(data_combined, idx, trait=True):
    # data = data_combined  # .groupby("trait_type")
    if trait:
        grouper = "trait_type"
    else:
        grouper = "value"

    data = (
        data_combined.groupby(grouper)["PRICE"].sum()
        / data_combined.groupby(grouper)["PRICE"].count()
    )
    return data.loc[idx].reset_index()


@st.cache()
def get_number_bought(data_combined, idx, trait=True):
    if trait:
        grouper = "trait_type"
    else:
        grouper = "value"
    return (
        data_combined.dropna(subset=["TX_HASH"])
        .groupby(grouper)["TX_HASH"]
        .count()
        .loc[idx]
        .reset_index()
    )


@st.cache()
def get_unique_number_bought(data_combined, idx, trait=True):
    if trait:
        grouper = "trait_type"
    else:
        grouper = "value"
    return (
        data_combined.dropna(subset=["TX_HASH"])
        .groupby(grouper)["name"]
        .nunique()
        .loc[idx]
        .reset_index()
    )


def get_all_transaction_diffs(test):
    return (test["PRICE"].shift(-1) - test["PRICE"]).sum() + (
        test["PRICE"].iloc[0] - 2.5
    )


def plot_bar(
    plot_data,
    x="trait_type",
    y="trait_type_rarity",
    title="Rarity via Probability",
    yaxis_title="Probability",
    xaxis_title="Trait",
):
    fig = px.bar(plot_data, x=x, y=y)
    fig.update_layout(title=title, yaxis_title=yaxis_title, xaxis_title=xaxis_title)
    return fig


def get_median_price_data_full(data):
    data.index = data["BLOCK_TIMESTAMP"]
    # data = data.groupby("trait_type")["PRICE"].mean().loc[idx]
    x = data.resample("d")["PRICE"].median().reset_index()
    y = x["PRICE"].tolist()
    x = x["BLOCK_TIMESTAMP"].tolist()
    return x, y


def plot_main_price(x, y, name="All traits", fig=None):
    if fig is None:
        fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            hovertemplate="Median Price:<br>" + "%{x}<br>" + "%{y:.2f} ETH<br>",
            name=name,
        )
    )
    return fig


def plot_single_price(
    x, y, text, val, name="All traits", max_val=1, min_val=0, fig=None
):
    if fig is None:
        fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            text=text,
            marker={"color": get_color(val, min_val, max_val)},
            # fill='tozeroy',
            hovertemplate="ID: %{text}<br>" + "%{x}<br>" + "Sold for %{y:.2f} ETH<br>",
            name=name,
        )
    )
    return fig
