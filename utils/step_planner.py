from utils import GPTClient
from utils.gpt_functions import FUNCTIONS


class StepPlanner:

    def analyze_step(self, objective: str, context: str, step: str):
        msg = f"""
        Main objective:
        {objective}

        Context:
        {context}
        ---
        {step}
        """.strip()

        messages = [
            {'role': 'system', 'content': StepPlanner.role_message()},
            {'role': 'user', 'content': msg}
        ]

        print('prompt: \n', msg)
        print('\n\n')
        response = GPTClient.prompt_gpt_api(messages, functions=FUNCTIONS, return_content=False)
        print(response)
        exit()

    @staticmethod
    def role_message():
        msg = """
        You are an expert coder, your job is to the best of your ability perform the task above taking into consideration the available functions to you.
        """.strip()

        return msg
