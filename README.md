# Youtube Chatbot

This is a simple chatbot that uses the Youtube API to search for videos and return 5 videos based on the user's query. The chatbot is built with Gemini's LLM API, Youtube API and Python's Typer library. 

## Installation

To install the required packages, run the following command:

```bash
pip install virtualenv
sudo virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

To run the chatbot, run the following command:

```bash
python main.py
```

## Development Process

I started by first writing the code to get the Youtube API key and search for videos based on the user's query. I directly tried creating my own API wrapper but it was really messy and hard to maintain so I decided to use the Google API's Python client.

I then wrote the code to get the user's query and return the top 5 videos based on the query. I then used Gemini's LLM API to generate responses for the chatbot. Finally, I used Python's Typer library to create a CLI for the chatbot.