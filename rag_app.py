import streamlit as st
from llm_helper import *
from indexer import PDFIndexer
from utils import *
from streamlit_pdf_viewer import pdf_viewer
st.set_page_config(layout='wide')

if "initialized" not in st.session_state:
    st.session_state["messages"] = []               # Human LLM interactions
    st.session_state["indexer"] = PDFIndexer()
    st.session_state["initialized"] = True  
    st.session_state['binary_data'] = None          # Binary data of PDF, for rendering
    st.session_state['page'] = 1                    # Which page of PDF to show
    st.session_state["state"] =  0                  # Overall state of UI

def render_pdf():
    with open("temp.pdf", 'rb') as fp:
        st.session_state['binary_data'] = fp.read()
    pdf_container = st.container(border=True, height=500)
    with pdf_container:
        pdf_viewer(input=st.session_state['binary_data'], pages_to_render=[st.session_state['page']], resolution_boost=2)

with st.sidebar:
    url = st.text_input("PDF URL", "https://arxiv.org/pdf/1810.04805")
    interact = st.button("Interact with PDF")
col1, col2 = st.columns([3,2])

if interact:
    full_text = get_pdf_text_from_url(url)
    st.session_state["indexer"].index_to_db(full_text, url)
    st.session_state["state"] = 1
    with st.sidebar:
        st.info("PDF processed")
    
if st.session_state["state"] == 1:
    with col1:
        back_col, _, next_col = st.columns([1, 5, 1])
        with next_col:
            if st.button("Next"):
                st.session_state['page'] += 1
        with back_col:
            if st.button("Back"):
                st.session_state['page'] -= 1
        render_pdf()

if st.session_state["state"] == 1:
    with col2:
        messages = st.container(height=500)
        for item in st.session_state["messages"][-3:]:
            messages.chat_message("user").write(item['user'])
            messages.chat_message("assistant").write(item['assistant'])
            
        if query := st.chat_input("Ask anything"):
            messages.chat_message("user").write(query)
            
            retriever = st.session_state["indexer"].get_retriever(url)
            retrieved_docs = retriever.invoke(query)
            context = format_docs(retrieved_docs)
            response = query_with_context(context, query)
            
            messages.chat_message("assistant").write(response)
            
            st.session_state["messages"].append({
                "user" : query,
                "assistant" : response
            })
                
            