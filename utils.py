import requests
import fitz

def get_all_text_content(pdf, ret_type="str"):
    text_list = []
    text_str = ""
    for i in range(len(pdf)):
        text_list.append(pdf.get_page_text(i))
        text_str += "\n"+pdf.get_page_text(i)
        
    if ret_type == "str":
        return text_str
    return text_list

def add_meta(docs, metadata:dict):
    for doc in docs:
        doc.metadata = metadata
        
    return docs

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_pdf_text_from_url(url):
    response = requests.get(url)
    with open('temp.pdf', 'wb') as f:
        f.write(response.content)
        
    pdf = fitz.open("temp.pdf")
    full_text = get_all_text_content(pdf)
    
    return full_text