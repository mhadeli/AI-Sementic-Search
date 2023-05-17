from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from docx import Document
import streamlit as st
import pinecone
import os

st.title("Semantic Search Engine")
st.write("")
st.write("")

if "submit" not in st.session_state:
    st.session_state["submit"] = False

def clear_submit():
    st.session_state["submit"] = False

@st.cache_data(show_spinner=False)
def extract_text(uploaded_file):
    file_path = os.path.join(os.getcwd(), uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == ".pdf":
        loader = PyPDFLoader(file_path)
        data = loader.load()
    elif file_extension == ".docx":
        doc = Document(file_path)
        data = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    elif file_extension == ".txt":
        loader = TextLoader(file_path)
        data = loader.load()
    else:
        st.error("Unsupported file format. Only pdf, docx, and txt files are supported.")
        return None
    return data

@st.cache_resource(show_spinner=False)
def vectors(_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
    PINECONE_API_ENV = st.secrets["PINECONE_API_ENV"]
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name="sementicsearch")
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")
    return docsearch,chain

@st.cache_data(show_spinner=False)
def find_ans(query,_data):
    docs = docsearch.similarity_search(query)
    ans = chain.run(input_documents=docs, question=query)
    return ans

uploaded_file = st.file_uploader(
    "Upload a pdf, docx, or txt file.",
    type=["pdf", "docx", "txt"],
    help="Scanned documents are not supported yet!",
    on_change=clear_submit,
)

if uploaded_file:
    data = extract_text(uploaded_file)
    docsearch, chain = vectors(data)

ques = st.text_area("Ask your question related to the document: ", on_change=clear_submit)

button = st.button("Submit")
if button and len(ques) >=5:
    try:
        with st.spinner("Finding the most Precise Answer ⏳... "):
            a = find_ans(ques,data)
        st.write(a)
    except NameError:
        st.warning("Upload a File!")