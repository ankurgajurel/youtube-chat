from typing import TypedDict
from dotenv import dotenv_values


class ConfigEnvironmentType(TypedDict):
    YOUTUBE_API_KEY: str
    GEMINI_API_KEY: str
    CLAUDE_API_KEY: str


config_environemnt: ConfigEnvironmentType = dict(dotenv_values(".env"))