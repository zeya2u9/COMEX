import os
import csv

def remove_multiple_spaces(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, "cleaned_" + filename)
            with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
                reader = csv.reader(infile)
                writer = csv.writer(outfile)
                for row in reader:
                    cleaned_row = [cell.replace('  ', ' ') for cell in row]
                    writer.writerow(cleaned_row)

input_directory_path = "~/COMEX/analysis/netstat"
output_directory_path = "~/COMEX/analysis/clean_netstat"
remove_multiple_spaces(input_directory_path, output_directory_path)
