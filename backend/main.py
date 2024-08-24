import random
from agent import Agent
from prompts import INSTRUCTION_PROMPT, INFO_PROMPTS, SYSTEM_PROMPTS, SCENE_PROMPT
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

names = ["Heidi", "Vincent", "Isabella"]

# Create agents with the chosen prompts and names
agents = [Agent([INSTRUCTION_PROMPT, system_prompt], name) for system_prompt, name in zip(SYSTEM_PROMPTS, names)]
killer = agents[2].name.lower()

conversation = [SCENE_PROMPT, *INFO_PROMPTS]


def run_conversation():
    # i hate globals too but we have like a couple hours lol
    global conversation

    print("Welcome to the multi-agent conversation! Type 'exit' to end the conversation.")

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
            response = agent.respond(conversation)
            print(response)
            conversation.append(response)

@app.get("/messages")
def get_messages() -> list[str]:
    global conversation

    return conversation

# going to write a websocket for the live messages as they come in



if __name__ == "__main__":
    run_conversation()