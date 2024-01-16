import requests
import re

def extract_gas_opcodes(url="https://raw.githubusercontent.com/Shirk/vim-gas/master/syntax/gas.vim"):
    # Download the file content
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to download the file"

    return response.text

opcodes = extract_gas_opcodes()
print(opcodes)
