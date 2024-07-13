import sys 

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

    # Extract the code block between the first and second empty lines
    if first_empty_line is not None and second_empty_line is not None:
        code_block = lines[first_empty_line + 1: second_empty_line]
        return ''.join(code_block)
    else:
        return None

public = sys.argv[1]
private = sys.argv[2]

private = extract_table_of_contents(public)
print(private)
