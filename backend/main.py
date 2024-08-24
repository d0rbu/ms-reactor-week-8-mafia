import random
import asyncio
import dataclasses
import random
import json
from agent import Agent, MafiaMessage
from prompts import INSTRUCTION_PROMPT, INFO_PROMPTS, SYSTEM_PROMPTS, SCENE_PROMPT
from fastapi import FastAPI, WebSocket
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
colors = random.sample(['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink', 'brown', 'black'], 3)
agents = [Agent([INSTRUCTION_PROMPT, system_prompt], name, color) for system_prompt, name, color in zip(SYSTEM_PROMPTS, names, colors)]
user_color = 'white'
killer = agents[2].name.lower()

conversation: list[MafiaMessage] = [
    MafiaMessage(content=SCENE_PROMPT, user="system", color="black"),
    *[
        MafiaMessage(content=info, user="system", color="black")
        for info in INFO_PROMPTS
    ]
]

game_over = False

@app.get("/messages")
def get_messages() -> list[dict]:
    global conversation

    return [dataclasses.asdict(message) for message in conversation]

@app.post("/guess")
async def guess(killer_guess: str):
    global game_over

    if killer_guess.lower() == killer:
        message = MafiaMessage(content="Winner winner chicken dinner!", user="system", color="black")
    else:
        message = MafiaMessage(content=f"{killer_guess} guessed incorrectly! You died 💀", user="system", color="black")
    
    conversation.append(message)
    game_over = True

    return dataclasses.asdict(message)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while not game_over:
        sent_second_message = False
        # wait 20 seconds for a user message. if no message is received, send a message from the agents
        try:
            user_message = await asyncio.wait_for(websocket.receive_text(), timeout=None if sent_second_message else 20)
        except asyncio.TimeoutError:
            print("No user message received")
            user_message = None
            sent_second_message = True

        if user_message is not None:
            conversation.append(MafiaMessage(content=user_message, user="user", color=user_color))

        agents_shuffled = agents.copy()
        random.shuffle(agents_shuffled)
        for agent in agents:
            response = agent.respond(conversation)
            conversation.append(response)
            await websocket.send_text(json.dumps(dataclasses.asdict(response)))
