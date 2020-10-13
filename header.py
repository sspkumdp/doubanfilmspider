import agents
import random

def get1agent(headers):
    agent=random.choice(agents.agents)
    headers["User-Agent"]=agent

def get1cookie(headers):
    return

def changeheader(headers):
    get1agent(headers)
    return headers


