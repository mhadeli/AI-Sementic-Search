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

st.set_page_config(page_title="Semantic Search", page_icon="⚡")
st.markdown("<h1 style='font-style: italic;'>"
            "<span style='color: #F55F0E;'>S</span>emantic "
            "<span style='color: #F55F0E;'>S</span>earch "
            "<span style='color: #F55F0E;'>E</span>ngine"
            "</h1>", unsafe_allow_html=True)

st.write("")
st.write("")
st.sidebar.title("Welcome !")
st.sidebar.write("")
st.sidebar.subheader("ABOUT:")
st.sidebar.markdown("<h3 style='font-weight: normal;'>This is Semantic Search Engine powered by Pinecone's Vector Database and OpenAI's LLM Model. <br><br>"
                    "Just Upload a file and ask any query regarding it to get your answer within seconds!!</h3>",unsafe_allow_html=True)
st.sidebar.write("")
if "submit" not in st.session_state:
    st.session_state["submit"] = False

def clear_submit():
    st.session_state["submit"] = False
def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key

@st.cache_data(show_spinner=True)
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
def vectors(_data, OPENAI_API_KEY):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    PINECONE_API_KEY = st.secrets.get("PINECONE_API_KEY")
    PINECONE_API_ENV = st.secrets.get("PINECONE_API_ENV")
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name="sementicsearch")
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")
    return docsearch, chain


@st.cache_data(show_spinner=False)
def find_ans(query,_data):
    docs = docsearch.similarity_search(query)
    ans = chain.run(input_documents=docs, question=query)
    return ans

OPENAI_API_KEY=st.sidebar.text_input(
            "Enter your OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",
            value=st.session_state.get("OPENAI_API_KEY", ""),)
if OPENAI_API_KEY:
    set_openai_api_key(OPENAI_API_KEY)

st.write("<h5 style= padding-bottom:0px; margin-bottom: 0px>Upload Document (pdf/ docx/ txt).</h5>",unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "",
    type=["pdf", "docx", "txt"],
    help="Scanned documents are not supported yet!",
    on_change=clear_submit,
)
st.write("")
st.write("")
st.write("")
if uploaded_file:
    data = extract_text(uploaded_file)
    docsearch, chain = vectors(data,OPENAI_API_KEY)

st.write("<h5 style= padding-bottom:0px; margin-bottom: 0px>Ask your question related to the document: </h5>",unsafe_allow_html=True)
ques = st.text_area("", on_change=clear_submit)
st.markdown(
    """
    <style>
    textarea {
        font-size: 1.25rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

button = st.button("Submit")
if button and len(ques) >= 5:
    if not OPENAI_API_KEY:
        st.warning("Please enter your OpenAI API Key in the sidebar.")
    else:
        with st.spinner("Finding the most Precise Answer ⏳... "):
            a = find_ans(ques, data)
        st.markdown(f"<h5 style='font-family: Roboto; font-weight: normal;'>{a}</h5>", unsafe_allow_html=True)




