import os
import sys
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Root directory

from ingestion.database_setup import get_database_connection
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Initialize the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')  # You can use other models as well

def get_embeddings(texts):
    """
    Given a list of texts, return their embeddings.
    """
    try:
        embeddings = model.encode(texts, convert_to_tensor=True)
        return embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        return []

def save_embeddings_to_csv():
    try:
        # Step 1: Load preprocessed data from the database
        engine = get_database_connection()
        df = pd.read_sql('SELECT * FROM processed_product_reviews', con=engine)

        # Step 2: Generate embeddings for the cleaned reviews
        embeddings = df['cleaned_review_text'].apply(lambda x: get_embeddings([x])).tolist()

        # Flatten the embeddings from (1, 384) to a 1D array with 384 elements for each review
        embeddings_flattened = [embedding[0] for embedding in embeddings]  # Get the first element, which is a 384-dimensional array

        # Convert the flattened embeddings to a DataFrame
        embeddings_df = pd.DataFrame(embeddings_flattened)

        # Add review IDs for reference
        embeddings_df['review_id'] = df['review_hash_id']  # Assuming you have review_hash_id as the ID

        # Save embeddings and associated review ids to a CSV file
        embeddings_df.to_csv('review_embeddings.csv', index=False)

        logger.info("Embeddings saved to review_embeddings.csv successfully.")

    except Exception as e:
        logger.error(f"Error during saving embeddings to CSV: {e}")

if __name__ == '__main__':
    save_embeddings_to_csv()
