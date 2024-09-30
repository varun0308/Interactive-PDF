import streamlit as st
from llm_helper import *
from indexer import PDFIndexer
from utils import *
from streamlit_pdf_viewer import pdf_viewer
import base64

st.set_page_config(layout='wide')

if "initialized" not in st.session_state:
    st.session_state["messages"] = []               # Human-LLM interactions
    st.session_state["indexer"] = PDFIndexer()
    st.session_state["initialized"] = True  
    st.session_state['binary_data'] = None          # Binary data of PDF, for rendering
    st.session_state['page'] = 1                    # Which page of PDF to show
    st.session_state["state"] =  0                  # Overall state of UI

def render_pdf():
    with open("temp.pdf", 'rb') as fp:
        st.session_state['base64_pdf'] = base64.b64encode(fp.read()).decode('utf-8')
    pdf_container = st.container(border=True)
    with pdf_container:
        pdf_display = F'<embed id="pdfViewer" src="data:application/pdf;base64,{st.session_state['base64_pdf']}" width="600" height="500" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)

with st.sidebar:
    url = st.text_input("PDF URL", "https://arxiv.org/pdf/1810.04805")
    interact = st.button("Interact with PDF")
pdf_col, chat_col = st.columns([3,2])

if interact:
    full_text = get_pdf_text_from_url(url)
    st.session_state["indexer"].index_to_db(full_text, url)
    st.session_state["state"] = 1
    with st.sidebar:
        st.info("PDF processed")
    
if st.session_state["state"] == 1:
    with pdf_col:
        render_pdf()

    with chat_col:
        messages = st.container(height=500)
        for item in st.session_state["messages"]:
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
                
            