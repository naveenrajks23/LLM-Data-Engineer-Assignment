import numpy as np
import json
from sqlalchemy import create_engine, text
from sklearn.metrics.pairwise import cosine_similarity
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Root directory

from ingestion.database_setup import get_database_connection
from sentence_transformers import SentenceTransformer  # Ensure the model is consistent with embeddings generation

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def initialize_embedding_model():
    """
    Initialize and return the SentenceTransformer model.
    """
    try:
        logger.info("Initializing embedding model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')  
        logger.info("Embedding model loaded successfully.")
        return model
    except Exception as e:
        logger.error(f"Error initializing embedding model: {e}")
        return None

def generate_embedding(prompt, embedding_model):
    """
    Generate an embedding for the given text prompt using the embedding model.
    """
    try:
        if embedding_model is None:
            raise ValueError("Embedding model is not initialized.")
        logger.info(f"Generating embedding for prompt: {prompt}")
        embedding = embedding_model.encode(prompt)
        return np.array(embedding)
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return None

def retrieve_similar_embeddings(prompt_embedding, top_n=5):
    """
    Retrieve similar embeddings from the review_embeddings table based on cosine similarity.
    """
    try:
        engine = get_database_connection()

        query = text("SELECT review_id, review_embeddings FROM review_embeddings_table")

        with engine.connect() as conn:
            result = conn.execute(query)
            stored_embeddings = []
            review_ids = []
            
            # Load embeddings and review IDs from the database
            for row in result:
                review_ids.append(row[0])  # Access review_id by index (tuple format)
                stored_embeddings.append(np.array(json.loads(row[1])))  # Convert the embedding to an array (assuming it's JSON)

        if not stored_embeddings:
            logger.warning("No embeddings found in review_embeddings table.")
            return []

        # Compute cosine similarity
        similarities = cosine_similarity([prompt_embedding], stored_embeddings)[0]
        
        # Get the top N similar embeddings
        top_indices = np.argsort(similarities)[-top_n:][::-1]  # Descending order
        similar_ids = [review_ids[i] for i in top_indices]
        return similar_ids
    except Exception as e:
        logger.error(f"Error retrieving similar embeddings: {e}")
        return []



def query_database_for_records(review_ids):
    """
    Query the database for records matching the given review IDs.
    """
    try:
        if not review_ids:
            logger.warning("No review IDs provided to query.")
            return []

        engine = get_database_connection()

        # Dynamically construct the placeholders for the IN clause
        placeholders = ', '.join(f":id{i}" for i in range(len(review_ids)))

        # Updated query with correct column name (e.g., reviewId)
        query = text(f"SELECT * FROM review_embeddings_table WHERE review_id IN ({placeholders})")

        # Map review IDs to parameter names
        params = {f"id{i}": review_id for i, review_id in enumerate(review_ids)}

        with engine.connect() as conn:
            result = conn.execute(query, params)
            records = result.fetchall()

        return records
    except Exception as e:
        logger.error(f"Error querying database: {e}")
        return []

# Example script usage
if __name__ == "__main__":
    # Define the input prompt
    prompt = "This is an example query for a product review"

    # Initialize the embedding model
    embedding_model = initialize_embedding_model()
    if embedding_model is None:
        logger.error("Failed to initialize embedding model. Exiting.")
        sys.exit(1)

    # Generate embedding for the prompt
    prompt_embedding = generate_embedding(prompt, embedding_model)
    if prompt_embedding is None:
        logger.error("Prompt embedding generation failed. Exiting.")
        sys.exit(1)

    # Retrieve similar embeddings from the review_embeddings table
    similar_ids = retrieve_similar_embeddings(prompt_embedding)
    logger.info(f"Retrieved similar IDs: {similar_ids}")

    # Query the database for records corresponding to the similar review IDs
    records = query_database_for_records(similar_ids)
    logger.info(f"Retrieved records: {records}")
