import json

input_file = 'vector_store.json'  # Your current vector store file
output_file = 'cleaned_vector_store.json'

try:
    with open(input_file, 'r') as f:
        vector_store = json.load(f)

    cleaned_store = []
    for item in vector_store:
        try:
            # Parse string embeddings into floats
            cleaned_embedding = [float(str(value).replace("tensor(", "").replace(")", "")) for value in item['embedding']]
            cleaned_store.append({
                "review_id": item['review_id'],
                "embedding": cleaned_embedding
            })
        except Exception as e:
            print(f"Error cleaning embedding for review_id {item['review_id']}: {e}")

    # Save the cleaned vector store
    with open(output_file, 'w') as f:
        json.dump(cleaned_store, f)

    print(f"Cleaned vector store saved to {output_file}")

except Exception as e:
    print(f"Error processing vector store: {e}")
