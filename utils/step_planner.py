from utils import GPTClient
from utils.gpt_functions import FUNCTIONS


class StepPlanner:

    def analyze_step(self, objective: str, context: str, previous: str, step: str):
        msg = f"""
        Main objective:
        {objective}

        Context:
        {context}

        Previous tasks:
        {previous}

        ---
        Current task: {step}
        """.strip()

        messages = [
            {'role': 'system', 'content': StepPlanner.role_message()},
            {'role': 'user', 'content': msg}
        ]

        model = 'gpt-4'
        # model = 'gpt-3.5-turbo-16k'

        return GPTClient.prompt_gpt_api(messages, model=model, functions=FUNCTIONS, return_content=False)

    @staticmethod
    def role_message():
        msg = """
        You are an expert coder, your job is to the best of your ability perform the task above taking into consideration the available functions to you.
        Remember that you are expected to perform the task with functions.
        """.strip()

        return msg
