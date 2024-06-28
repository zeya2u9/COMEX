import os

def count_connected_rows(input_directory, output_file):
    result = {}
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            connected_count = 0
            with open(os.path.join(input_directory, filename), 'r') as file:
                for line in file:
                    elements = line.strip().split(" ")
                    print(elements[8])
                    if len(elements) >= 3 and elements[8] == "CONNECTED":
                        connected_count += 1
            result[filename] = connected_count
    
    with open(output_file, 'w') as output:
        for filename, count in result.items():
            output.write(f"File: {filename}, Number of rows with 'connected' in the 3rd element: {count}\n")

input_directory_path = "~/COMEX/analysis/clean_netstat"
output_file_path = "output.txt"
count_connected_rows(input_directory_path, output_file_path)
