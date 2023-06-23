from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import json


EMBEDDING_MODEL = "text-embedding-ada-002"


class ContextInjector:
    """
    Class responsible for retrieving and injecting context most relevant to user's prompt.
    """

    def __init__(self, context_file: str = None):
        self.__context_file = 'api_embedding_data.csv'
        if context_file is not None:
            self.__context_file = context_file

        self.__df = pd.read_csv(self.__context_file)
        self.__df['code_embedding'] = self.__df['code_embedding'].apply(lambda x: json.loads(x))
        self.__df['code_summarization_embedding'] = self.__df['code_summarization_embedding'].apply(lambda x: json.loads(x))

    def get_context_for_prompt(self, prompt_query: str, max_context_items=3):
        """
        Search and retrieve x most relevant pieces of context.
        """

        query_embedding = get_embedding(prompt_query, engine=EMBEDDING_MODEL)
        # self.__df['similarities'] = self.__df['code_embedding'].apply(lambda x: cosine_similarity(x, query_embedding))
        self.__df['similarities'] = self.__df['code_summarization_embedding'].apply(lambda x: cosine_similarity(x, query_embedding))

        return self.__df.sort_values('similarities', ascending=False).head(max_context_items)


    # todo: measure relevancy to better classify context items (data)
