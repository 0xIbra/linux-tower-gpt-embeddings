from agents.code_agent import CodeAgent
import os


if not os.path.isfile('prompt.txt'):
    prompt = input('What should i do on linux-tower ?\n')

    with open('prompt.txt', 'w') as f:
        f.write(prompt)

with open('prompt.txt', 'r') as f:
    prompt = f.read().strip()

agent = CodeAgent(prompt)
agent.run()
