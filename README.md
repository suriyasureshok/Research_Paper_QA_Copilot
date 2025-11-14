# Research Paper QA Copilot

A comprehensive AI-powered tool for collecting research papers from arXiv, processing their full text, and enabling intelligent question-answering through semantic search and large language models.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Dependencies](#dependencies)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Features

- **Automated Paper Collection**: Fetch research papers from arXiv based on topics and quantity limits
- **Full-Text Extraction**: Extract complete text content from PDF papers using PyMuPDF
- **Intelligent Text Chunking**: Use semantic chunkers to split text into meaningful segments
- **Vector Database Storage**: Store text chunks with embeddings in Qdrant for efficient retrieval
- **Semantic Search**: Perform similarity-based search on stored chunks
- **AI-Powered QA**: Answer questions using Google's Gemini LLM with retrieved context
- **Web Interface**: User-friendly Streamlit application with separate pages for paper collection and chat
- **Persistent Storage**: Local Qdrant database for data persistence across sessions

## Architecture

The system follows a Retrieval-Augmented Generation (RAG) pattern:

1. **Data Ingestion Pipeline**:
   - ArXiv API integration for paper discovery
   - PDF download and text extraction
   - Semantic text chunking

2. **Vector Storage Layer**:
   - Sentence Transformers for embedding generation
   - Qdrant vector database for storage and search

3. **QA Engine**:
   - Semantic search for relevant context retrieval
   - Gemini LLM for answer generation

4. **User Interface**:
   - Streamlit web application
   - Multi-page interface (Collection + Chat)

## Installation

### Prerequisites

- Python 3.8 or higher
- A Google Gemini API key (free tier available)

### Setup Steps

1. **Clone the repository**:
   `bash
   git clone https://github.com/suriyasureshok/Research_Paper_QA_Copilot.git
   cd Research_Paper_QA_Copilot
   `

2. **Create a virtual environment**:
   `bash
   python -m venv paper-qa
   `

3. **Activate the virtual environment**:
   - Windows:
     `bash
     .\paper-qa\Scripts\activate
     `
   - macOS/Linux:
     `bash
     source paper-qa/bin/activate
     `

4. **Install dependencies**:
   `bash
   pip install -r requirements.txt
   `

5. **Set up environment variables**:
   Create a .env file in the root directory:
   `
   GEMINI_API_KEY=your_gemini_api_key_here
   `

   Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

## Usage

### Running the Application

1. **Start the Streamlit app**:
   `bash
   streamlit run src/app.py
   `

2. **Access the web interface**:
   Open your browser and navigate to http://localhost:8501

### Using the Application

#### Paper Collection Page

1. Enter a research topic (e.g., "machine learning", "quantum computing")
2. Specify the maximum number of papers to collect
3. Click "Collect Papers" to start the ingestion process
4. The system will:
   - Search arXiv for relevant papers
   - Download PDF files
   - Extract full text content
   - Chunk the text semantically
   - Generate embeddings and store in Qdrant

#### Chat Interface Page

1. Enter your question about the collected research papers
2. The system will:
   - Search for relevant text chunks in the vector database
   - Provide context to the Gemini LLM
   - Generate an answer based on the research content

### Command-Line Testing

You can also test individual components:

`python
# Test paper collection
from src.data_ingestion.paper_collector import ArxivPaperCollection
collector = ArxivPaperCollection()
papers = collector.fetch_papers("machine learning", max_results=5)

# Test text chunking
from src.data_ingestion.text_chunker import TextChunker
chunker = TextChunker()
chunks = chunker.chunk_text("Your text here...")

# Test vector storage
from src.data_ingestion.store_data import DataStore
store = DataStore()
store.add_chunks(chunks)

# Test QA
from src.chat.gemini_client import GeminiQAHandler
handler = GeminiQAHandler("your_api_key", store)
answer = handler.answer_question("What is machine learning?")
`

## How It Works

### 1. Data Ingestion Process

The ArxivPaperCollection class handles paper discovery and processing:

- Uses arXiv's Atom feed API to search for papers by topic
- Downloads PDF files from arXiv
- Extracts text using PyMuPDF (fitz)
- Filters out non-text elements and formatting artifacts

### 2. Text Chunking

The TextChunker class uses semantic chunking:

- Employs semantic_chunkers library with StatisticalChunker
- Splits text based on semantic meaning rather than fixed sizes
- Preserves context within each chunk for better retrieval

### 3. Vector Storage and Search

The DataStore class manages vector operations:

- Uses Sentence Transformers (ll-MiniLM-L6-v2) for 384D embeddings
- Stores chunks with metadata in Qdrant local database
- Performs cosine similarity search for relevant chunks
- Supports batch operations for efficiency

### 4. Question Answering

The GeminiQAHandler class orchestrates QA:

- Searches vector database for relevant context
- Constructs prompts with retrieved chunks
- Uses Gemini 2.0 Flash (free tier) for answer generation
- Provides concise, context-aware responses

### 5. Web Interface

The Streamlit app provides two main pages:

- **Paper Collection**: Form-based interface for data ingestion
- **Chat Interface**: Conversational QA with the research database

## Dependencies

Key dependencies include:

- streamlit: Web application framework
- qdrant-client: Vector database client
- sentence-transformers: Embedding generation
- google-generativeai: Gemini LLM integration
- semantic-chunkers: Intelligent text chunking
- eedparser: arXiv API integration
- PyMuPDF: PDF text extraction
- python-dotenv: Environment variable management

See 
equirements.txt for complete list.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## Acknowledgments

- arXiv for providing open access to research papers
- Google for the Gemini AI models
- Qdrant for the vector database
- All contributors to the open-source libraries used

---

Built with  for researchers and AI enthusiasts.
