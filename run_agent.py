from agents.code_agent import CodeAgent
import sys


with open('prompt.txt', 'r') as f:
    prompt = f.read()

agent = CodeAgent(prompt)
agent.run()
