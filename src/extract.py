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
    pattern = "\*\s\[\[(.*)\]\]|\*\s(.*)"
    for line in private_toc:
        matches = re.findall(pattern, line)
        match = results = [match[0] if match[0] else match[1] for match in matches]
        if f"{match[0]}.wiki" in wiki_files:
            public = public + line
        else:
            censored.append(line)
    return public, censored


private = sys.argv[1]
public_name = sys.argv[2]

toc = extract_table_of_contents(private)
public, censored = censor_table_of_contents(toc)

print(censored)
print(public)
