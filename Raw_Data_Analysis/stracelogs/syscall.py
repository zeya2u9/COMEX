import os
import pandas as pd

directory_path = '~/COMEX/stracelogs'

def parse_log_line(line):
    parts = line.strip().split(' ')
    if len(parts) >= 4:
        time = parts[0]
        syscall = parts[1].split('(')[0]
        args = ' '.join(parts[1:]).split('(')[1:]  # Split arguments by '('
        args = [arg.split(')')[0] for arg in args]
        return_value = parts[-1]
        return {'time': time, 'syscall_name': syscall, 'arguments': args, 'return_value': return_value}
    return None

for app in os.listdir(directory_path):
    app_path_1 = os.path.join(directory_path, app)
    app_path = os.path.join(app_path_1,'tmp')
    strace_dir = os.path.join(app_path, 'strace')
    output_file_name = os.path.join(app_path, 'concatenated.txt')

    # Remove strace directory
    if os.path.exists(strace_dir) and os.path.isdir(strace_dir):
        os.system(f'rm -rf {strace_dir}')

    # Concatenate logs
    log_data = []
    with open(output_file_name, 'w') as output_file:
        for file_name in os.listdir(app_path):
            file_path = os.path.join(app_path, file_name)
            if os.path.isfile(file_path) and file_name != 'concatenated.txt':
                with open(file_path, 'r', errors='replace') as input_file:
                    for line in input_file:
                        output_file.write(line)

    # Parse concatenated logs and save as CSV
    log_data = []
    with open(output_file_name, 'r', errors='replace') as input_file:
        for line in input_file:
            parsed_line = parse_log_line(line)
            if parsed_line:
                log_data.append(parsed_line)

    output_file_path = os.path.join(app_path, 'concatenated.csv')
    df = pd.DataFrame(log_data)
    df.to_csv(output_file_path, index=False)
