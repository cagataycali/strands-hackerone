from strands import Agent
from strands_hackerone import hackerone

agent = Agent(tools=[hackerone])

agent("List my previous submissions")