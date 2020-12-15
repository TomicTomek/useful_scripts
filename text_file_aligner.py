#!/usr/bin/python3
import sys
import os


if len(sys.argv) != 2:
    print("No file path provided")
    print("Provide file path as argument.")
    sys.exit(-1)

file_path = sys.argv[1]

if not os.path.exists(file_path):
    print("No such file: \"" + file_path + "\"")
    sys.exit(-1)

print("Attempt to sort file: \"" + file_path + "\"")

with open(file_path, mode='r') as input_file:
    Lines = input_file.readlines()
    sorted_lines = sorted(Lines)

    sorted_file_path = file_path + "_SORTED"

    with open(sorted_file_path, mode='w') as file_sorted:
        file_sorted.write(''.join(sorted_lines))

    print("OK READY")

sys.exit(0)
