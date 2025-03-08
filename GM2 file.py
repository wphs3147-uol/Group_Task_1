import os
import requests
import csv
from io import StringIO
from datetime import datetime

def import_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download data.")
    
    data_text = response.text
    
    # Ensure the 'data' folder exists
    if not os.path.exists("data"):
        os.makedirs("data")
    
    file_path = os.path.join("data", "dataset_M1.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data_text)
    
    return data_text.splitlines()

def clean_data(data_text_list):
    """Processes the dataset and converts date format to DD-MM-YYYY HH:MM:SS."""
    data_str = "\n".join(data_text_list)
    csv_reader = csv.reader(StringIO(data_str))
    header = next(csv_reader)
    
    # Find the index of the date field (assume it's called 'time')
    date_index = header.index("time")
    cleaned_rows = [header]
    
    for row in csv_reader:
        try:
            original_date = row[date_index].rstrip("Z")  # Remove trailing 'Z' if present
            dt = datetime.fromisoformat(original_date)
            formatted_date = dt.strftime("%d-%m-%Y %H:%M:%S")
            row[date_index] = formatted_date
        except Exception as e:
            print(f"Error processing row: {e}")
        cleaned_rows.append(row)
    
    # Ensure the 'output' folder exists
    if not os.path.exists("output"):
        os.makedirs("output")
    
    output_file = os.path.join("output", "cleaned_data_M1.txt")
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(cleaned_rows)
    
    return [",".join(row) for row in cleaned_rows]

# Example usage
if __name__ == "__main__":
    dataset_url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2023-01-01&endtime=2023-01-02"
    raw_data = import_data(dataset_url)
    cleaned_data = clean_data(raw_data)
    print("Data cleaning completed successfully.")
