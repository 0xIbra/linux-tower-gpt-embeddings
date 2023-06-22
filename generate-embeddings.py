from argparse import ArgumentParser
from openai.embeddings_utils import get_embedding
from utils import CodeReader, CodeSummarizer
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
GPT_MODEL = "gpt-3.5-turbo-0613"
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

    code_data = []
    for file_path in files:
        in_context_file_path = file_path.replace(f'{directory}/', '')

        reader = CodeReader(file_path)
        code = reader.get_full_code()
        code = f'# file: {in_context_file_path}\n{code}'
        code_embedding = get_embedding(code, engine=EMBEDDING_MODEL)

        code_summarization = CodeSummarizer.summarize(code, model='gpt-4')
        code_summarization_embedding = get_embedding(code_summarization, engine=EMBEDDING_MODEL)

        data_item = {
            'filename': os.path.basename(file_path),
            'filepath': in_context_file_path,
            'code': code,
            'code_embedding': code_embedding,
            'code_summarization': code_summarization,
            'code_summarization_embedding': code_summarization_embedding
        }
        code_data.append(data_item)

        print(f'processed {file_path}')

    df = pd.DataFrame(code_data)
    df.to_csv("api_embedding_data.csv", index=False)

    print(f'\n[info] embeddings generated for {len(code_data)} files.')

if __name__ == "__main__":
    main()
