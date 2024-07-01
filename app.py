import streamlit as st
from src.utils_method import get_query_params
from src.utils_mongdb import fetch_paginated_results
from datetime import datetime

# Add custom CSS to limit the title to two lines
st.markdown("""
    <style>
    .truncate-title {
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    </style>
    """, unsafe_allow_html=True)

# Main function to run the app
def main() -> None:
    youtubechannelname="ZeeshanUsmaniYouTube"
    st.title("Query String Example")
    query_params = get_query_params()
    
    if query_params:
        st.write("Query parameters:")
        for key, value in query_params.items():
            st.write(f"{key}: {value}")
    else:
        st.write("No query parameters found.")
    
    # Streamlit UI
    st.title("MongoDB Pagination with Streamlit")

    # Parameters for pagination
    page_size = st.sidebar.number_input("Page Size", min_value=1, max_value=10, value=6)
    page_number = st.sidebar.number_input("Page Number", min_value=1, value=1)

    # Fetch paginated results
    results = fetch_paginated_results(youtubechannelname,page_size, page_number)

    # Display results in a grid
    cols = st.columns(3)  # Adjust the number of columns as needed

    for idx, doc in enumerate(results):
        col = cols[idx % len(cols)]
        with col:
            print(doc)
            st.image(doc['thumbnail'], use_column_width=True)
            st.write(f"<div class='truncate-title'>{doc['title']}</div>", unsafe_allow_html=True)
            #st.write(f"Author: {doc['author']}")
            st.write(f"Published on: {doc['publish_date']} - <a href='https://youtubetranslate.streamlit.app/?source={doc['source']}'>Translate</a>", unsafe_allow_html=True)
            #st.write(f"Views: {doc['view_count']}")
            #st.write(f"Description: {doc['description']}")

    # Add navigation buttons
    col1, col2, col3 = st.columns(3)
    if page_number > 1:
        if col1.button("Previous"):
            st.experimental_set_query_params(page_number=page_number-1)

    if len(results) == page_size:
        if col3.button("Next"):
            st.experimental_set_query_params(page_number=page_number+1)

    # Get the query parameters to set the page number
    query_params = st.experimental_get_query_params()
    if 'page_number' in query_params:
        page_number = int(query_params['page_number'][0])
    else:
        page_number = 1

if __name__ == "__main__":
    main()
