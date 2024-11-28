import csv
import re
import statistics
from collections import Counter

# Function to clean text data
def clean_text(text):
    # Remove special characters and extra spaces
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)  # Removes non-alphanumeric characters except spaces
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = text.strip()  # Remove leading and trailing spaces
    text = text.lower()  # Convert to lowercase
    return text

# Function to check if a string is empty or NaN
def is_empty_or_nan(value):
    return value == "" or value is None or value.lower() == "nan"

# Function to fill missing values in a column based on other rows (imputation)
def fill_missing_values(data, column):
    # For categorical columns, use the most frequent value (mode)
    values = [row[column] for row in data if not is_empty_or_nan(row[column])]
    if values:
        most_common_value = Counter(values).most_common(1)[0][0]  # Get most frequent value
    else:
        most_common_value = None
    
    for row in data:
        if is_empty_or_nan(row[column]):
            row[column] = most_common_value  # Fill missing value with the most common value

# Function to fill numeric columns with the mean or median value
def fill_numeric_missing_values(data, column):
    # For numeric columns, use the mean or median
    numeric_values = [float(row[column]) for row in data if not is_empty_or_nan(row[column])]
    if numeric_values:
        mean_value = sum(numeric_values) / len(numeric_values)  # Mean value
        for row in data:
            if is_empty_or_nan(row[column]):
                row[column] = mean_value  # Fill missing value with the mean value

# Function to check if a row is fully empty or NaN
def is_row_empty(row):
    return all(is_empty_or_nan(value) for value in row.values())

# Read the existing CSV data
input_csv = 'C:/Users/RNaveen/Documents/LLM-Data-Engineer-Assignment/data/input/amazon_reviews.csv'
output_csv = 'C:/Users/RNaveen/Documents/LLM-Data-Engineer-Assignment/data/processed/cleaned_data.csv'

# Open the input CSV file and read its contents with the correct encoding (UTF-8)
with open(input_csv, 'r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    
    # Get the headers (fieldnames)
    fieldnames = reader.fieldnames
    print("Headers:", fieldnames)  # Debug print to show headers

    # Process the data (clean the text for relevant fields)
    data = []
    for row in reader:
        print("Original Row:", row)  # Debug print to show the row before processing
        
        # Skip rows that are completely empty or NaN
        if is_row_empty(row):
            print("Skipping row due to being empty:", row)  # Debug print to show why a row is skipped
            continue
        
        cleaned_row = row.copy()  # Copy the row to avoid modifying it directly while iterating
        
        # Clean text in each relevant field (assuming you want to clean all string fields)
        for key, value in cleaned_row.items():
            if isinstance(value, str):  # Check if the value is a string
                cleaned_row[key] = clean_text(value)  # Clean the text
        
        data.append(cleaned_row)

    # Ensure that there is data to process and remove columns where all values are empty or NaN
    if data:
        # Impute missing values in relevant columns
        for column in fieldnames:
            if column in data[0]:  # Ensure the column exists in the data
                if all(is_empty_or_nan(row[column]) for row in data):  # If column is completely empty
                    continue
                if isinstance(data[0][column], str):  # Categorical column (fill with mode)
                    fill_missing_values(data, column)
                elif isinstance(data[0][column], (int, float)):  # Numeric column (fill with mean)
                    fill_numeric_missing_values(data, column)

        # Write the processed data to a new CSV file with the correct encoding (UTF-8)
        with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)

            # Write the header to the output file
            writer.writeheader()
            
            # Write the processed data rows to the output file
            writer.writerows(data)

        print(f"CSV data has been cleaned and saved to {output_csv}.")
    else:
        print("No valid data found to write.")
