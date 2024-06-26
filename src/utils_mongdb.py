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

    # Aggregation pipeline to group by title, include publish_date and thumbnail_url, and paginate results
    pipeline = [
    {
        '$match': {
            'title': {'$ne': 'None'}
        }
    },
    {
        '$group': {
            '_id': {
                'title': '$title',
                'thumbnail': '$thumbnail',
                'publish_date': '$publish_date',
                'source': '$source',
                'youtubelink':'$youtubelink'
            },
            'count': {'$sum': 1}
        }
    },
    {
        '$project': {
            '_id': 0,
            'title': '$_id.title',
            'thumbnail': '$_id.thumbnail',
            'publish_date': '$_id.publish_date',
            'source': '$_id.source',
            'youtubelink':'$_id.youtubelink',
            'count': 1
        }
    },
    {
        '$sort': {
            'publish_date': -1  # Sort by publish_date in ascending order. Use -1 for descending order.
        }
    },
    {
        '$skip': skip
    },
    {
        '$limit': page_size
    }
]

    #cursor = collection.find({}, {'text':0,'embedding':0}).skip(skip).limit(page_size)
    cursor = collection.aggregate(pipeline)
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