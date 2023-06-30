from agents.code_agent import CodeAgent
import sys


prompt = sys.argv[1]
agent = CodeAgent(prompt)

agent.run()