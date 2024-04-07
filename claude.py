import anthropic
from config import config_environemnt


def generate_response(prompt: str) -> str:

    client = anthropic.Anthropic(
        api_key=config_environemnt["CLAUDE_API_KEY"],
    )
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    print(message.content[0].text)