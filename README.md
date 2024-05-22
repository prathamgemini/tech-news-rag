### README

# RAG Project with The Guardian Technology Articles

This project implements a Retrieval-Augmented Generation (RAG) system using articles from The Guardian's technology section. The system retrieves relevant documents based on user queries and generates detailed answers using a language model. The following instructions will guide you through setting up and running the project.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
- [Running the Program](#running-the-program)
- [File Descriptions](#file-descriptions)
- [Acknowledgments](#acknowledgments)

## Prerequisites
Ensure you have the following installed:
- Python 3.8+
- wkhtmltopdf
- Qdrant
- The Guardian API key
- Streamlit
- Download the mistral-7b-v0.1.Q4_K_M.gguf model from [Hugging Face](https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF) and place it in the root directory of this project.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/prathamgemini/tech-news-rag.git
    cd rag-project
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Install wkhtmltopdf:
    - Download and install wkhtmltopdf from [here](https://wkhtmltopdf.org/downloads.html).
    - Ensure the executable is accessible from your PATH or note its installation path for later configuration.

4. Install and run Qdrant:
    - Follow the instructions on the [Qdrant documentation](https://qdrant.tech/documentation/) to install and run Qdrant.

## Setup
1. **Guardian API Key:**
   - Obtain an API key from The Guardian.
   - Set the API key as an environment variable:
     ```bash
     export GUARDIAN_API_KEY='your_api_key_here'
     ```

2. **Directory Structure:**
   Ensure the following directories are present:
   ```bash
   corpus/
   media/
   pdfs/
   ```

## Running the Program
### 1. Fetch Articles (Not necessary as I have already included the files in the corpus folder)
Run the `fetchdata.py` script to fetch articles from The Guardian:
```bash
python fetchdata.py
```
This will download the articles and save them in the `corpus` directory.

### 2. Convert HTML to PDF (Not necessary as I have already included the files in the pdfs folder)
Run the `html2pdf.py` script to convert the HTML files to PDF:
```bash
python html2pdf.py
```
This will generate PDF files in the `pdfs` directory.

### 3. Ingest Data into Qdrant
Run the `ingest.py` script to ingest the PDF data into Qdrant:
```bash
python ingest.py
```
This will create a vector database in Qdrant with the ingested documents.

### 4. Run the Streamlit Application
Start the Streamlit application:
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501` to interact with the application.

## File Descriptions
- **fetchdata.py:** Fetches articles from The Guardian API and saves them as HTML files.
- **html2pdf.py:** Converts HTML files to PDF format.
- **ingest.py:** Ingests PDF documents into Qdrant vector database.
- **app.py:** Streamlit application for user interaction and query processing.

## Acknowledgments
- The Guardian API for providing access to news articles.
- The developers of Qdrant for the vector database.
- The authors of `pdfkit`, `BeautifulSoup`, and other libraries used in this project.

