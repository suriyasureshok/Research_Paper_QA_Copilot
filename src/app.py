import streamlit as st
from data_ingestion.paper_collector import ArxivPaperCollection
from data_ingestion.text_chunker import TextChunker
from data_ingestion.store_data import DataStore
from chat.gemini_client import GeminiQAHandler

# Cache the DataStore to avoid multiple instances
@st.cache_resource
def get_datastore():
    return DataStore()

# Cache the handler
@st.cache_resource
def get_handler(api_key, _datastore, _version=3):
    return GeminiQAHandler(api_key, _datastore)

# Sidebar for navigation
page = st.sidebar.radio("Navigate", ["Paper Collection", "Chat Interface"])

if page == "Paper Collection":
    st.title("📄 Paper Collection")
    st.write("Collect and process research papers from arXiv.")

    datastore = get_datastore()

    with st.form("collection_form"):
        query = st.text_input("Topic/Keyword", value="transformer")
        max_results = st.number_input("Max Results", min_value=1, max_value=20, value=5)
        submitted = st.form_submit_button("Collect Papers")

        if submitted:
            with st.spinner("Collecting and processing papers..."):
                collector = ArxivPaperCollection(query, max_results)
                papers = collector.fetch_papers()
                
                chunker = TextChunker(method='statistical')
                
                total_chunks = 0
                for paper in papers:
                    chunks = chunker.chunk_text(paper['full_text'])
                    datastore.add_chunks(chunks)
                    total_chunks += len(chunks)
                
                st.success(f"Collected {len(papers)} papers and stored {total_chunks} chunks!")
                st.write("Papers collected:")
                for paper in papers:
                    st.write(f"- {paper['title']}")

elif page == "Chat Interface":
    st.title("💬 Chat Interface")
    st.write("Ask questions about the collected research papers.")

    # API Key input
    api_key = st.text_input("Gemini API Key", type="password")
    
    if api_key:
        datastore = get_datastore()
        handler = get_handler(api_key, datastore, _version=2)
        
        # Chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about the papers..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get response
            with st.spinner("Thinking..."):
                response = handler.answer_question(prompt)
            
            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
    else:
        st.warning("Please enter your Gemini API Key to use the chat interface.")