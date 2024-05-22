import streamlit as st
from langchain import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain_community.embeddings import SentenceTransformerEmbeddings
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant

local_llm = "mistral-7b-v0.1.Q4_K_M.gguf"  # Make sure the model path is correct for your system!
llm = LlamaCpp(model_path=local_llm, temperature=0.3, max_tokens=2048, top_p=1)
print("LLM Initialized....")

prompt_template = """Use the following pieces of information to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer. Context: {context} Question: {question} Only return the helpful answer. Answer must be detailed and well explained. Helpful answer: """

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
url = "http://localhost:6333"
client = QdrantClient(url=url, prefer_grpc=False)
db = Qdrant(client=client, embeddings=embeddings, collection_name="vector_db")
prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
retriever = db.as_retriever(search_kwargs={"k": 1})

def qa_function(query):
    chain_type_kwargs = {"prompt": prompt}
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True, chain_type_kwargs=chain_type_kwargs, verbose=True)
    response = qa(query)
    answer = response['result']
    source_document = response['source_documents'][0].page_content
    doc = response['source_documents'][0].metadata['source']
    return answer, source_document, doc

st.title("Latest Tech News Q&A System")
st.write("Ask questions about the provided context.")

query = st.text_area("Enter your query")
if st.button("Submit"):
    answer, source_document, doc = qa_function(query)
    st.subheader("Answer")
    st.write(answer)
    st.subheader("Source Document")
    st.write(source_document)
    st.subheader("Source")
    st.write(doc)