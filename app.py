import streamlit as st
from src.utils_method import get_query_params



# Main function to run the app
def main() -> None:
    st.title("Query String Example")
    query_params = get_query_params()
    
    if query_params:
        st.write("Query parameters:")
        for key, value in query_params.items():
            st.write(f"{key}: {value}")
    else:
        st.write("No query parameters found.")

if __name__ == "__main__":
    main()
