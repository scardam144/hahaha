import os
import re
import sys

directory_path = "/home/devops/Rushi/record"
#cronus
#artemis
#neutron
#voyager
if len(sys.argv) != 2:
    print("Usage: python3 test2.py <filename>")
    sys.exit(1)


p_t = r'^.*{}.*\.out$'
filename = sys.argv[1]
pattern = p_t.format(filename)
file_pattern = re.compile(pattern)

def print_lines(file_path, line_numbers):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        print(f"Lines from {file_path}:")
        for line_number in line_numbers:
            if 1 <= line_number <= len(lines):
                print(f"Line {line_number}: {lines[line_number - 1].strip()}")
        print(f"Last 10 lines of {file_path}:")
        for line in lines[-15:]:
            print(line.strip())


def main():
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        print(f"Directory {directory_path} does not exist.")
        return
    
    file_list = os.listdir(directory_path)
    n=0
    for file_name in file_list:
        if file_pattern.match(file_name):
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path):
                line_numbers = [3]  # You can add more line numbers here
                print_lines(file_path, line_numbers)
                #print_last_10_lines(file_path)
                print("\n")
                print("*" * 100)
                n=n+1
                print(n+1)
                print("\n")

if __name__ == "__main__":
    main()