import os
import requests
from datetime import datetime

def import_data(url):
    file_path = "data/dataset_M1.txt"
    
    if not os.path.exists("data"):
        os.makedirs("data")
    
    response = requests.get(url)
    with open(file_path, "w") as file:
        file.write(response.text)
    
    with open(file_path) as file:
        data_lines = file.readlines()
    
    return data_lines

def clean_data(data_text_list):
    if not os.path.exists("output"):
        os.makedirs("output")
    
    output_path = "output/cleaned_data_M1.txt"
    cleaned_lines = []
    
    for i, line in enumerate(data_text_list):
        if i == 0:
            cleaned_lines.append(line)
            continue

        words = line.strip().split(",")
        for j in range(len(words)):
            word = words[j]
            try:
                if "T" in word:
                    dt = datetime.strptime(word, "%Y-%m-%dT%H:%M:%S.%fZ")
                    words[j] = dt.strftime("%d-%m-%Y %H:%M:%S")
            except:
                continue
        
        cleaned_lines.append(",".join(words) + "\n")
    
    with open(output_path, "w") as file:
        file.writelines(cleaned_lines)
    
    return cleaned_lines

if __name__ == "__main__":
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2023-01-01&endtime=2023-01-02"
    data = import_data(url)
    cleaned_data = clean_data(data)
    print("Data cleaning completed.")
