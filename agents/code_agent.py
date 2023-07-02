from utils import ContextInjector, GPTClient, Planner, StepPlanner


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
            self.__execute_step(step)

    def __execute_step(self, step: str):
        _temp = step.lower()
        if 'open the file' in _temp:
            return

        # todo: 

        context = self.context_injector.get_context_for_prompt(step, max_context_items=15)
        context_text = "\n".join(context['code'].to_list())

        step_plan = self.step_planner.analyze_step(self.objective, context_text, step)
