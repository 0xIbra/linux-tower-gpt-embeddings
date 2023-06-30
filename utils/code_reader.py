from redbaron import RedBaron
import os


class CodeReader:
    """
    Helper class that reads code from .py files and cuts into chunks
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        if not os.path.isfile(self.filepath):
            raise Exception(f'file "{self.filepath}" was not found.')

        with open(self.filepath, 'r') as f:
            self.code = f.read()
            self.red = RedBaron(self.code)

    def is_class(self):
        for node in self.red:
            if node.type == "class":
                return True

        return False

    def get_functions(self):
        func_strs = []
        for node in self.red:
            pass

    def get_full_code(self):
        code = ""
        for node in self.red:
            if node.type == "comment":
                continue

            chunk = str(node).strip()
            code += f"{chunk}\n"

        return code
