import openai
import os


openai.api_key = os.environ.get('OPENAI_API_KEY')


class GPTClient:

    @staticmethod
    def prompt_gpt_api(messages: list, model='gpt-3.5-turbo-16k', temperature=0.0):
        response = openai.ChatCompletion.create(
            model=model,
            temperature=temperature,
            messages=messages
        )

        return response['choices'][0]['message']['content']
