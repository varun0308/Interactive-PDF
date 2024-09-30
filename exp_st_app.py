import streamlit as st
import base64

file = "temp.pdf"

with open(file, "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # base64_pdf = f.read()

# Embedding PDF in HTML
pdf_display = F'<embed id="pdfViewer" src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'

# Displaying File
st.markdown(pdf_display, unsafe_allow_html=True)

# Scroll to and highlight text
html = (f'''
<alert> JS injected... </alert>
<script>
var container = document.getElementById("pdfViewer");
container.scrollTop = container.scrollHeight;
</script>
''')

if st.button("Scroll"):
    st.markdown(html, unsafe_allow_html=True)