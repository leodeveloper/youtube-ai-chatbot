import streamlit as st
from src.utils_method import get_query_params
from src.utils_mongdb import fetch_paginated_results
from src.utils_qa import get_answer
from datetime import datetime
import os
os.environ["TOKENIZERS_PARALLELISM"] = "true"

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

            st.write(f"Ask any question from {youtubechannelname}")
            question = st.text_input("Please write a question here", placeholder="write question here")
            if question:
                with st.spinner("please wait....."):
                    answer,sourcedocs = get_answer(question,f"Youtube.{youtubechannelname}",f"{youtubechannelname}_Vector_Index")
                    st.write(answer)
                    if sourcedocs:
                        for sourcedoc in sourcedocs:
                            st.write(sourcedoc.metadata['title'])
                            st.write(sourcedoc.metadata['youtube_url'])
                            st.image(sourcedoc.metadata['thumbnail'],width=50,use_column_width=True)
                            st.write(sourcedoc.metadata['publish_date'])
            
            st.caption("Question answer powered by Groq Api")
            # Parameters for pagination
            page_size = st.sidebar.number_input("Page Size", min_value=1, max_value=10, value=6)
            page_number = st.sidebar.number_input("Page Number", min_value=1, value=1,key="pageNumber")
            searchvideo = st.sidebar.text_input("Search video")
            if searchvideo:
                page_number=1
            # Fetch paginated results
            results,total_count = fetch_paginated_results(youtubechannelname,page_size, page_number,searchvideo)
            st.info(f"Total videos {total_count}, Page {page_number}")
            # Display results in a grid
            cols = st.columns(3)  # Adjust the number of columns as needed

            for idx, doc in enumerate(results):
                col = cols[idx % len(cols)]
                with col:
                    youtubeurlen=f"https://www.youtube.com/watch?v={doc['source']}&src_lang=hi&target_lang=en"
                    youtubeurlit=f"https://www.youtube.com/watch?v={doc['source']}&src_lang=hi&target_lang=it"
                    youtubeurlur=f"https://www.youtube.com/watch?v={doc['source']}&src_lang=hi&target_lang=ur"
                    youtubeurlfr=f"https://www.youtube.com/watch?v={doc['source']}&src_lang=hi&target_lang=fr"
                    st.image(doc['thumbnail'], use_column_width=True)
                    st.write(f"<div class='truncate-title'>{doc['title']}</div>", unsafe_allow_html=True)
                    #st.write(f"Author: {doc['author']}")
                    st.write(f"Published on: {doc['publish_date']} - <a href='https://leodeveloper2000-youtubetranslationapi.hf.space/generate/?youtubeurl={youtubeurlen}'>EN</a> <a href='https://leodeveloper2000-youtubetranslationapi.hf.space/generate/?youtubeurl={youtubeurlur}'>Ur</a>", unsafe_allow_html=True)
                    #st.write(f"Views: {doc['view_count']}")
                    #st.write(f"Description: {doc['description']}")
        else:
            st.error("Please provide a valid channel name")

    else:
        st.write("Please provide a valid channel name")

if __name__ == "__main__":
    main()
