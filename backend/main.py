import random
import asyncio
import dataclasses
import random
import json
import uvicorn
from agent import Agent, MafiaMessage
from prompts import INSTRUCTION_PROMPT, INFO_PROMPTS, SYSTEM_PROMPTS, SCENE_PROMPT
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

names = ["Heidi", "Vincent", "Isabella"]

# Create agents with the chosen prompts and names
colors = random.sample(['green', 'yellow', 'violet', 'orange', 'fuchsia', 'sky', 'rose'], 3)
agents = [Agent([INSTRUCTION_PROMPT, system_prompt], name, color) for system_prompt, name, color in zip(SYSTEM_PROMPTS, names, colors)]
user_color = 'blue'
killer = agents[2].name.lower()

conversation: list[MafiaMessage] = [
    MafiaMessage(content=SCENE_PROMPT, user="system", color="slate"),
    *[
        MafiaMessage(content=info, user="system", color="slate")
        for info in INFO_PROMPTS
    ]
]

game_over = False

@app.get("/messages")
def get_messages() -> list[dict]:
    global conversation

    return [dataclasses.asdict(message) for message in conversation]

@app.get("/guess/{killer_guess}")
async def guess(killer_guess: str):
    global game_over

    message = MafiaMessage(content=f"The killer is {killer_guess}!", user="user", color=user_color)
    conversation.append(message)
    game_over = True

    return dataclasses.asdict(message)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global game_over

    if game_over:
        return

    rounds_since_last_message = 0
    await websocket.accept()
    while not game_over:
        # wait 20 seconds for a user message. if no message is received, send a message from the agents
        try:
            user_message = await asyncio.wait_for(websocket.receive_text(), timeout=None if rounds_since_last_message < 2 else random.randint(10, 25))
            if user_message == "GAME_OVER":
                game_over = True
                break

            user_message = json.loads(user_message)
            rounds_since_last_message = 0
        except asyncio.TimeoutError:
            print("No user message received")
            user_message = None
            rounds_since_last_message += 1

        if game_over:
            break

        if user_message is not None:
            conversation.append(MafiaMessage(**user_message))

        if rounds_since_last_message < 2:
            agents_shuffled = agents.copy()
            random.shuffle(agents_shuffled)
            for agent in agents:
                if game_over:
                    break
                response = agent.respond(conversation)
                conversation.append(response)
                await websocket.send_text(json.dumps(dataclasses.asdict(response)))

    # voting time
    random.shuffle(agents)
    votes = {
        agent.name: 0
        for agent in agents
    }
    votes["user"] = 0
    for agent in agents:
        vote = agent.vote(conversation)
        voted_agents = [agent for agent in agents if agent.name.lower() == vote]
        voted_agent = voted_agents[0] if voted_agents else "user"
        proper_name = voted_agent.name if voted_agent != "user" else "user"
        name = f"{voted_agent.name} is" if voted_agent != "user" else "you are"
        conversation.append(MafiaMessage(content=f"I think {name} the killer!", user=agent.name, color=agent.color))
        votes[proper_name] += 1

        await websocket.send_text(json.dumps(dataclasses.asdict(conversation[-1])))

    chosen_agent = max(votes, key=votes.get)
    chosen_agents = [agent for agent in agents if agent.name == chosen_agent]
    chosen_agent = chosen_agents[0] if chosen_agents else "user"
    proper_chosen_name = chosen_agent.name if chosen_agent != "user" else "user"
    chosen_name = f"{chosen_agent.name} has" if chosen_agent != "user" else "You have"
    correct = proper_chosen_name.lower() == killer
    correct_str = "correctly" if correct else "incorrectly"

    message = MafiaMessage(content=f"{chosen_name} been {correct_str} chosen as the killer!", user="system", color="slate")
    conversation.append(message)
    await websocket.send_text(json.dumps(dataclasses.asdict(message)))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
