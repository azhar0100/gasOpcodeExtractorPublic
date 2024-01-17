import json
import argparse
from pprint import pprint

from tqdm import tqdm

def separate_dumped_data_sections(objdumped_data):
    sections = []
    section = []
    for line in objdumped_data:
        if line.startswith('Disassembly of section'):
            if section:
                sections.append(section)
            section = []
        section.append(line)
    sections.append(section)
    return sections

def find_instruction_lines_in_section(section):
    instructions = []
    for line in section:
        if line.startswith(' '):
            instructions.append(line.split('\t')[-1].strip())
    return instructions

def identify_all_instruction_sets_in_instruction_line_using_faster_lookup_data(instruction_line, faster_lookup_data):
    instruction_sets = []
    for instruction in instruction_line.split():
        if instruction in faster_lookup_data:
            instruction_sets.append(faster_lookup_data[instruction])
    return sorted(list(set(instruction_sets)))

def main(file_path, dumped_obj_file):
    with open(file_path, "r") as file:
        data = json.load(file)

    faster_lookup_data = {x:k for k,v in data.items() for x in v}

    with open(dumped_obj_file, "r") as file:
        objdumped_data = file.readlines()

    extracted_instruction_set_data = [[identify_all_instruction_sets_in_instruction_line_using_faster_lookup_data(x, faster_lookup_data) for x in find_instruction_lines_in_section(section)] for section in tqdm(separate_dumped_data_sections(objdumped_data),desc=f"reading sections from {dumped_obj_file}")]
    extracted_instruction_set_data_flattened = sorted(list(set([x1 for x3 in extracted_instruction_set_data for x2 in x3 for x1 in x2])))
    pprint(extracted_instruction_set_data_flattened)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find binary instruction sets.')
    parser.add_argument('file_path', type=str, help='Path to the file')
    parser.add_argument('dumped_obj_file', type=str, help='Path to the dumped object file')
    args = parser.parse_args()
    main(args.file_path, args.dumped_obj_file)
