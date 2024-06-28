import os

def remove_headers(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            with open(os.path.join(input_directory, filename), 'r') as file:
                lines = file.readlines()
                
                column_index = next((i for i, line in enumerate(lines) if line.startswith("Proto RefCnt Flags       Type       State         I-Node   Path")), None)
                
                if column_index is not None:
                    output_filename = os.path.join(output_directory, "header_removed_" + filename)
                    with open(output_filename, 'w') as new_file:
                        new_file.writelines(lines[column_index:])
                    print(f"Header removed from {filename}, saved as {output_filename}")
                else:
                    print(f"No column names found in {filename}")

input_directory_path = "~/COMEX/netstat"
output_directory_path = "~/COMEX/analysis/netstat"
remove_headers(input_directory_path, output_directory_path)
