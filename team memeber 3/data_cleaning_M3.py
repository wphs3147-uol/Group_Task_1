import os
import requests

def import_data(url):
    """Downloads the earthquake dataset and saves it as dataset_M3.txt."""
    
    # Send request to download the dataset
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download data: {response.status_code}")

    data_text = response.text  # Store the dataset as text

    # Ensure the 'data/' folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # Save raw dataset to data/dataset_M3.txt
    file_path = os.path.join("data", "dataset_M3.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(data_text)

    # Read file back as a list of lines
    with open(file_path, "r", encoding="utf-8") as file:
        data_lines = file.readlines()
    
    return data_lines

# Test the function
if __name__ == "__main__":
    test_url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2023-01-01&endtime=2023-01-02"
    data = import_data(test_url)
    print(f"Downloaded {len(data)} lines and saved to dataset_M3.txt.")

import csv
from io import StringIO
from datetime import datetime

def clean_data(data_text_list):
    """Standardizes date format in earthquake dataset."""
    
    # Convert list of strings into CSV reader
    data_str = "".join(data_text_list)
    csv_reader = csv.reader(StringIO(data_str))
    
    # Extract header
    header = next(csv_reader)
    
    # Identify 'time' column index
    try:
        time_index = header.index("time")
    except ValueError:
        raise Exception("Time column not found in dataset.")

    cleaned_rows = [header]  # Add header back to cleaned data

    # Process each row
    for row in csv_reader:
        original_date = row[time_index].rstrip("Z")  # Remove 'Z' if present
        try:
            dt = datetime.fromisoformat(original_date)  # Parse date
            formatted_date = dt.strftime("%d-%m-%Y %H:%M:%S")  # Format as DD-MM-YYYY HH:MM:SS
            row[time_index] = formatted_date
        except Exception as e:
            print(f"Skipping invalid date '{original_date}': {e}")

        cleaned_rows.append(row)

    # Ensure output/ folder exists
    if not os.path.exists("output"):
        os.makedirs("output")

    # Save cleaned data
    output_file = os.path.join("output", "cleaned_data_M3.txt")
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(cleaned_rows)

    # Return cleaned data as list of strings
    return [";".join(row) + "\n" for row in cleaned_rows]

# Run cleaning function
if __name__ == "__main__":
    data = import_data("https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2023-01-01&endtime=2023-01-02")
    cleaned_data = clean_data(data)
    print("Data cleaning complete. Saved to output/cleaned_data_M3.txt.")

    