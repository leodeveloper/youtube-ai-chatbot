import streamlit as st
import os
import pymongo
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
cloudmongo = os.environ.get("cloudmongodb")
    # Establish a connection to the MongoDB server
client = pymongo.MongoClient(**st.secrets["mongo"])

# Select the database and collection
db = client["Youtube"]


# Function to fetch paginated results
def fetch_paginated_results(collection, page_size, page_number):
    collection = db[collection]
    """
    Fetches paginated results from the collection.

    Parameters:
    collection (pymongo.collection.Collection): The MongoDB collection.
    page_size (int): Number of documents per page.
    page_number (int): The page number to retrieve.

    Returns:
    list: A list of documents from the specified page.
    """
    skip = page_size * (page_number - 1)
    cursor = collection.find().skip(skip).limit(page_size)
    results = list(cursor)
    return results

# Example usage
page_size = 10
page_number = 1

""" while True:
    results = fetch_paginated_results(collection, page_size, page_number)
    if not results:
        break
    for doc in results:
        print(doc)
    page_number += 1 """
    # To stop after a certain number of pages, add a condition here
    # if page_number > some_max_page_number:
    #     break