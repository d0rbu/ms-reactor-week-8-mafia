import os
import json

from dotenv import load_dotenv
from typing import Self
from enum import Enum
from octoai.text_gen import ChatMessage
from octoai.client import OctoAI

load_dotenv()

class Response(Enum):
    NO_RESPONSE = 1

class Agent:
    def __init__(self: Self, system_prompts: list[str], name: str) -> None:
        self.system_prompts = system_prompts
        self.name = name
        self.client = OctoAI(
            api_key=os.getenv('OCTOAI_KEY'),
        )

    def respond(self: Self, conversation: list[str]) -> str | Response:
        messages=[
            ChatMessage(
                content="\n\n".join(self.system_prompts),
                role="system"
            ),
            *[ChatMessage(
                content=message,
                role="user"
            ) for message in conversation]
        ]

        response = self.client.text_gen.create_chat_completion(
            max_tokens=512,
            messages=messages,
            model="meta-llama-3.1-8b-instruct",
            presence_penalty=0,
            temperature=0,
            top_p=1
        ).choices[0].message.content

        if response == "NO_RESPONSE":
            return Response.NO_RESPONSE

        return response
