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
    query_params = get_query_params()
    if query_params:
        if "channelName" in st.query_params:
            youtubechannelname = st.query_params["channelName"]
            # Streamlit UI
            st.title(f"Youtube Channel {youtubechannelname}")

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
                    youtubeurl=f"https://www.youtube.com/watch?v={doc['source']}&src_lang=hi&target_lang=en"
                    st.image(doc['thumbnail'], use_column_width=True)
                    st.write(f"<div class='truncate-title'>{doc['title']}</div>", unsafe_allow_html=True)
                    #st.write(f"Author: {doc['author']}")
                    st.write(f"Published on: {doc['publish_date']} - <a href='https://leodeveloper2000-youtubetranslationapi.hf.space/generate/?youtubeurl={youtubeurl}'>Translate</a>", unsafe_allow_html=True)
                    #st.write(f"Views: {doc['view_count']}")
                    #st.write(f"Description: {doc['description']}")
        else:
            st.error("Please provide a valid channel name")

    else:
        st.write("Please provide a valid channel name")

if __name__ == "__main__":
    main()
