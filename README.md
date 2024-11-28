# LLM Data Engineer Pre-Assignment

## Overview

This project is designed to build a comprehensive pipeline for handling large-scale data processing, including ingestion, vectorization, querying, and retrieving embeddings from a database to generate responses to queries. The goal is to efficiently process and work with product review data using **embedding models**, **vector storage**, and **RAG (Retrieval-Augmented Generation)** techniques.

The core functionalities include:
1. **Data Ingestion** – Collecting and preprocessing product review data.
2. **Vectorization** – Generating embeddings using the **SentenceTransformer** model.
3. **Vector Storage** – Saving embeddings into a structured format (CSV, JSON, or Database).
4. **Querying** – Retrieving similar embeddings from the database.
5. **RAG Use Case** – Using retrieved data to generate summaries or responses using models like **HuggingFace's BART**.

## Project Structure

The project is structured as follows:

```
LLM-Data-Engineer-Assignment/
│
├── ingestion/
│   ├── database_setup.py       # Database connection setup and utility functions
│
├── vectorization/
│   ├── embeddings_model.py     # Script for generating embeddings from text
│   ├── vector_generation.py    # Script to clean and generate vector stores
│   ├── vector_storage.py       # Script to load and store vectors in the database
│
├── query/
│   ├── query_api.py            # API for querying the database and retrieving similar vectors
│
├── rag_usecase/
│   ├── rag_usecase.py          # Use case for generating responses using RAG techniques
│
├── requirements.txt            # Python dependencies for the project
├── README.md                   # Project documentation (this file)
└── .gitignore                  # Git ignore file for excluding unnecessary files
```

## Requirements

- **Python**: 3.7+
- **Libraries**:
  - `sentence-transformers` – For generating text embeddings.
  - `sklearn` – For calculating cosine similarities.
  - `SQLAlchemy` – For interacting with the database.
  - `transformers` – For summarization and generative tasks.
  - `pandas` – For handling data manipulation.
  - `numpy` – For numerical operations.
  - `json` – For data serialization.

You can install the required dependencies using:

```
pip install -r requirements.txt
```

## Modules

### 1. **Ingestion Module**

The ingestion module is responsible for setting up the database connection and loading data into the system. It includes:
- **database_setup.py**: Establishes the connection to the database and provides utility functions for interacting with it.

### 2. **Vectorization Module**

This module focuses on generating and storing embeddings for the product reviews:
- **embeddings_model.py**: Uses `SentenceTransformer` to generate embeddings for product review text.
- **vector_generation.py**: Processes raw embeddings, cleaning and formatting them for storage.
- **vector_storage.py**: Loads cleaned embeddings into the database and prepares them for efficient querying.

### 3. **Query API Module**

The query API module enables querying the database to retrieve similar embeddings based on cosine similarity. It includes:
- **query_api.py**: Contains functions to initialize the embedding model, generate embeddings for prompts, retrieve similar embeddings from the database, and query relevant records.

### 4. **RAG Use Case Module**

The RAG module implements the retrieval-augmented generation technique. It retrieves similar documents based on a query and generates a summary or response using a transformer-based model (e.g., HuggingFace's BART):
- **rag_usecase.py**: Uses retrieved records to generate an answer or summary, leveraging a pre-trained summarization model.

## How to Use

### 1. **Run the Vectorization Pipeline**

- **Step 1**: Ingest the product review data into your database.
  
- **Step 2**: Generate embeddings using the **SentenceTransformer** model. Run the following script:
  ```bash
  python vectorization/embeddings_model.py
  ```

- **Step 3**: Clean and store the embeddings in your database. Run:
  ```bash
  python vectorization/vector_generation.py
  python vectorization/vector_storage.py
  ```

### 2. **Querying for Similar Reviews**

Once the embeddings are stored, you can query the database for similar product reviews. Use the **query_api.py** script to do so:
```bash
python query/query_api.py
```

### 3. **Run RAG Use Case**

To generate responses or summaries from the retrieved records, run the **rag_usecase.py** script:
```bash
python rag_usecase/rag_usecase.py
```

### Example:

- After generating the embeddings and storing them in the database, you can use the RAG model to retrieve similar product reviews and generate responses to questions about the reviews. 

## Logging

The project uses Python's **logging** module to log various stages of processing, including:
- Model initialization
- Embedding generation
- Query execution
- Error handling

Logs will be printed to the console and can also be saved to a file for further debugging.