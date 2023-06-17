# AI-Semantic Search Engine

Semantic Search Engine is a powerful search tool that combines Pinecone's Vector Database and OpenAI's LLM Model to provide accurate and efficient search results. It allows you to upload various file formats (PDF, DOCX, TXT) and ask queries related to the content of those files, providing you with relevant answers within seconds.

## Features

- Supports PDF, DOCX, and TXT file formats.
- Utilizes Pinecone's Vector Database for fast and accurate similarity search.
- Integrates OpenAI's LLM Model for question-answering capabilities.
- Easy-to-use web interface powered by Streamlit.

## Getting Started

To get started with Semantic Search Engine, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/semantic-search.git
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt 

3.Set up your OpenAI API key:

Sign up for an account at https://platform.openai.com if you haven't already.
Retrieve your OpenAI API key from your account dashboard.
In the app.py file, replace YOUR_OPENAI_API_KEY with your actual API key.

4.Set up your Pinecone API key (optional):

Sign up for a Pinecone account at https://www.pinecone.io if you haven't already.
Retrieve your Pinecone API key.
In the main.py file, replace YOUR_PINECONE_API_KEY with your actual API key.

5.Run the application:

streamlit run app.py
Open your browser and access the application at http://localhost:8501.

## Usage
1.Upload a file:

Click on the "Upload Document" button and select a file in PDF, DOCX, or TXT format.
Wait for the file to be processed and indexed.

2.Ask a question:

In the text area below, enter your question related to the document.
Click the "Submit" button.

3.View the answer:

The answer to your question will be displayed below the text area.
## Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request. 
For major changes, please open an issue first to discuss the proposed changes.


## Live Website Link
https://ai-sementic-search.streamlit.app/
