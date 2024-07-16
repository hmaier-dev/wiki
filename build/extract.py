import sys
import os
import re


# 1st/2nd empty line are used as delimiters
def extract_table_of_contents(file_path):
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
def censor_table_of_contents(private_toc):
    censored = []
    public = ""
    f = os.listdir(".")
    wiki_files = [file for file in f if file.endswith('.wiki')]
    pattern = r"\*\s\[\[(.*)\]\]|\*\s(.*)"
    for line in private_toc:
        matches = re.findall(pattern, line)
        link = matches[0][0]
        no_link = matches[0][1]
        if f"{link}.wiki" in wiki_files:
            public = public + line
        elif no_link:
            public = public + line
        else:
            censored.append(line)
    return public, censored


private = sys.argv[1]
public_name = sys.argv[2]

toc = extract_table_of_contents(private)

if toc is not None:
    public, censored = censor_table_of_contents(toc)
    with open(public_name, 'w') as file:
        file.write(public)
else:
    print("No blank lines found.")
    exit(1)
