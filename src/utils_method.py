import streamlit as st

# Function to extract query parameters
def get_query_params():
    query_params = st.query_params.to_dict()
    return query_params