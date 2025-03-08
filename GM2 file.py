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
    
    if not os.path.exists("data"):
        os.makedirs("data")
    
    file_path = os.path.join("data", "dataset_M1.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data_text)
    
    return data_text.splitlines()

def clean_data(data_text_list):
    data_str = "\n".join(data_text_list)
    csv_reader = csv.reader(StringIO(data_str))
    header = next(csv_reader)
    
    date_index = header.index("time")
    cleaned_rows = [header]
    
    for row in csv_reader:
        try:
            original_date = row[date_index].rstrip("Z")  
            dt = datetime.fromisoformat(original_date)
            formatted_date = dt.strftime("%d-%m-%Y %H:%M:%S")
            row[date_index] = formatted_date
        except Exception as e:
            print(f"Error processing row: {e}")
        cleaned_rows.append(row)
    
    if not os.path.exists("output"):
        os.makedirs("output")
    
    output_file = os.path.join("output", "cleaned_data_M1.txt")
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(cleaned_rows)
    
    return [",".join(row) for row in cleaned_rows]