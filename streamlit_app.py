import streamlit as st
import requests

st.title("AI Research Paper Assistant")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file and st.button("Process PDF"):

    response = requests.post(
        "http://127.0.0.1:5000/upload",
        files={
            "file": uploaded_file
        }
    )

    
    if response.status_code == 200:
        result = response.json()
        st.session_state.uploaded_file = uploaded_file.name

        st.success(result["message"])

        st.write("Pages:", result["pages"])
        st.write("Chunks:", result["chunks"])
    else:
        st.error("PDF processing failed")

question = st.text_input("Ask a question about the document")

if st.button("Ask"):
    if question:
        response = requests.post(
            "http://127.0.0.1:5000/ask",
            json={"question": question}
        )
        result = response.json()
        st.subheader("Answer")
        st.write(result["answer"])

        st.subheader("Sources")
        for page in result["sources"]:
            st.write(f"Page: {page}")