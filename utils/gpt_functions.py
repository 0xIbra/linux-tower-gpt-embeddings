import os


def fwrite(file: str, data: str):
    dirpath = os.path.dirname(file)
    if dirpath != os.path.basename(file) and not os.path.isdir(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    with open(file, 'w') as f:
        f.write(data)

    return True


def fedit(file: str, start_line: int, data: str):
    # Read the contents of the file.
    with open(file, 'r') as file:
        lines = file.readlines()

    # Insert the text.
    lines.insert(start_line, data + "\n")

    # Write the contents back to the file.
    with open(file, 'w') as file:
        file.writelines(lines)

    return True


FUNCTIONS = [
    {
        'name': 'fwrite',
        'description': 'Write text to a file, also creates directory for the file if it doesn\'t exist already.',
        'parameters': {
            'type': 'object',
            'properties': {
                'file': {'type': 'string', 'description': 'the file path'},
                'data': {'type': 'string', 'description': 'text data to be written to the file'}
            },
            'required': ['file', 'data']
        }
    },
    {
        'name': 'fedit',
        'description': 'Insert text into an existing file after a given line.',
        'parameters': {
            'type': 'object',
            'properties': {
                'file': {'type': 'string', 'description': 'File path to be edited'},
                'start_line': {'type': 'integer', 'description': 'The line number after which the text should be inserted in the file.'},
                'data': {'type': 'string', 'description': 'Text data to be inserted in the file.'}
            }
        }
    }
]

AVAILABLE_FUNCTIONS = {
    'fwrite': fwrite,
    'fedit': fedit
}
