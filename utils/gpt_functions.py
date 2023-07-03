import os


def fwrite(file: str, data: str):
    dirpath = os.path.dirname(file)
    if dirpath != os.path.basename(file) and not os.path.isdir(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    with open(file, 'w') as f:
        f.write(data)

    return True


def fedit(file: str, start_line: int, data: str):
    start_line -= 1

    with open(file, 'r') as f:
        # lines = f.read().split('\n')
        lines = f.readlines()

    lines.insert(start_line, '\n' + data + '\n')

    with open(file, 'w') as f:
        f.write('\n'.join(lines))

    return True


FUNCTIONS = [
    {
        'name': 'fwrite',
        'description': 'Write text to a new file or rewrite existing file.',
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
        'description': 'Edit file, add code into an existing file on a given line.',
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

