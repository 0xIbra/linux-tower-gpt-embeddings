from utils import ContextInjector, GPTClient, Planner


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

    def run(self):
        context = self.context_injector.get_context_for_prompt(self.objective, max_context_items=20)
        self.plan = self.planner.analyze_and_make_plan(self.objective, context)

        print('PLAN: ', self.plan)
