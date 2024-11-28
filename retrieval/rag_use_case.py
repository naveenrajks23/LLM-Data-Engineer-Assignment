import warnings
from transformers import pipeline
import logging

# Suppress the warning for max_length mismatch
warnings.filterwarnings("ignore", category=UserWarning, message=".*max_length.*")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_summary_or_response(retrieved_records, query, summarizer_model):
    """
    Use retrieved records to generate a response or summary.
    """
    try:
        # Combine retrieved records as context
        context = " ".join([record['review_text'] for record in retrieved_records])  # Adjust field as needed
        input_text = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"

        # Calculate the length of the input and adjust max_length based on it
        input_length = len(input_text.split())
        max_length = min(40, input_length + 50)  # Lower the max_length to a more reasonable value
        min_length = max(10, min(max_length - 10, 50))  # Ensure min_length is valid

        # Generate a summary or answer with dynamic max_length
        response = summarizer_model(input_text, max_length=max_length, min_length=min_length, do_sample=False)

        # Log the generated response
        logger.info(f"Generated response: {response[0]['summary_text']}")
        return response[0]['summary_text']
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "Sorry, I could not generate a response."

# Example script usage
if __name__ == "__main__":
    # Example data, replace with actual retrieved records
    query = "What are the most frequent issues with this product?"
    retrieved_records = [{"review_text": "The battery life is short."}, 
                         {"review_text": "Build quality is poor."}, 
                         {"review_text": "Customer support is unresponsive."}, 
                         {"review_text": "The product overheats during use."}] 
    # Load or initialize your summarization model (e.g., HuggingFace pipeline)
    summarizer_model = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # Generate a response
    response = generate_summary_or_response(retrieved_records, query, summarizer_model)
    print(f"Final Generated Response: {response}")
