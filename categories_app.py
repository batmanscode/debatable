"""
streamlit app to create or recreate the categories

run with:
streamlit run categories_app.py --server.enableCORS false --server.enableXsrfProtection false
"""

import streamlit as st
import asyncio

from debatable import categorise_input
from db_utils import get_email, get_product_context


st.set_page_config(page_title="Redo Categories", page_icon="💡", initial_sidebar_state="auto", layout="wide")

st.title("Redo Categories 💡")
st.write(
    """
    some utils to create or recreate the categories.
    """
)
st.markdown("---")

with st.form("categories_form"):
    key = st.text_input("Enter the key of the report you want to rewrite")

    rewrite_button = st.form_submit_button("Categorise", type="primary")

if rewrite_button:
    # get the email and product context
    email = get_email(key=key)
    if email is None:
        raise ValueError(f"no report found for key {key}")

    product_context = get_product_context(key=key)

    # categorise the input
    # save the categories
    c = asyncio.run(categorise_input(
        email=email,
        product_context=product_context,
        key=key
        ))
    
    # show the categories
    st.write(":blue[categories]")
    st.write(c)

    col1, col2 = st.columns(2)

    with col1:
        st.write(":blue[email]")
        st.write(email)

    with col2:
        st.write(":blue[product context]")
        st.write(product_context)