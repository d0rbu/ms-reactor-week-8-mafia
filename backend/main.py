import random
from agent import Agent
from prompts import SYSTEM_PROMPTS


num_agents = len(SYSTEM_PROMPTS)
# chosen_names = random.sample(["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"], 3)
chosen_names = ["Alice", "Bob", "Charlie"]

# Create agents with the chosen prompts and names
agents = [Agent(prompt, name) for prompt, name in zip(SYSTEM_PROMPTS, chosen_names)]
killer = agents[2].name


def run_conversation():
    print("Welcome to the multi-agent conversation! Type 'exit' to end the conversation.")
    conversation = []

    while True:
        user_input = input("You: ")
        if user_input.lower().startswith("the killer is"):
            if user_input.lower().endswith(killer):
                print("you won!")
            else:
                print("you lose!")
            break

        conversation.append(user_input)

        # Each agent responds in turn
        for agent in agents:
            response = f"{agent.name}: {agent.respond(conversation)}"
            print(response)
            conversation.append(response)


if __name__ == "__main__":
    run_conversation()