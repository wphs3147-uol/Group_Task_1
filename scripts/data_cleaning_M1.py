import os
import requests

def import_data():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2023-01-01&endtime=2023-01-02"
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
    
    for line in data_text_list:
        words = line.split(",")
        for i in range(len(words)):
            word = words[i]
            if "/" in word or "-" in word:
                date_parts = word.replace("T", " ").replace("/", "-").split("-")
                if len(date_parts) >= 3:
                    if len(date_parts[0]) == 4:
                        words[i] = date_parts[2] + "-" + date_parts[1] + "-" + date_parts[0]
                    elif len(date_parts[2]) == 4:
                        words[i] = date_parts[0] + "-" + date_parts[1] + "-" + date_parts[2]
        cleaned_lines.append(",".join(words))
    
    with open(output_path, "w") as file:
        file.writelines(cleaned_lines)
    
    return cleaned_lines

if __name__ == "__main__":
    data = import_data()
    cleaned_data = clean_data(data)
    print("Data cleaning completed.")
