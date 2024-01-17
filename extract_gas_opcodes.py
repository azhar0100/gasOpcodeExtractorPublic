import json
from pprint import pprint
import requests
import re
from joblib import Memory

mem = Memory('gasCodeMem')

@mem.cache
def download_opcode_file(url="https://raw.githubusercontent.com/Shirk/vim-gas/master/syntax/gas.vim"):
    # Download the file content
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to download the file"

    return response.text

opcode_text = download_opcode_file()
opcode_lines = opcode_text.split('\n')

opcode_lines = [x for x in opcode_lines if x.startswith('syn keyword')]
# print("\n".join(opcode_lines))
opcode_lines_stripped_of_begin_words = [x.replace('syn keyword ','') for x in opcode_lines]
# opcode_lines_stripped_of_begin_words = [x for x in opcode_lines]
opcode_lines_with_instruction_code = [(x.split()[0],x.split()[1:]) for x in opcode_lines_stripped_of_begin_words]
dict_opcode_list = {}
for k,vs in opcode_lines_with_instruction_code:
    dict_opcode_list.setdefault(k,[])
    dict_opcode_list[k] += vs

dict_opcode_list = {k:sorted(list(set(vs))) for k,vs in dict_opcode_list.items()}
with open('gas_codes.json','w') as f:
    json.dump(dict_opcode_list,f,indent=2)
pprint(dict_opcode_list)
