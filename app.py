import streamlit as st

from scripts.utils import load_metadata, read_flipside
from scripts.talk import Downloader

from pages.single_moonbird import single_moonbird_page
from pages.traits import trait_page as trait_page_old
from pages.moonbird_main import main_page
from pages.moonbird_trait import trait_page
from pages.moonbird_attribute import attribute_page
from pages.utils import get_traits

st.set_page_config(page_title="FlipsideCrypto <3 Moonbirds", layout="wide")

downloader = Downloader()
metadata = load_metadata()
traits = get_traits(metadata)
traits = ["All"] + traits.tolist()
df = read_flipside(
    url="https://api.flipsidecrypto.com/api/v2/queries/0b98038f-94ae-4d7c-92e7-be7a83758a2b/data/latest"
)

st.sidebar.markdown(
    """ # Moonbirds
## Rare Traits vs Price
This dashboard for Flipside looks at 

1. What Moon Bird traits are rarest

2. How have different traits performed with buyers and sellers?
"""
)

radio_choice = st.sidebar.radio(
    "Choose", ("Main", "Traits", "Traits_old", "Moonbirds"), index=0
)
if radio_choice == "Moonbirds":
    single_moonbird_page(downloader, metadata, df)
elif radio_choice == "Traits":
    trait_choice = st.sidebar.radio("Choose Trait", traits, index=0)
    st.markdown(
        f"""## Selected trait: {trait_choice}

The unusual is interesting. Degree of rarity and probability are essentially identical concepts. [Weaver, 1948](https://www.jstor.org/stable/22339)

Here we order the the traits and their attributes, based on the probability they occur. 
The smaller the probability of an trait/attribute to occur thus the rarer the trait/attribute. 
The traits with less probable tend to be priced higher than the more common traits
"""
    )
    data_prob = metadata.drop_duplicates(subset=["trait_type"]).sort_values(
        by="trait_type_rarity"
    )
    idx = data_prob["trait_type"].tolist()
    data_combined = metadata.merge(df, left_on="name", right_on="TOKENID", how="left")

    if trait_choice == "All":
        trait_page(data_prob, idx, data_combined, trait_choice, downloader)
    else:
        attribute_page(metadata, data_combined, trait_choice, downloader)
elif radio_choice == "Traits_old":
    trait_page_old(downloader, metadata, df)
elif radio_choice == "Main":
    main_page(df, downloader)
else:
    st.write("shouldn't be here")
