from argparse import ArgumentParser
from openai.embeddings_utils import get_embedding
import pandas as pd
import numpy as np
import openai
import math
import glob
import pathlib
import redbaron
import re
import os


########### OPENAI ###########
EMBEDDING_MODEL = "text-embedding-ada-002"
openai.api_key = os.environ.get("OPENAI_API_KEY")


###### OTHER #######
extensions = [".py"]
directory = "linux-tower/api"


def main():
    global extensions
    global directory

    arg = ArgumentParser()
    arg.add_argument('--extensions', '-x', nargs="+", required=False, default=extensions, help="File extensions which will be included in generating embeddings for. Default: [.py]")
    arg.add_argument('--directory', '-d', type=str, required=False, default=directory, help="Directory to files")

    inputs = arg.parse_args()

    extensions = inputs.extensions
    directory = inputs.directory

    files = [y for x in os.walk(directory) for ext in extensions for y in glob.glob(os.path.join(x[0], '*'+ext))]

    for file_path in files:
        with open(file_path, "r") as f:
            red = redbaron.RedBaron(f.read())

        for i, node in enumerate(red):
            print(str(node))
            exit()

        exit()


if __name__ == "__main__":
    main()
