from utils import ContextInjector, GPTClient, Planner, StepPlanner
from utils.gpt_functions import AVAILABLE_FUNCTIONS
from loguru import logger
from halo import Halo
import json


logger.remove()
logger.add('code_agent.log', format="{time} {level} {message}", level="INFO", diagnose=False)


class CodeAgent:
    """
    This class incorporates the notion of an agent which will be responsible for completing a task given by the user.
    It's job will be to analyze the base prompt of the user, ask for clarifications if needed and 
    finally plan the whole task step by step and execute each step with validation.
    """

    def __init__(self, objective: str):
        self.objective = objective
        self.context_injector = ContextInjector()
        self.planner = Planner()
        self.step_planner = StepPlanner()
        self.previous_steps = []

    def run(self):
        context = self.context_injector.get_context_for_prompt(self.objective, max_context_items=20)
        context_text = "\n".join(context['code'].to_list())

        self.plan = self.planner.analyze_and_make_plan(self.objective, context_text)

        # temporary write plan to file
        with open('plan.txt', 'w') as f:
            f.write('\n\n'.join(self.plan))

        for step in self.plan:
            # ignore writing tests 
            if 'tests/' in step:
                continue

            spinner = Halo(text=step, spinner='dots')
            spinner.start()

            execution_result = self.__execute_step(step)
            self.previous_steps.append(step)
            if execution_result:
                spinner.succeed(step)
                logger.info(step)
            else:
                spinner.fail(step)
                logger.error(step)

    def __execute_step(self, step: str, retry=3):
        _temp = step.lower()
        if 'open the file' in _temp:
            return True
        
        context = self.context_injector.get_context_for_prompt(step, max_context_items=10)
        context_text = "\n".join(context['code'].to_list())

        previous_steps_text = "\n".join(self.previous_steps)

        trials = 0
        while trials < retry:
            trials += 1
            gpt_response = self.step_planner.analyze_step(self.objective, context_text, previous_steps_text, step)
            if gpt_response['choices'][0]['finish_reason'] == 'function_call':
                break

        gpt_response = gpt_response['choices'][0]
        if gpt_response['finish_reason'] not in ['function_call']:
            raise Exception(f'gpt api finish reason unsupported: {gpt_response["finish_reason"]}\ngpt response: {gpt_response}')

        function_call_content = gpt_response['message']['function_call']
        # print('\n')
        # print(function_call_content)
        # print('\n')
        # print('function call: ', function_call_content)
        function_name = function_call_content['name']
        function_args = json.loads(function_call_content['arguments'])

        function_to_call = AVAILABLE_FUNCTIONS[function_name]

        return function_to_call(**function_args)
