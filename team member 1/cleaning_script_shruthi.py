import os
import requests
import csv
from datetime import datetime

def import_data(url):
    """
    Downloads the dataset from the provided URL and saves it to the data/ folder.
    Returns the dataset as a list of strings (each line as an element).
    """
    # Ensure the 'data' folder exists
    os.makedirs("data", exist_ok=True)

    # Define file path
    file_path = "data/dataset_M1.txt"

    # Download the dataset
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)
    else:
        raise Exception("Failed to download data.")

    # Read the file and return its content as a list of lines
    with open(file_path, "r", encoding="utf-8") as f:
        data_lines = f.readlines()

    return data_lines

def clean_data(data_text_list):
    """
    Converts the date format in the 'time' column to 'DD-MM-YYYY HH:MM:SS'.
    Saves the cleaned dataset and returns the modified list of strings.
    """
    # Ensure the 'output' folder exists
    os.makedirs("output", exist_ok=True)

    # Process the dataset as a CSV
    data_str = "".join(data_text_list)
    csv_reader = csv.reader(data_str.splitlines())
    
    # Extract header and find the index of the 'time' column
    header = next(csv_reader)
    if "time" not in header:
        raise KeyError("The dataset does not have a 'time' column.")

    date_index = header.index("time")
    
    # Process each row
    cleaned_rows = [header]  # Start with the header row
    for row in csv_reader:
        try:
            original_date = row[date_index]
            original_date = original_date.rstrip("Z")  # Remove trailing 'Z' if present
            dt = datetime.fromisoformat(original_date)
            formatted_date = dt.strftime("%d-%m-%Y %H:%M:%S")
            row[date_index] = formatted_date
        except Exception as e:
            print(f"Error processing row: {e}")
        
        cleaned_rows.append(row)

    # Save cleaned data to output file
    output_file = "output/cleaned_data_M1.txt"
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(cleaned_rows)

    return ["\t".join(row) + "\n" for row in cleaned_rows]  # Return cleaned dataset as a list of strings

if __name__ == "__main__":
    dataset_url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2023-01-01&endtime=2023-01-02"

    # Download and inspect dataset
    raw_data = import_data(dataset_url)
    print("First 5 rows of raw data:")
    print("".join(raw_data[:5]))  # Print first 5 rows for inspection

    # Clean dataset
    cleaned_data = clean_data(raw_data)

    print(f"✅ Cleaned dataset saved in 'output/cleaned_data_M1.txt'")
