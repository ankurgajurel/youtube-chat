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

I tried to implement function calling but Gemini's LLM API was really hard to work with and it used to give the same function call response for any kind of question. There was also a way to use Python's client library for function calling but I didn't have enough time for it.

I also tried using Claude AI's LLM but it was really slow and since I did not have enough time, I decided to use Gemini's LLM API.


## Usage

This project was built within a specific timeframe and sometimes the LLM hallucinates. 

For best usage, please follow the following steps:

1. Run the chatbot using the command `python main.py`
2. To search for videos, enter your query with the keyword "search" to search for videos
3. To summarize a video, enter your query with the keyword "summarize" to summarize a video