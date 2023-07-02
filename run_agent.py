from agents.code_agent import CodeAgent


with open('prompt.txt', 'r') as f:
    prompt = f.read().strip()

agent = CodeAgent(prompt)
agent.run()
