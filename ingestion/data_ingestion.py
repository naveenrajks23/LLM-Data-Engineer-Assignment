import os
import pandas as pd
from sqlalchemy import create_engine
# from ingestion.data_ingestion import get_database_connection
from database_setup import get_database_connection
 # Import the connection function from dbsetup.py

# Load your JSON file into pandas DataFrame
file_path = 'C:/Users/RNaveen/Documents/LLM-Data-Engineer-Assignment/data/input/amazon_reviews.json'  # Change this to your actual file path

# Ingest the data from the JSON file into the DataFrame
try:
    df = pd.read_json(file_path)
    print("Data loaded successfully from JSON file.")
except Exception as e:
    print(f"Error loading JSON data: {e}")

# Connect to the database using the engine from dbsetup.py
try:
    engine = get_database_connection()
    print("Database connection established successfully.")
    
    # Ingest the data into your database (adjust the table name as needed)
    df.to_sql('product_reviews', con=engine, if_exists='replace', index=False)
    print("Data ingestion successful!")
except Exception as e:
    print(f"Error during ingestion: {e}")
