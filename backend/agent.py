import os

from dotenv import load_dotenv
from typing import Self
from enum import Enum
from octoai.text_gen import ChatMessage
from octoai.client import OctoAI

load_dotenv()

class Response(Enum):
    NO_RESPONSE = 1
    STARTED_TYPING_BUT_NOT_SENT = 2

class Agent:
    def __init__(self: Self, system_prompt: str, name: str) -> None:
        self.system_prompt = system_prompt
        self.name = name
        self.client = OctoAI(
            api_key=os.getenv('OCTOAI_KEY'),
        )

    def respond(self: Self, messages: str) -> str | Response:

        self.client.text_gen.create_chat_completion_stream(
            max_tokens=512,
            messages=[
                ChatMessage(
                    content=self.system_prompt,
                    role="system"
                ),
                [ChatMessage(
                    content=message,
                    role="user"
                ) for message in messages]
                
            ],
            model="meta-llama-3.1-8b-instruct",
            presence_penalty=0,
            temperature=0,
            top_p=1
        )
