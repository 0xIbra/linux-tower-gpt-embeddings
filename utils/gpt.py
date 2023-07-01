import openai
import os


openai.api_key = os.environ.get('OPENAI_API_KEY')


class GPTClient:

    @staticmethod
    def prompt_gpt_api(messages: list, model='gpt-3.5-turbo-16k', temperature=0.0, functions=None):
        args = {
            'model': model,
            'temperature': temperature,
            'messages': messages
        }

        if functions is not None:
            args['functions'] = functions
        
        response = openai.ChatCompletion.create(**args)

        return response['choices'][0]['message']['content']
