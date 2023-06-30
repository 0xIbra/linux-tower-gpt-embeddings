from utils import ContextInjector, GPTClient

class CodeAgent:
    """
    This class incorporates the notion of an agent which will be responsible for completing a task given by the user.
    It's job will be to analyze the base prompt of the user, ask for clarifications if needed and 
    finally plan the whole task step by step and execute each step with validation.
    """

    def __init__(self, objective: str):
        self.__objective = objective
        self.__context_injector = ContextInjector()

    def run(self):
        self.__analyze_objective()

    def __analyze_objective(self):
        context = self.__context_injector.get_context_for_prompt(self.__objective, max_context_items=20)

        message = f"""
        Objective:
        {self.__objective}

        Context:
        {context}

        ---
        Analyze the objective above and make a step by step plan of all actions required in all the code files to achieve the end result.
        """.strip()

        sys_msg = """
        You are a expert coder, your job is to the best of your ability to establish a step by step detailed plan to perform the task given by the user.
        """.strip()

        messages = [
            {'role': 'system', 'content': sys_msg},
            {'role': 'user', 'content': message}
        ]
        plan = GPTClient.prompt_gpt_api(messages)

        print('PLAN:', plan)
        exit()

