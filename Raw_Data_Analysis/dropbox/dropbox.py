import os

def extract_info(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    pid = None
    error_service = None
    cause = None

    for line in lines:
        if "PID:" in line:
            pid = line.split("PID: ")[1].split()[0]
        elif "android.util.Log$TerribleFailure:" in line:
            error_service = line.split("android.util.Log$TerribleFailure:")[1].strip()
        elif "Caused by:" in line:
            cause = line.split("Caused by: ")[1].strip()
    
    return pid, error_service, cause

def process_files(directory):
    for app in os.listdir(directory):
        app_path_1 = os.path.join(directory, app)
        app_path = os.path.join(app_path_1, 'dropbox')
        if not os.path.isdir(app_path):
            continue  # Skip if dropbox folder doesn't exist
        #print(f"Processing files in: {app_path}") 
        for filename in os.listdir(app_path):
            #print(f"Found file: {filename}")
            if filename.startswith('system_server_wtf@'):
                #print(filename)
                file_path = os.path.join(app_path, filename)
                pid, error_service, cause = extract_info(file_path)
                #print(pid, error_service, cause)
                if pid or error_service or cause:
                    output_file_path = os.path.join(app_path, 'concatenated.txt')
                    write_to_text_file([{'PID': pid, 'Error Service': error_service, 'Cause': cause}], output_file_path)
            #else:
                #print("akshat")
def write_to_text_file(log_info, output_file):
    with open(output_file, 'a') as file:
        for entry in log_info:
            file.write(f"{entry['PID']}\t{entry['Error Service']}\t{entry['Cause']}\n")

if __name__ == "__main__":
    directory_path = '~/COMEX/dropbox'
    process_files(directory_path)
