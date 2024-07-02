import os
import streamlit as st
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings
import pymongo
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import pprint




os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')
llm = ChatGroq(temperature=0.7,model="llama3-70b-8192")

prompt_template = """You are a helpful assistant. Use the provided context to answer the question at the end. Prioritize the answers based on the most recent publish date.

{context}

Question: {question}
"""

def format_docs(docs)-> str:
    return "\n\n".join(doc.page_content for doc in docs)

def get_answer(question)-> str:
    try:
        print(question)
        client = pymongo.MongoClient(**st.secrets["mongo"])
        print(client)
        embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L12-v2")
        docsearch=MongoDBAtlasVectorSearch.from_connection_string("mongodb+srv://leodevelopergcp:FVpcYt0S8rkZN24R@youtube.o94da0r.mongodb.net/?retryWrites=true&w=majority&appName=Youtube",
                                                                  "Youtube.ZeeshanUsmaniYouTube",embedding_function,index_name="ZeeshanUsmani_Vector_Index")
        
        qa_retriever = docsearch.as_retriever(search_type="similarity",search_kwargs={"k": 4,"post_filter_pipeline": [{"$limit": 25}]})
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        qa = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff", retriever=qa_retriever, return_source_documents=True, 
                                 chain_type_kwargs={"prompt": PROMPT}
                                 )
        
        docs=qa(question)
        pprint.pprint(docs["result"])
        pprint.pprint(docs['source_documents'][0].metadata)
        print("--------------------------------------")
        rag_chain = ({"context": qa_retriever | format_docs, "question": RunnablePassthrough()} 
                     | PROMPT 
                     | llm
                     | StrOutputParser())
        
        #respone=rag_chain.invoke(question)
        #print(respone)
        #docs = docsearch.similarity_search(question)
        #print(question)
        #print(docs)
        #print(docs[0].metadata)
        #print(docs[0].page_content)
        return docs["result"]
    except Exception as e:
        return print(f"Error{e}")



