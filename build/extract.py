import sys
import os
import re
from pathlib import Path


# 1st/2nd empty line are used as delimiters
def extract_table_of_contents(file_path):
    try:
        Path(file_path).resolve(strict=True)
    except FileNotFoundError:
        print(file_path + " hasn't been found...")
        exit(1)

    with open(file_path, 'r') as file:
        lines = file.readlines()

    first_empty_line = None
    second_empty_line = None
    for i, line in enumerate(lines):
        if line.strip() == '':
            if first_empty_line is None:
                first_empty_line = i
            elif second_empty_line is None:
                second_empty_line = i
                break

    if first_empty_line is not None and second_empty_line is not None:
        code_block = lines[first_empty_line + 1: second_empty_line]
        return code_block
    else:
        return None


# Just use the present articles names as links
def censor_table_of_contents(private_toc, ext):
    censored = []
    public = ""
    f = os.listdir(".")
    wiki_files = [file for file in f if file.endswith("." + ext)]
    # Regex-Pattern hardcoded for Markdown-Links 
    # (e.g. * [Python](Python))
    pattern = r"\*\s\[(.*)\]|\*\s(.*)"
    for line in private_toc:
        matches = re.findall(pattern, line)
        link = matches[0][0]
        no_link = matches[0][1]
        if f"{link}.{ext}" in wiki_files:
            public = public + line
        elif no_link:
            public = public + line
        else:
            censored.append(line)
    return public, censored


file_path = sys.argv[1]
extension = file_path.split('.')[-1]

toc = extract_table_of_contents(file_path)
public_string, censored = censor_table_of_contents(toc, extension)

if toc is not None and len(censored) > 0:
    print("These links have been censored")
    print(censored)
    with open(file_path, 'w') as file:
        file.write(public_string)
else:
    print("No blank lines found.")
    print("No links have been censored.")
    print("Exiting...")
    exit(1)
