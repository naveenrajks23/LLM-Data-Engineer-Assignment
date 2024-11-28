import numpy as np
import pandas as pd
import json
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ingestion.database_setup import get_database_connection  # Import the database connection function

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def load_embeddings_from_json(file_path):
    """
    Load the review embeddings from a JSON file and prepare it for insertion into the database.
    """
    try:
        logger.info(f"Loading embeddings from JSON file: {file_path}")
        
        # Load the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Check the first few entries to debug
        logger.info(f"First few entries: {data[:5]}")

        # Ensure the JSON data is in the expected format
        if not all(['review_id' in entry and 'embedding' in entry for entry in data]):
            raise ValueError("JSON data must contain 'review_id' and 'embedding' keys.")

        # Convert each embedding to a numpy array and ensure the embedding is a list of floats
        def clean_embedding(embedding):
            # Ensure the embedding is a list of floats (if it's not already cleaned)
            cleaned_embedding = []
            for value in embedding:
                if isinstance(value, str):  # Check if the value is a string (tensor format)
                    value = value.replace('tensor(', '').replace(')', '')  # Clean tensor string
                cleaned_embedding.append(float(value))  # Convert to float
            return np.array(cleaned_embedding)
        
        # Clean the embeddings and create a DataFrame
        df = pd.DataFrame(data)
        df['review_embeddings'] = df['embedding'].apply(clean_embedding)
        
        # Keep only the necessary columns ('review_id' and 'review_embeddings')
        df = df[['review_id', 'review_embeddings']]
        
        logger.info(f"Loaded {len(df)} rows of embeddings.")

        # Insert the data into the database
        insert_embeddings_into_db(df)

        return df

    except Exception as e:
        logger.error(f"Error loading embeddings from JSON: {e}")
        return pd.DataFrame()

def insert_embeddings_into_db(df):
    """
    Insert the review embeddings into a new table in the database using the pre-existing connection.
    """
    try:
        # Connect to the database using the engine from database_setup.py
        engine = get_database_connection()
        logger.info("Database connection established successfully.")
        
        # Convert numpy array to list and then to JSON for storage
        df['review_embeddings'] = df['review_embeddings'].apply(lambda x: json.dumps(x.tolist()))

        # Use pandas to_sql for bulk insert (replace existing table if needed)
        with engine.begin():  # This ensures a transaction is used if you're using SQLAlchemy
            df.to_sql('review_embeddings_table', con=engine, if_exists='replace', index=False)
        
        logger.info(f"Successfully inserted {len(df)} embeddings into the database.")
    
    except Exception as e:
        logger.error(f"Error inserting embeddings into database: {e}")

# Example of how the function would be used
if __name__ == '__main__':
    file_path = 'C:/Users/RNaveen/Documents/LLM-Data-Engineer-Assignment/vectorization/cleaned_vector_store.json'
    df = load_embeddings_from_json(file_path)
    if not df.empty:
        print(df.head())  # You can use this to verify the output
