from utils import ContextInjector, GPTClient, Planner, StepPlanner
from utils.gpt_functions import AVAILABLE_FUNCTIONS
from loguru import logger
from halo import Halo


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

    def run(self):
        context = self.context_injector.get_context_for_prompt(self.objective, max_context_items=20)
        context_text = "\n".join(context['code'].to_list())

        self.plan = self.planner.analyze_and_make_plan(self.objective, context_text)

        for step in self.plan:
            spinner = Halo(text=step, spinner='dots')
            spinner.start()

            execution_result = self.__execute_step(step)
            if execution_result:
                spinner.succeed(step)
                logger.info(step)
            else:
                spinner.fail(step)
                logger.error(step)

    def __execute_step(self, step: str):
        _temp = step.lower()
        if 'open the file' in _temp:
            return True

        # todo: 

        context = self.context_injector.get_context_for_prompt(step, max_context_items=15)
        context_text = "\n".join(context['code'].to_list())

        gpt_response = self.step_planner.analyze_step(self.objective, context_text, step)
        gpt_response = gpt_response['choices'][0]
        if gpt_response['finish_reason'] not in ['function_call']: # add 'stop' later ?
            raise Exception(f'gpt api finish reason unsupported: {gpt_response["finish_reason"]}\ngpt response: {gpt_response}')

        function_to_call = gpt_response['message']['function_call']
        print('func to call: ', function_to_call)
        exit()

