from redbaron import RedBaron
import os


class CodeReader:
    """
    Helper class that reads code from .py files and cuts into chunks
    """

    def __init__(self, filepath: str):
        self.__filepath = filepath
        if not os.path.isfile(self.__filepath):
            raise Exception(f'file "{self.__filepath}" was not found.')

        with open(self.__filepath, 'r') as f:
            self.__code = f.read()
            self.__red = RedBaron(self.__code)

    def is_class(self):
        for node in self.__red:
            if node.type == "class":
                return True

        return False

    def get_functions(self):
        func_strs = []
        for node in self.__red:
            pass

    def get_full_code(self):
        code = ""
        for node in self.__red:
            if node.type == "comment":
                continue

            chunk = str(node).strip()
            code += f"{chunk}\n"

        return code
