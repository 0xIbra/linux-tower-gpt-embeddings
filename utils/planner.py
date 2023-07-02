from utils import GPTClient
import re


class Planner:

    def analyze_and_make_plan(self, objective: str, context: str):
        msg = f"""
        Objective:
        {objective}

        Context:
        {context}

        ---
        Analyze the objective above and make a step by step plan of all actions required in all the code files to achieve the end result.
        """.strip()

        messages = [
            {'role': 'system', 'content': Planner.role_message()},
            {'role': 'user', 'content': msg}
        ]

        raw_plan = GPTClient.prompt_gpt_api(messages)

        return Planner.parse_plan(raw_plan)

    @staticmethod
    def parse_plan(plan: str):
        steps = []
        temp_step = ""
        for line in plan.split('\n'):
            if re.match(r"\d+\.", line):  # if the line starts with number and period (e.g., "1.")
                if temp_step:  # if there is a previous step, add it to the list
                    steps.append(temp_step.strip())
                temp_step = line  # start a new step

        return steps


    @staticmethod
    def role_message():
        msg = """
        You are an expert coder, your job is to the best of your ability to establish a step by step detailed plan to perform the task given, keep in mind that you are talking to another gpt agent.
        No need to write any tests, focus on the objective.
        Make the plan parseable by a program by making sure that 1 line equals 1 step as this plan will be parsed and handled by a gpt agent.
        """.strip()

        return msg
