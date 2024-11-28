import sys
import os
import pandas as pd
from text_cleaning import clean_text
from textblob import TextBlob
from sklearn.preprocessing import MinMaxScaler

# Add the root directory to sys.path to resolve 'ingestion' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Root directory

from ingestion.database_setup import get_database_connection
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def feature_engineering(df):
    """
    Function to create additional features, such as sentiment score.
    """
    def get_sentiment(text):
        try:
            # Return the polarity score from TextBlob (ranges from -1 to 1)
            return TextBlob(text).sentiment.polarity
        except Exception as e:
            logger.error(f"Error calculating sentiment: {e}")
            return None

    try:
        # Create sentiment score from the cleaned review text
        df['sentiment_score'] = df['cleaned_review_text'].apply(get_sentiment)
    except Exception as e:
        logger.error(f"Error adding sentiment scores: {e}")

    try:
        # Example of scaling the rating column
        scaler = MinMaxScaler()
        df['normalized_rating'] = scaler.fit_transform(df[['rating']])
    except Exception as e:
        logger.error(f"Error scaling ratings: {e}")

    return df

def preprocess_data():
    try:
        # Step 1: Load cleaned data from CSV file
        logger.info("Loading cleaned data from CSV file...")
        df = pd.read_csv('C:/Users/RNaveen/Documents/LLM-Data-Engineer-Assignment/data/processed/cleaned_data.csv')
        logger.info("Data loaded successfully from CSV.")

        # Step 2: Clean the text column (if not already cleaned in previous steps)
        logger.info("Cleaning text data...")
        df['cleaned_review_text'] = df['review_text'].apply(clean_text)  # Assuming 'review_text' column exists
        logger.info("Text cleaning completed.")

        # Step 3: Feature engineering (e.g., sentiment score, normalized rating)
        logger.info("Starting feature engineering...")
        df = feature_engineering(df)
        logger.info("Feature engineering completed.")

        # Step 4: Save the preprocessed data back to the database
        logger.info("Saving preprocessed data to the database...")
        engine = get_database_connection()  # Assuming you have a method to get the database connection
        df.to_sql('processed_product_reviews', con=engine, if_exists='replace', index=False)
        logger.info("Data preprocessing successful and saved to the database.")
    
    except Exception as e:
        logger.error(f"Error during preprocessing: {e}")

if __name__ == '__main__':
    preprocess_data()
