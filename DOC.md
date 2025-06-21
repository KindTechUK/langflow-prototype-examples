# Citizen Advice RAG Flow Documentation

## Overview

This Langflow flow implements a **Retrieval Augmented Generation (RAG)** system designed to answer questions based on content from the Citizen Advice website. It loads and ingests website data, processes and indexes it into a vector database, and then uses a language model to answer user queries with relevant, factual information.

## Flow Components and How They Work Together

### 1. Data Loading and Ingestion

#### URL Component
- Recursively crawls and loads web pages starting from the Citizen Advice benefits URL (`https://www.citizensadvice.org.uk/benefits/`)
- Configurable max depth (default 2) controls how many link levels are followed
- Option to restrict crawling to the same domain to avoid external sites
- Supports asynchronous loading for faster crawling
- Outputs raw text data extracted from HTML pages as a list of documents

#### Split Text Component
- Splits the loaded text documents into smaller chunks for better embedding and retrieval
- Configured with chunk size (default 1000 characters) and overlap (default 200 characters) to maintain context between chunks
- Outputs chunks as data objects

#### MistralAI Embeddings Component
- Converts text chunks into vector embeddings using MistralAI embedding models
- Requires a Mistral API key for authentication

#### Chroma Vector Store Component
- Stores embeddings and associated text chunks in a Chroma vector database for efficient similarity search
- Configured with collection name (`cas-benefits`) and persistence directory (`./chroma-db`)
- Supports options like allowing duplicates and caching

### 2. Query Handling and Prompt Construction

#### Chat Input Component
- Entry point for user queries entered in the Langflow Playground interface
- Captures user messages and metadata such as sender info and session ID

#### Chroma Vector Store (Search Query Input)
- Receives the user query and performs a similarity search in the vector store to retrieve relevant documents
- Outputs search results as data objects

#### Parser Component
- Formats the retrieved search results into a textual context using a template (e.g., `{source}` or `{text}`)
- Supports cleaning data and converting structured data into readable text

#### Prompt Component
- Combines the retrieved context, source URLs, and user question into a prompt template
- The prompt instructs the language model to answer factually based on the retrieved content and to include source URLs without duplicates

### 3. Language Model and Output

#### MistralAI Model Component
- Generates the answer text using MistralAI large language models
- Configurable parameters include model name, temperature, max tokens, API key, and more
- Input is the prompt message constructed by the Prompt Component
- Output is the generated answer as a message

#### Chat Output Component
- Displays the generated answer in the Langflow Playground chat interface
- Supports storing the message in chat history and customizing sender info and appearance

### 4. Additional Components and Notes

#### Batch Run Component
- Allows running the language model over each row of a DataFrame, useful for batch processing or evaluation

#### Correctness Evaluator Component
- Uses OpenAI's LLM to evaluate the correctness of model outputs against reference answers

#### Privacy Anonymizer Component (Optional)
- Can anonymize input text by masking sensitive information (PII), useful for privacy compliance

#### Note Nodes
- Provide inline documentation and guidance within the flow workspace, such as reminders to add API keys and instructions on running the data loading flow first

## How to Build a Similar Flow in Langflow

### 1. Load Data
- Use a **URL loader** to crawl and extract text from your target website or data source
- Split the text into chunks suitable for embedding

### 2. Generate Embeddings
- Use an **embedding model component** (e.g., MistralAI Embeddings) to convert text chunks into vectors

### 3. Create a Vector Store
- Use a **vector store component** (e.g., Chroma) to index and store embeddings for similarity search

### 4. Set Up Query Input and Retrieval
- Use a **Chat Input** component to accept user queries
- Connect it to the vector store to perform similarity search and retrieve relevant documents

### 5. Format Retrieved Data
- Use a **Parser** component to convert retrieved documents into a readable context string

### 6. Build Prompt
- Use a **Prompt** component to combine context, sources, and user question into a prompt template

### 7. Generate Answer
- Use a **language model component** (e.g., MistralAI) to generate answers from the prompt

### 8. Display Output
- Use a **Chat Output** component to show the generated answer in the chat interface

### 9. Add Optional Components
- Add **batch processing** or **evaluation components** to test and improve your system
- Add **privacy components** if needed

### 10. Document Your Flow
- Use **Note nodes** to add helpful comments and instructions for users
