from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
'''
pdf_path = "data/Attention is all you need.pdf"

loader = PyPDFLoader(pdf_path)
documents = loader.load()
'''
def ingest_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print("Pages:", len(documents))
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )

    chunks = splitter.split_documents(documents)
    print("Chunks:", len(chunks))

    print("\nFirst chunk")
    print(chunks[0].page_content)

    # 3. Convert chunks into embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    print("Creating embeddings...")

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    # 4. Save vector database locally
    vectorstore.save_local("faiss_index")


    print("Vector database created")

    return len(documents), len(chunks)


