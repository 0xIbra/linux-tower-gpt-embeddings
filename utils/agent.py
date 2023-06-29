from utils import CodeSummarizer, ContextInjector


class Agent:
    """
    This class incorporates the notion of an agent which will be responsible for completing a task given by the user.
    It's job will be to analyze the base prompt of the user, ask for clarifications if needed and 
    finally plan the whole task step by step and execute each step with validation.
    """

    def __init__(self, objective: str):
        self.__objective = objective
